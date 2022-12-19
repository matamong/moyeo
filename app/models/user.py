from sqlalchemy import Boolean, Column, BigInteger, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, unique=True, index=True, nullable=False )
    is_active = Column(Boolean(), default=True, nullable=False)
