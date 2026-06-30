from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    author = Column(String(150), nullable=False)

    category = Column(String(100), nullable=False)

    isbn = Column(String(20), unique=True, nullable=False)

    total_copies = Column(Integer, nullable=False)

    available_copies = Column(Integer, nullable=False)

    is_deleted = Column(Boolean, default=False)