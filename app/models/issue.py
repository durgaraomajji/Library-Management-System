from sqlalchemy import Column, Integer, ForeignKey, Boolean

from app.database import Base


class Issue(Base):

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("members.id"),
        nullable=False
    )

    book_id = Column(
        Integer,
        ForeignKey("books.id"),
        nullable=False
    )

    returned = Column(
        Boolean,
        default=False,
        nullable=False
    )