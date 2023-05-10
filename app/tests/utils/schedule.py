from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.models.schedule import VoteSchedule
from app.schemas.schedule import VoteScheduleCreate
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
