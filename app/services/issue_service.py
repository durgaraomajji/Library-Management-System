from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.member import Member
from app.models.issue import Issue
from app.schemas.issue_schema import IssueBook


# Issue Book
def issue_book(issue: IssueBook, db: Session):

    # Check member exists
    member = (
        db.query(Member)
        .filter(
            Member.id == issue.member_id,
            Member.is_active == True
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # Check book exists
    book = (
        db.query(Book)
        .filter(
            Book.id == issue.book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check availability
    if book.available_copies <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book is not available"
        )

    # Prevent duplicate active issue
    existing_issue = (
        db.query(Issue)
        .filter(
            Issue.member_id == issue.member_id,
            Issue.book_id == issue.book_id,
            Issue.returned == False
        )
        .first()
    )

    if existing_issue:
        raise HTTPException(
            status_code=400,
            detail="This member has already borrowed this book"
        )

    # Create issue
    new_issue = Issue(
        member_id=issue.member_id,
        book_id=issue.book_id,
        returned=False
    )

    db.add(new_issue)

    # Reduce available copies
    book.available_copies -= 1

    db.commit()
    db.refresh(new_issue)

    return {
        "message": "Book issued successfully",
        "issue": new_issue
    }


# Return Book
def return_book(issue_id: int, db: Session):

    issue = (
        db.query(Issue)
        .filter(Issue.id == issue_id)
        .first()
    )

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue record not found"
        )

    if issue.returned:
        raise HTTPException(
            status_code=400,
            detail="Book already returned"
        )

    book = (
        db.query(Book)
        .filter(Book.id == issue.book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Update issue status
    issue.returned = True

    # Increase available copies
    book.available_copies += 1

    db.commit()

    return {
        "message": "Book returned successfully"
    }


# Get Books Borrowed by a Member
def member_books(member_id: int, db: Session):

    member = (
        db.query(Member)
        .filter(
            Member.id == member_id,
            Member.is_active == True
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    issues = (
        db.query(Issue)
        .filter(
            Issue.member_id == member_id,
            Issue.returned == False
        )
        .all()
    )

    books = []

    for issue in issues:

        book = (
            db.query(Book)
            .filter(Book.id == issue.book_id)
            .first()
        )

        if book:
            books.append({
                "issue_id": issue.id,
                "book_id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "isbn": book.isbn
            })

    return {
        "member_id": member.id,
        "member_name": member.name,
        "borrowed_books": books
    }