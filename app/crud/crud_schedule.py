from app.crud.base import CRUDBase
from app.models.schedule import VoteSchedule
from app.schemas.schedule import VoteScheduleCreate, VoteScheduleUpdate


class CRUDVoteSchedule(CRUDBase[VoteSchedule, VoteScheduleCreate, VoteScheduleUpdate]):
    pass


vote_schedule = CRUDVoteSchedule(VoteSchedule)
