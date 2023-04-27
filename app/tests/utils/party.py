from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.models import Party, User
from app.models.party import PartyUser
from app.schemas import PartyCreate, UserCreate, PartyUserCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_party_with_random_user(db: Session) -> Party:
    user = create_random_user(db=db)
    name = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    nickname = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)
    return party


def create_random_party_with_user(db: Session, user: User, party_nickname: str) -> Party:
    user = crud.user.get(db=db, id=user.id)
    if user is None:
        user_in = UserCreate(email=user.email, nickname=user.nickname)
        user = crud.user.create(db=db, obj_in=user_in)
    name = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, desc=desc, img_path=img_path, nickname=party_nickname)
    return crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)


def create_random_party_user(db: Session, party_id: int, user: Optional[User] = None) -> PartyUser:
    if user is None:
        user = create_random_user(db=db)
    nickname = random_lower_string()
    party_user_in = PartyUserCreate(party_id=party_id, nickname=nickname)
    return crud.party_user.create_party_user(db=db, obj_in=party_user_in, user_id=user.id)
