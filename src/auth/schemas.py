from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserCreateTelegram(UserBase):
    password: str
    telegram_id: Optional[str]=None

class UserResponse(UserBase):
    id: int

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: Optional[str]=None

class UserTelegramId(BaseModel):
    telegram_id: str