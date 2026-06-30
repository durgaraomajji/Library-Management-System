from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.member import Member
from app.schemas.member_schema import MemberCreate


# Create Member
def create_member(member: MemberCreate, db: Session):

    # Check if email already exists
    existing_email = (
        db.query(Member)
        .filter(Member.email == member.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Check if phone number already exists
    existing_phone = (
        db.query(Member)
        .filter(Member.phone == member.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        is_active=True
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {
        "message": "Member created successfully",
        "member": new_member
    }


# Get All Members
def get_members(db: Session):

    members = (
        db.query(Member)
        .filter(Member.is_active == True)
        .all()
    )

    return members


# Get Member By ID
def get_member(member_id: int, db: Session):

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

    return member