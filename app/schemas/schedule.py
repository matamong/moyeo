from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel


class ScheduleBase(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    desc: Optional[str] = None


class VoteScheduleCreate(BaseModel):
    party_id: int
    manager_id: int
    title: str
    desc: Optional[str] = None
    periods: Optional[Dict[str, list[datetime]]] = None
    notices: Optional[Dict[str, list[str]]] = None


class VoteScheduleUpdate(BaseModel):
    party_id: int
