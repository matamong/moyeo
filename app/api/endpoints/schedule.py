from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import dependency

router = APIRouter()


@router.post('/', response_model=schemas.VoteSchedule)
def create_schedule(
        *,
        db: Session = Depends(dependency.get_db),
        schedule_in: schemas.VoteScheduleCreate,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    party_user = crud.party_user.get_by_user_id(db=db, party_id=schedule_in.party_id, user_id=current_user.id)
    if not party_user or not party_user.is_manager:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    schedule_in.manager_id = party_user.id
    vote_schedule = crud.vote_schedule.create(db=db, obj_in=schedule_in)

    return vote_schedule
