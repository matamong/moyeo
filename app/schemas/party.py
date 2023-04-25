from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User


# Shared Properties
class PartyBase(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    code: Optional[str] = None  # 나중에 따로 빼기
    access_code: Optional[str] = None   # 나중에 따로 빼기
    img_path: Optional[str] = None
    leader_id: Optional[int] = None
    is_private: Optional[bool] = False
    created_at: Optional[datetime] = None


class PartyUserBase(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    party_id: Optional[int] = None
    is_manager: Optional[bool] = False
    nickname: Optional[str] = None


class PartyCreate(BaseModel):
    name: str
    nickname: str
    desc: Optional[str] = None
    img_path: Optional[str] = None
    is_private: Optional[bool] = False


class PartyUpdate(PartyBase):
    pass


class PartyInDBBase(PartyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Party(PartyInDBBase):
    pass


##############
# PartyUser
#############

class PartyUserCreate(PartyUserBase):
    party_id: int


class PartyUserInDBBase(PartyUserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class PartyUser(PartyUserInDBBase):
    pass


class PartyUserSimple(BaseModel):
    id: int
    nickname: str
    is_manager: bool

    class Config:
        orm_mode = True


class PartyWithPartyUser(Party):
    party_user_set: list[PartyUserSimple] = []

    class Config:
        orm_mode = True


class PartyUserCreate(BaseModel):
    party_id: int
    nickname: str
    party_code: Optional[str | None]


class PartyUserUpdate(PartyUserBase):
    pass
