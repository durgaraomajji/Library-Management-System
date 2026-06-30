from fastapi import FastAPI

from app.database import Base, engine

# Import all models
from app.models.user import User
from app.models.book import Book
from app.models.member import Member
from app.models.issue import Issue

# Import all routers
from app.routes.auth_routes import router as auth_router
from app.routes.book_routes import router as book_router
from app.routes.member_routes import router as member_router
from app.routes.issue_routes import router as issue_router


# Create all database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Library Management System",
    description="Library Management System using FastAPI, SQLAlchemy, MySQL and JWT Authentication",
    version="1.0.0"
)


# Include Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(book_router, prefix="/books", tags=["Books"])
app.include_router(member_router, prefix="/members", tags=["Members"])
app.include_router(issue_router, tags=["Book Issue & Return"])


@app.get("/")
def root():
    return {
        "message": "Library Management System API is running successfully!"
    }