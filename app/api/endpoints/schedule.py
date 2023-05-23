from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import dependency

router = APIRouter()


@router.post('/', response_model=schemas.VoteSchedule)
def create_vote_schedule(
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


# TODO with party_user 여부 확인하고 있으면 party_user도 같이 보내주기
@router.get('/{vote_schedule_id}', response_model=schemas.VoteSchedule)
def get_vote_schedule_by_id(
        *,
        db: Session = Depends(dependency.get_db),
        vote_schedule_id: int,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    vote_schedule = crud.vote_schedule.get(db=db, id=vote_schedule_id)
    if vote_schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    party_user = crud.party_user.get_by_user_id(db=db, party_id=vote_schedule.party_id, user_id=current_user.id)
    if party_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return vote_schedule


# TODO Async
@router.get('/with-participants/{vote_schedule_id}', response_model=schemas.VoteScheduleWithParticipants)
def get_vote_schedule_with_participants(
        *,
        db: Session = Depends(dependency.get_db),
        vote_schedule_id: int,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    vote_schedule = crud.vote_schedule.get(db=db, id=vote_schedule_id)
    if vote_schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    party_user = crud.party_user.get_by_user_id(db=db, party_id=vote_schedule.party_id, user_id=current_user.id)
    if party_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if vote_schedule.manager_id == party_user.id or party_user.is_manager is True:
        db_obj = crud.vote_schedule.get_by_id_with_users(db=db, id=vote_schedule.id)
        return schemas.VoteScheduleWithParticipants.from_orm(db_obj)
