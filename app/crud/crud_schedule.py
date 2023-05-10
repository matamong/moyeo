from app.crud.base import CRUDBase
from app.models.schedule import VoteSchedule, VoteParticipant
from app.schemas.schedule import VoteScheduleCreate, VoteScheduleUpdate, VoteParticipantCreate, VoteParticipantUpdate


class CRUDVoteSchedule(CRUDBase[VoteSchedule, VoteScheduleCreate, VoteScheduleUpdate]):
    pass


class CRUDVoteParticipant(CRUDBase[VoteParticipant, VoteParticipantCreate, VoteParticipantUpdate]):
    pass


vote_schedule = CRUDVoteSchedule(VoteSchedule)
vote_participant = CRUDVoteParticipant(VoteParticipant)
