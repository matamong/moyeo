from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from app.schemas import PartyUserSimple


class VoteScheduleBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    manager_id: Optional[int] = None
    periods: Optional[Dict[str, list[str]]] = None
    notices: Optional[Dict[str, list[str]]] = None


class VoteScheduleCreate(VoteScheduleBase):
    party_id: int
    manager_id: int
    title: str


class VoteScheduleUpdate(VoteScheduleBase):
    pass

#
# class VoteScheduleInDBBase(VoteScheduleBase):
#     id: int
#     title: str
#     party_id: int
#     manager_id: int
#
#     class Config:
#         orm_mode = True
#
#
# class VoteSchedule(VoteScheduleInDBBase):
#     pass
#
#
# ###
# # Vote Participant
# ###
#
# class VoteParticipantBase(BaseModel):
#     id: Optional[int] = None
#     vote_schedule_id: Optional[int] = None
#     party_user_id: Optional[int] = None
#     periods: Optional[Dict[str, list[datetime]]] = None
#
#
# class VoteParticipantInDBBase(VoteParticipantBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
#
# class VoteParticipant(VoteParticipantInDBBase):
#     pass
#
#
# class VoteScheduleWithParticipants(VoteSchedule):
#     party_user_set: list[PartyUserSimple] = []
#
#     class Config:
#         orm_mode = True
#
#