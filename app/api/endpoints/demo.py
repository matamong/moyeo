from fastapi import APIRouter
from starlette import status
from typing import List

from app.schemas.dates import UserSchedules
from app.utils import find_most_overlapping_date

router = APIRouter()

@router.post(
    "/date",
    status_code=status.HTTP_200_OK,
    name="demo: find-most-available-date",
    tags=["demo"]
)
def get_most_overlapping_date(request: UserSchedules):
    dates = []
    for schedule in request.schedules:
        for d in schedule.dates:
            dates.append(d)

    most_overlap = find_most_overlapping_date(dates=dates)
    
    return f"The date with the most overlap is {most_overlap}"