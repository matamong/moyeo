from typing import Dict

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.party import create_random_party_user
from app.tests.utils.schedule import create_random_vote_schedule_with_tuple
from app.tests.utils.utils import random_lower_string


def test_create_vote_schedule(db: Session, client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    vote_schedule, party, party_user = create_random_vote_schedule_with_tuple(db=db)
    title = random_lower_string()
    desc = random_lower_string()
    periods = {
        'start_datetime': ['2023.04.29 18:00'],
        'end_datetime': ['2023.05.05 18:00']
    }
    notices = {
        'warning': ['주말은 꼭 모여주세요.', '모일 때 모두 음료수를 지참해주세요.']
    }

    data = {
        'party_id': party.id,
        'title': title,
        'desc': desc,
        'periods': periods,
        'notices': notices
    }

    # Join party_user and Update to manager
    ###
    party_user_data = {
        'party_id': party.id,
        'nickname': 'ForTest',
        'is_manager': True
    }

    party_user_response = client.post(f'{settings.API_V1_STR}/party/join', headers=normal_user_token_headers, json=party_user_data)
    party_user_content = party_user_response.json()
    party_user = crud.party_user.get(db=db, id=party_user_content['id'])
    update_in = {
        'is_manager': True
    }
    updated_party_user = crud.party_user.update(db=db, db_obj=party_user, obj_in=update_in)
    ###

    response = client.post(f'{settings.API_V1_STR}/schedule', headers=normal_user_token_headers, json=data)
    content = response.json()

    assert party_user_response.status_code == 200
    assert response.status_code == 200
    assert content['title'] == data['title']
    assert content['desc'] == data['desc']
    assert content['periods']['start_datetime'][0] == data['periods']['start_datetime'][0]
    assert content['notices']['warning'][0] == data['notices']['warning'][0]
    assert 'id' in content


def test_not_create_vote_schedule_if_not_manager(
        db: Session, client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    vote_schedule, party, party_user = create_random_vote_schedule_with_tuple(db=db)
    title = random_lower_string()
    desc = random_lower_string()

    data = {
        'party_id': party.id,
        'title': title,
        'desc': desc,
    }

    response = client.post(f'{settings.API_V1_STR}/schedule', headers=normal_user_token_headers, json=data)
    content = response.json()
    assert response.status_code == 403


def test_get_vote_schedule(
        db: Session, client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    vote_schedule, party, party_user = create_random_vote_schedule_with_tuple(db=db)
    response = client.get(f'{settings.API_V1_STR}/schedule/{vote_schedule.id}', headers=normal_user_token_headers)

    assert response.status_code == 403

    # Join Party
    ###
    party_user_data = {
        'party_id': party.id,
        'nickname': 'ForTest',
        'is_manager': True
    }

    party_user_response = client.post(f'{settings.API_V1_STR}/party/join', headers=normal_user_token_headers,
                                      json=party_user_data)
    ###

    response2 = client.get(f'{settings.API_V1_STR}/schedule/{vote_schedule.id}', headers=normal_user_token_headers)
    content = response2.json()

    assert party_user_response.status_code == 200
    assert response2.status_code == 200
    assert content['id'] == vote_schedule.id
    assert content['title'] == vote_schedule.title
    assert content['desc'] == vote_schedule.desc
    assert content['periods']['start_datetime'][0] == vote_schedule.periods['start_datetime'][0]
    assert content['notices']['warning'][0] == vote_schedule.notices['warning'][0]


def test_get_vote_schedule_with_party_users(
        db: Session, client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    vote_schedule, party, party_user1 = create_random_vote_schedule_with_tuple(db=db)
    party_user2 = create_random_party_user(db=db, party_id=party.id)
    crud.party_user.create()
    party_user3 = create_random_party_user(db=db, party_id=party.id)
