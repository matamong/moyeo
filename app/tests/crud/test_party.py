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


def test_get_party(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    user = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)
    stored_party = crud.party.get(db=db, id=party.id)

    assert stored_party
    assert party.id == stored_party.id
    assert party.name == stored_party.name
    assert party.desc == stored_party.desc
    assert party.img_path == stored_party.img_path
    assert party.leader_id == stored_party.leader_id

def test_create_party_with_user(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    user = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)

    filter_data = {"party_id": party.id, "user_id": user.id}
    stored_party_user = crud.party_user.get_by_multiple_filter(db=db, filter_data=filter_data)

    assert party.name == name
    assert party.desc == desc
    assert party.img_path == img_path
    assert party.leader_id == user.id

    assert stored_party_user.party_id == party.id
    assert stored_party_user.user_id == user.id
    assert stored_party_user.nickname == nickname
    assert stored_party_user.is_manager is True