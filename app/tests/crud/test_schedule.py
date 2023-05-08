from sqlalchemy.orm import Session

from app import crud
from app.schemas.schedule import VoteScheduleCreate, VoteScheduleUpdate
from app.tests.utils.party import create_random_party_with_user
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_vote_schedule(db: Session) -> None:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()
    desc = random_lower_string()

    periods = {
        'start_datetime': ['2023.04.29 18:00'],
        'end_datetime': ['2023.05.05 18:00']
    }


    # TODO 포맷 확실히 잡기 (프론트에서 어떻게 정제할지)
    notices = {
        'warning': ['주말은 꼭 모여주세요.', '모일 때 모두 음료수를 지참해주세요.']
    }

    vote_schedule_in = VoteScheduleCreate(
        party_id=party.id,
        manager_id=party_user.id,
        title=title,
        desc=desc,
        periods=periods,
        notices=notices
    )

    vote_schedule = crud.vote_schedule.create(db=db, obj_in=vote_schedule_in)
    assert vote_schedule.party_id == party.id
    assert vote_schedule.manager_id == party_user.id
    assert vote_schedule.title == title
    assert vote_schedule.desc == desc
    assert vote_schedule.periods['start_datetime'][0] == periods['start_datetime'][0]
    assert vote_schedule.periods['end_datetime'][0] == periods['end_datetime'][0]
    assert vote_schedule.notices['warning'][0] == notices['warning'][0]


def test_create_vote_schedule_with_multiple_periods_and_notices(db: Session) -> None:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()
    desc = random_lower_string()

    periods = {
        'start_datetime': ['2023.04.29 18:00', '2023.05.29 18:00', '2023.06.29 18:00'],
        'end_datetime': ['2023.05.05 18:00', '2023.06.05 18:00', '2023.07.05 18:00']
    }


    # TODO 포맷 확실히 잡기 (프론트에서 어떻게 정제할지)
    notices = {
        'warning': ['주말은 꼭 모여주세요.', '모일 때 모두 음료수를 지참해주세요.'],
        'plain': ['마타몽은 최고닷', '마타몽은 바보닷'],
    }

    vote_schedule_in = VoteScheduleCreate(
        party_id=party.id,
        manager_id=party_user.id,
        title=title,
        desc=desc,
        periods=periods,
        notices=notices
    )

    vote_schedule = crud.vote_schedule.create(db=db, obj_in=vote_schedule_in)
    assert vote_schedule.party_id == party.id
    assert vote_schedule.manager_id == party_user.id
    assert vote_schedule.title == title
    assert vote_schedule.desc == desc
    assert vote_schedule.periods['start_datetime'][0] == periods['start_datetime'][0]
    assert vote_schedule.periods['start_datetime'][1] == periods['start_datetime'][1]

    assert vote_schedule.periods['start_datetime'][2] == periods['start_datetime'][2]

    assert vote_schedule.periods['end_datetime'][0] == periods['end_datetime'][0]

    assert vote_schedule.periods['end_datetime'][1] == periods['end_datetime'][1]

    assert vote_schedule.periods['end_datetime'][2] == periods['end_datetime'][2]

    assert vote_schedule.notices['warning'][0] == notices['warning'][0]
    assert vote_schedule.notices['warning'][1] == notices['warning'][1]
    assert vote_schedule.notices['plain'][0] == notices['plain'][0]
    assert vote_schedule.notices['plain'][1] == notices['plain'][1]


def test_get_by_id(db: Session) -> None:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()

    vote_schedule_in = VoteScheduleCreate(
        party_id=party.id,
        manager_id=party_user.id,
        title=title,
    )
    vote_schedule = crud.vote_schedule.create(db=db, obj_in=vote_schedule_in)

    db_obj = crud.vote_schedule.get(db=db, id=vote_schedule.id)

    assert vote_schedule.id == db_obj.id
    assert vote_schedule.party_id == party.id


def test_update_vote_schedule1(db: Session) -> None:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()
    desc = random_lower_string()

    periods = {
        'start_datetime': ['2023.04.29 18:00'],
        'end_datetime': ['2023.05.05 18:00']
    }

    # TODO 포맷 확실히 잡기 (프론트에서 어떻게 정제할지)
    notices = {
        'warning': ['주말은 꼭 모여주세요.', '모일 때 모두 음료수를 지참해주세요.']
    }

    vote_schedule_in = VoteScheduleCreate(
        party_id=party.id,
        manager_id=party_user.id,
        title=title,
        desc=desc,
        periods=periods,
        notices=notices
    )

    updated_title = random_lower_string()
    updated_desc = random_lower_string()
    # new_manager = create_random_user(db=db) TODO VoteParticipant create
    updated_periods = {
        'start_datetime': ['2023.05.29 16:00', '2023.06.29 16:00'],
        'end_datetime': ['2023.06.05 18:00', '2023.07.05 18:00'],
    }

    updated_notices = {
        'warning': ['평일은 꼭 모여주세요.', '모일 때 모두 엄청난 것을 지참해주세요.', '수정된 모임입니다.'],
        'plain': ['matamong은 최고닷', 'matamong은 바보닷'],
    }
    updated_in = VoteScheduleUpdate(
        title=updated_title,
        desc=updated_desc,
        periods=updated_periods,
        notices=updated_notices
    )

    vote_schedule = crud.vote_schedule.create(db=db, obj_in=vote_schedule_in)
    vote_schedule2 = crud.vote_schedule.update(
        db=db,
        db_obj=vote_schedule,
        obj_in=updated_in
    )

    assert vote_schedule2.desc == updated_desc
    assert vote_schedule2.title == updated_title
    assert len(vote_schedule2.periods['start_datetime']) == len(updated_periods['start_datetime'])
    assert len(vote_schedule2.notices['warning']) == len(updated_notices['warning'])

