from pydantic import BaseModel
from typing import List
from datetime import date, datetime


class DateSchedule(BaseModel):
    user_name: str
    dates: List[date]


class DateTimeSchedule(BaseModel):
    user_name: str
    dates: List[datetime]


class UserSchedules(BaseModel):
    schedules: List[DateSchedule]


class DateTimeStrs(BaseModel):
    date_time: List[str]
