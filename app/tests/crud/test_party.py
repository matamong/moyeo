from sqlalchemy.orm import Session

from app import crud
from app.schemas.party import PartyCreate, PartyUpdate, PartyUserCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


# TODO create_random_party fixture and etc(scope=function).
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
    assert party.code is not None
    assert party.access_code is not None
    assert party.created_at is not None
    assert party.updated_at is not None


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


def test_create_party_with_leader(db: Session) -> None:
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


def test_update_party(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    user = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)

    desc2 = random_lower_string()
    party_update = PartyUpdate(desc=desc2)
    party2 = crud.party.update(db=db, db_obj=party, obj_in=party_update)

    assert party.name == name
    assert party.img_path == img_path
    assert party.leader_id == user.id

    assert party2.id == party2.id
    assert party2.name == party2.name
    assert party2.img_path == party2.img_path

    assert party2.desc == desc2


def test_delete_party(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    user = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=user.id)

    party2 = crud.party.remove(db=db, id=party.id)
    party3 = crud.party.get(db=db, id=party.id)

    assert party3 is None
    assert party2.id == party.id
    assert party2.name == name
    assert party2.desc == desc
    assert party2.leader_id == user.id


def test_get_by_id_with_users(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    leader = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=leader.id)

    user1 = create_random_user(db=db)
    party_user_in = PartyUserCreate(party_id=party.id, nickname=user1.nickname)
    party_user2 = crud.party_user.create_party_user(db=db, obj_in=party_user_in, user_id=user1.id)

    user2 = create_random_user(db=db)
    party_user_in2 = PartyUserCreate(party_id=party.id, nickname=user2.nickname)
    party_user3 = crud.party_user.create_party_user(db=db, obj_in=party_user_in2, user_id=user2.id)

    party_with_users = crud.party.get_by_id_with_users(db=db, id=party.id)
    user_set = party_with_users.party_user_set

    assert user_set != []
    assert len(user_set) == 3
    assert party.id == party_user2.party_id
    assert user_set[1].id == party_user2.id
    assert user_set[2].id == party_user3.id


def test_get_by_code(db: Session) -> None:
    name = random_lower_string()
    nickname = random_lower_string()
    desc = random_lower_string()
    img_path = random_lower_string()
    party_in = PartyCreate(name=name, nickname=nickname, desc=desc, img_path=img_path)
    leader = create_random_user(db=db)
    party = crud.party.create_with_leader(db=db, obj_in=party_in, leader_id=leader.id)

    db_obj = crud.party.get_by_code(db=db, code=party.code)

    assert party.id == db_obj.id
    assert party.name == db_obj.name
