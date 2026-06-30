from pydantic import BaseModel


class IssueBook(BaseModel):

    member_id:int

    book_id:int