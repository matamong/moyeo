from typing import List, Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependency

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(dependency.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        db: Session = Depends(dependency.get_db),
) -> Any:
    user = crud.user.get(db, id=user_id)
    return user


@router.get("/me", response_model=schemas.UserInDB)
def read_user_me(
        current_user: models.User = Depends(dependency.get_current_user)
) -> Any:
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(dependency.get_db),
        nickname: str = Body(None),
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if nickname is not None:
        user_in.nickname = nickname
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.delete("/me", response_model=schemas.User)
def delete_user_me(
        *,
        db: Session = Depends(dependency.get_db),
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    user = crud.user.remove(db, id=int(current_user.id))
    return user

