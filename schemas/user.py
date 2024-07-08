from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class UserCreate(BaseModel):
	firstName: str
	lastName: str
	email : EmailStr
	password : str = Field(..., min_length=4)
	phone: str


class UserLogin(BaseModel):
	email : EmailStr
	password : str = Field(..., min_length=4)


class ShowUser(BaseModel):
    userId: int
    firstName: str
    lastName: str
    email : EmailStr
    phone: Optional[str] = None

    class Config():
        from_attributes = True
        
