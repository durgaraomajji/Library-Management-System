from pydantic import BaseModel


class BookCreate(BaseModel):

    title:str

    author:str

    category:str

    isbn:str

    total_copies:int