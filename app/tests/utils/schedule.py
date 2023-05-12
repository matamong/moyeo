from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app import crud
from app.models import Party
from app.models.party import PartyUser
from app.models.schedule import VoteSchedule, VoteParticipant
from app.schemas import PartyUserSimple
from app.schemas.schedule import VoteScheduleCreate, VoteParticipantCreate
from app.tests.utils.party import create_random_party_with_user
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_vote_schedule(db: Session, vote_schedule_in: Optional[VoteScheduleCreate] = None) -> VoteSchedule:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()
    desc = random_lower_string()

    if not vote_schedule_in:
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

    return crud.vote_schedule.create(db=db, obj_in=vote_schedule_in)


def create_random_vote_schedule_with_tuple(
        db: Session, vote_schedule_in: Optional[VoteScheduleCreate] = None
) -> tuple[VoteSchedule, Party, PartyUser]:
    user = create_random_user(db=db)
    party = create_random_party_with_user(db=db, user=user, party_nickname='matamong')
    party2 = crud.party.get_by_id_with_users(db=db, id=party.id)
    party_user = party2.party_user_set[0]
    title = random_lower_string()
    desc = random_lower_string()

    if not vote_schedule_in:
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

    return crud.vote_schedule.create(db=db, obj_in=vote_schedule_in), party, party_user


def create_vote_participant(
        db: Session,
        vote_schedule_id: int,
        party_user_id: int
) -> VoteParticipant:
    periods = {
        'start_datetime': ['2023.04.29 18:00'],
        'end_datetime': ['2023.05.05 18:00']
    }
    obj_in = VoteParticipantCreate(
        vote_schedule_id=vote_schedule_id,
        party_user_id=party_user_id,
        periods=periods
    )
    return crud.vote_participant.create(db=db, obj_in=obj_in)
