from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book_schema import BookCreate


# Create Book
def create_book(book: BookCreate, db: Session):

    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()

    if existing_book:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    new_book = Book(
        title=book.title,
        author=book.author,
        category=book.category,
        isbn=book.isbn,
        total_copies=book.total_copies,
        available_copies=book.total_copies
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book added successfully",
        "book": new_book
    }


# Get All Books
def get_books(
    search: str,
    category: str,
    page: int,
    limit: int,
    db: Session
):

    query = db.query(Book).filter(Book.is_deleted == False)

    # Search by title or author
    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%")
            )
        )

    # Filter by category
    if category:
        query = query.filter(Book.category == category)

    # Pagination
    offset = (page - 1) * limit

    books = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return books


# Get Single Book
def get_book(book_id: int, db: Session):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# Update Book
def update_book(
    book_id: int,
    updated_book: BookCreate,
    db: Session
):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check ISBN uniqueness
    existing = (
        db.query(Book)
        .filter(
            Book.isbn == updated_book.isbn,
            Book.id != book_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    issued_books = (
        book.total_copies - book.available_copies
    )

    book.title = updated_book.title
    book.author = updated_book.author
    book.category = updated_book.category
    book.isbn = updated_book.isbn
    book.total_copies = updated_book.total_copies

    # Keep borrowed books safe
    book.available_copies = (
        updated_book.total_copies - issued_books
    )

    if book.available_copies < 0:
        book.available_copies = 0

    db.commit()
    db.refresh(book)

    return {
        "message": "Book updated successfully",
        "book": book
    }


# Soft Delete Book
def delete_book(book_id: int, db: Session):

    book = (
        db.query(Book)
        .filter(
            Book.id == book_id,
            Book.is_deleted == False
        )
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    book.is_deleted = True

    db.commit()

    return {
        "message": "Book deleted successfully"
    }