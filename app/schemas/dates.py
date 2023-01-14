from pydantic import BaseModel, Field
from typing import List, Tuple
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
    date_time: List[str] = Field(
        default=["2023-05-16 19:00", "2023-05-16 20:00", "2023-05-14 20:00", "2023-05-16 21:00"]
    )


class DateTimeRanges(BaseModel):
    date_time_ranges: List[Tuple[str, str]] = Field(
        default=[
            ["2022-05-16 14:00", "2022-05-16 17:00"],
            ["2022-05-16 12:00", "2022-05-16 18:00"],
            ["2022-05-16 15:00", "2022-05-16 16:00"]
        ]
    )
