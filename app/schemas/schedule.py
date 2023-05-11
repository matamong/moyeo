from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel

from app.schemas import PartyUserSimple, PartyUser


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


class VoteScheduleInDBBase(VoteScheduleBase):
    id: int
    title: str
    party_id: int
    manager_id: int

    class Config:
        orm_mode = True


class VoteSchedule(VoteScheduleInDBBase):
    pass


# ###
# # Vote Participant
# ###


class VoteParticipantBase(BaseModel):
    id: Optional[int] = None
    vote_schedule_id: Optional[int] = None
    party_user_id: Optional[int] = None
    periods: Optional[Dict[str, list[str]]] = None


class VoteParticipantCreate(VoteParticipantBase):
    vote_schedule_id: int
    party_user_id: int


class VoteParticipantUpdate(VoteParticipantBase):
    periods: Optional[Dict[str, list[str]]] = None


class VoteParticipantInDBBase(VoteParticipantBase):
    id: int

    class Config:
        orm_mode = True


class VoteParticipant(VoteParticipantInDBBase):
    party_user: Optional[PartyUser] = None
    pass


class VoteScheduleWithParticipants(VoteSchedule):
    vote_participant_set: list[VoteParticipant] = []

    class Config:
        orm_mode = True
