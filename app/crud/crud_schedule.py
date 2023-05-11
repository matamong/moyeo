from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models import Party
from app.models.party import PartyUser
from app.models.schedule import VoteSchedule, VoteParticipant
from app.schemas.schedule import VoteScheduleCreate, VoteScheduleUpdate, VoteParticipantCreate, VoteParticipantUpdate, \
    VoteScheduleWithParticipants


class CRUDVoteSchedule(CRUDBase[VoteSchedule, VoteScheduleCreate, VoteScheduleUpdate]):
    def get_by_id_with_users(self, db: Session, *, id: int) -> Optional[VoteScheduleWithParticipants]:
        vote_schedule = (
            db.query(VoteSchedule)
            .options(joinedload(VoteSchedule.vote_participant_set)
                     .joinedload(VoteParticipant.party_user))
            .filter(VoteSchedule.id == id)
            .first()
        )
        return vote_schedule


class CRUDVoteParticipant(CRUDBase[VoteParticipant, VoteParticipantCreate, VoteParticipantUpdate]):
    pass


vote_schedule = CRUDVoteSchedule(VoteSchedule)
vote_participant = CRUDVoteParticipant(VoteParticipant)
