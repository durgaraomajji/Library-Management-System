from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.member_schema import MemberCreate
from app.services import member_service

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.post("/")
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    return member_service.create_member(member, db)


@router.get("/")
def get_members(db: Session = Depends(get_db)):
    return member_service.get_members(db)


@router.get("/{member_id}")
def get_member(member_id: int, db: Session = Depends(get_db)):
    return member_service.get_member(member_id, db)