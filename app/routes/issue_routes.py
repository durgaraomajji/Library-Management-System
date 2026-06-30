from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.issue_schema import IssueBook
from app.services import issue_service

router = APIRouter(
    prefix="",
    tags=["Book Issue & Return"]
)


@router.post("/issues")
def issue_book(issue: IssueBook, db: Session = Depends(get_db)):
    return issue_service.issue_book(issue, db)


@router.put("/returns/{issue_id}")
def return_book(issue_id: int, db: Session = Depends(get_db)):
    return issue_service.return_book(issue_id, db)


@router.get("/members/{member_id}/books")
def member_books(member_id: int, db: Session = Depends(get_db)):
    return issue_service.member_books(member_id, db)