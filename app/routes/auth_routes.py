from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import Register, Login
from app.services import user_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: Register, db: Session = Depends(get_db)):
    return user_service.register_user(user, db)


@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    return user_service.login_user(user, db)