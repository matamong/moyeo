from fastapi import APIRouter
from starlette import status

from app.schemas.dates import UserSchedules, DateTimeStrs, DateTimeRanges
from app.utils import find_most_overlapping_dates, find_most_overlapping_datetimes, find_available_intersection_datetime

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


@router.post(
    "/datetime",
    name="demo: find-most-available-date-and-time",
    tags=["demo"]
)
def get_available_date_time(request: DateTimeStrs):
    most_overlaps = find_most_overlapping_datetimes(request.date_time)
    return {"result": most_overlaps}


@router.post(
    "/interval",
    name="demo: find-most-interval-date-and-time",
    tags=["demo"]
)
def get_interval_datetime(request: DateTimeRanges):
    interval_datetime = find_available_intersection_datetime(request.date_time_ranges)
    return {"result": interval_datetime}
