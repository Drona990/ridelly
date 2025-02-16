from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Union

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass

class OTPRequest(BaseModel):
    email: str
    otp: str
    
class UserOut(UserBase):
    user_id: UUID

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserResponse(BaseModel):
    user_id: UUID
    email: str

class TokenData(BaseModel):
    email: Union[str, None] = None 
