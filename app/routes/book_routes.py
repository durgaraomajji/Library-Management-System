from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.book_schema import BookCreate
from app.services import book_service

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(book, db)


@router.get("/")
def get_books(
    search: str = None,
    category: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return book_service.get_books(search, category, page, limit, db)


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.get_book(book_id, db)


@router.put("/{book_id}")
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return book_service.update_book(book_id, book, db)


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.delete_book(book_id, db)