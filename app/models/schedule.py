from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class VoteSchedule(Base):
    id = Column(BigInteger, primary_key=True)
    party_id = Column(Integer, ForeignKey("party.id", ondelete="CASCADE"))
    party = relationship("Party", backref="vote_schedule_set")
    manager_id = Column(Integer, ForeignKey("partyuser.id", ondelete="SET NULL"))
    manager = relationship("PartyUser", backref="vote_schedule_managing_set")
    title = Column(String)
    desc = Column(String, nullable=True)
    periods = Column(MutableDict.as_mutable(JSONB), nullable=True)    # null = No deadline
    notices = Column(MutableDict.as_mutable(JSONB), nullable=True)    # user customizable

    # vote_participant_set = relationship("VoteParticipant", back_populates="vote_schedule")


class VoteParticipant(Base):
    id = Column(BigInteger, primary_key=True)
    vote_schedule_id = Column(Integer, ForeignKey("voteschedule.id", ondelete="CASCADE"))
    vote_schedule = relationship("VoteSchedule", backref="vote_participant_set")
    party_user_id = Column(Integer, ForeignKey("partyuser.id", ondelete="CASCADE"))
    party_user = relationship("PartyUser", backref="vote_participant_set")
    periods = Column(MutableDict.as_mutable(JSONB))
