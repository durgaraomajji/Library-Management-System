from pydantic import BaseModel,EmailStr
from pydantic import Field


class MemberCreate(BaseModel):

    name:str

    email:EmailStr

    phone:str=Field(min_length=10,max_length=10)