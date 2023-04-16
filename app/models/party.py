from sqlalchemy import Column, BigInteger, String, DateTime, func, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship, backref

from app.db.base_class import Base


# TODO Party 용 status 만들기(개방, 비공개(코드 필요), 폐쇄)
# https://github.com/tiangolo/fastapi/issues/2194
class Party(Base):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String(100))
    img_path = Column(String)
    leader_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    leader = relationship("User", backref=backref("leading_party_set"))
    code = Column(String, unique=True)  # UUID for Party itself (Mainly used for shared links.)
    access_code = Column(String, unique=True)   # UUID to access shared links without logging in.
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# TODO Party User 용 대기유저, 일반유저, 매니저 status 테이블 만들고 블랙리스트 테이블도 만들자.
# TODO 프로필 img
class PartyUser(Base):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    user = relationship("User", backref="party_user_set")
    party_id = Column(Integer, ForeignKey("party.id", ondelete="CASCADE", onupdate="CASCADE"))
    party = relationship("Party", backref="party_user_set")
    is_manager = Column(Boolean, default=False)
    nickname = Column(String(20), unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
