from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.api import dependency
from app import crud, models, schemas

router = APIRouter()


# TODO : Should Super-User only. (After setting UserStatus model)
@router.get("/", response_model=List[schemas.Party])
def read_parties(
        db: Session = Depends(dependency.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    parties = crud.party.get_multi(db, skip=skip, limit=limit)
    return parties


@router.get("/me", response_model=List[schemas.PartyWithMe])
def read_my_parties(
        *,
        db: Session = Depends(dependency.get_db),
        current_user: models.User = Depends(dependency.get_current_user),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    parties = crud.party.get_multiple_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    party_schemas = [schemas.PartyWithMe.from_orm(party) for party in parties]
    return party_schemas


@router.get("/me/{party_id}", response_model=schemas.PartyWithMe)
def read_my_party(
        *,
        db: Session = Depends(dependency.get_db),
        current_user: models.User = Depends(dependency.get_current_user),
        party_id: int,
) -> Any:
    party = crud.party.get_by_id_with_user(db=db, party_id=party_id, user_id=current_user.id)
    return schemas.PartyWithMe.from_orm(party)


# TODO : Should Super-User & The Party user only. (After setting UserStatus model)
@router.get("/{party_id}", response_model=schemas.Party)
def read_party_by_id(
        party_id: int,
        db: Session = Depends(dependency.get_db),
) -> Any:
    party = crud.party.get(db, id=party_id)
    if party is None:
        raise HTTPException(
            status_code=400, detail="Party ot Found"
        )
    return party


# TODO : Should Super-User & The Party user only. (After setting UserStatus model)
@router.get("/party-with-users/{party_id}", response_model=schemas.PartyWithPartyUser)
def read_party_with_users(
        party_id: int,
        db: Session = Depends(dependency.get_db),
) -> Any:
    db_obj = crud.party.get_by_id_with_users(db, id=party_id)
    return schemas.PartyWithPartyUser.from_orm(db_obj)


@router.get("/code/{party_code}", response_model=schemas.Party)
def read_party_by_code(
        party_code: str,
        db: Session = Depends(dependency.get_db),
) -> Any:
    party = crud.party.get_by_code(db, code=party_code)
    if party is None:
        raise HTTPException(status_code=400, detail="Party Not Found")
    return party


@router.post("/", response_model=schemas.Party)
def create_party(
        *,
        db: Session = Depends(dependency.get_db),
        party_in: schemas.PartyCreate,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    try:
        party = crud.party.create_with_leader(db, obj_in=party_in, leader_id=current_user.id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is the duplicated value")
    return party


@router.put("/{party_id}", response_model=schemas.PartyUpdate)
def update_party(
        *,
        db: Session = Depends(dependency.get_db),
        party_id: int,
        party_update_in: schemas.PartyUpdate,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    try:
        db_obj = crud.party.get(db=db, id=party_id)
        party = crud.party.update(db=db, db_obj=db_obj, obj_in=party_update_in)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="There is the duplicatted value")

    if party is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is No party")

    party_user = crud.party_user.get_by_user_id(db=db, party_id=party_id, user_id=current_user.id)
    if party_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if not party_user.is_manager:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return party


# TODO Should deleted only by leader
# TODO Don't remove just change is_active field
@router.delete("/{party_id}", response_model=schemas.Party)
def delete_party(
        *,
        db: Session = Depends(dependency.get_db),
        party_id: int,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    party = crud.party.remove(db, id=party_id)
    return party


"""
Party User API
"""


@router.post("/join", response_model=schemas.PartyUser)
def join_party(
        *,
        db: Session = Depends(dependency.get_db),
        party_user_in: schemas.PartyUserCreate,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    party_user = crud.party_user.create_party_user(db, obj_in=party_user_in, user_id=int(current_user.id))
    return party_user


@router.delete("/withdraw/{party_id}", response_model=schemas.PartyUser)
def withdraw_party_me(
        *,
        db: Session = Depends(dependency.get_db),
        party_id: int,
        current_user: models.User = Depends(dependency.get_current_user),
) -> Any:
    party_user = crud.party_user.delete(db, party_id=party_id, user_id=int(current_user.id))
    return party_user
