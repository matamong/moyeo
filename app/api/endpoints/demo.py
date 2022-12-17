from fastapi import APIRouter
from starlette import status
from typing import List

from app.schemas.dates import UserSchedules
from app.utils import find_most_overlapping_dates

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

    most_overlaps = find_most_overlapping_dates(dates=dates)
    return {"result": most_overlaps}