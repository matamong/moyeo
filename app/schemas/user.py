from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared Properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    nickname: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    nickname: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB. eg.hashed_password
class UserInDB(UserInDBBase):
    pass
