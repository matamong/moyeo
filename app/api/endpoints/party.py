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


@router.get("/me", response_model=List[schemas.Party])
def read_my_parties(
        *,
        db: Session = Depends(dependency.get_db),
        current_user: models.User = Depends(dependency.get_current_user),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    parties = crud.party.get_multiple_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return parties


# TODO : Should Super-User & The Party user only. (After setting UserStatus model)
@router.get("/{party_id}", response_model=schemas.Party)
def read_party_by_id(
        party_id: int,
        db: Session = Depends(dependency.get_db),
) -> Any:
    party = crud.party.get(db, id=party_id)
    if party is None:
        raise  HTTPException(
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
    party = schemas.PartyWithPartyUser(
        id=db_obj.id,
        name=db_obj.name,
        desc=db_obj.desc,
        img_path=db_obj.img_path,
        leader_id=db_obj.leader_id,
        is_private=db_obj.is_private,
        party_user_set=[
            schemas.PartyUser(id=c.id, nickname=c.nickname, is_manager=c.is_manager) for c in db_obj.party_user_set
        ]
    )
    return party


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
    party = crud.party.create_with_leader(db, obj_in=party_in, leader_id=current_user.id)
    return party

# TODO Should deleted only by leader
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
