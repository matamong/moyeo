from sqlalchemy.orm import Session

from app import crud
from app.schemas.party import PartyCreate, PartyUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_party(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    user = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)

    assert party.name == name
    assert party.desc == desc
    assert party.img_path == img_path
    assert party.leader_id == user.id


# def test_get_party(db: Session) -> None:
#     pass