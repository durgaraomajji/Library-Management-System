from pydantic import BaseModel,EmailStr


class Register(BaseModel):

    username:str

    email:EmailStr

    password:str

    role:str


class Login(BaseModel):

    username:str

    password:str