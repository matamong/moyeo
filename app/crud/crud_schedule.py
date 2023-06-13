from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models import Party
from app.models.party import PartyUser
from app.models.schedule import VoteSchedule, VoteParticipant
from app.schemas.schedule import VoteScheduleCreate, VoteScheduleUpdate, VoteParticipantCreate, VoteParticipantUpdate, \
    VoteScheduleWithParticipants


class CRUDVoteSchedule(CRUDBase[VoteSchedule, VoteScheduleCreate, VoteScheduleUpdate]):
    def get_multiple_by_party_id(
            self, db: Session, *, party_id: int, skip: int = 0, limit: int = 100
    ) -> List[VoteSchedule]:
        vote_schedules = (db.query(self.model)
                   .join(Party)
                   .filter(Party.id == party_id)
                   .offset(skip)
                   .limit(limit)
                   .all())

        return vote_schedules or []

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
