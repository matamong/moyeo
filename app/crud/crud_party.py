from typing import Optional, List, Any
import uuid

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, contains_eager, subqueryload
from starlette import status

from app.crud.base import CRUDBase
from app.models.party import Party, PartyUser
from app.schemas.party import PartyCreate, PartyWithPartyUser, PartyUserCreate, PartyUpdate, PartyUserUpdate
from app.utils import generate_code


class CRUDParty(CRUDBase[Party, PartyCreate, PartyUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Party]:
        return db.query(Party).filter(Party.code == code).first()

    # TODO Move HTTPException to api level.
    def get_by_id_with_users(self, db: Session, *, id: int) -> Optional[PartyWithPartyUser]:
        party = (
            db.query(Party)
            .options(joinedload(Party.party_user_set))
            .filter(Party.id == id).first()
        )
        if party is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")
        return party

    # https://fastapi.tiangolo.com/tutorial/body-nested-models/

    def get_multiple_by_user(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Party]:
        parties = (
            db.query(self.model)
            .join(self.model.party_user_set)
            .filter(and_(PartyUser.user_id == user_id, PartyUser.party_id == Party.id))
            .options(contains_eager(self.model.party_user_set))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return parties or []

    def create_with_leader(self, db: Session, *, obj_in: PartyCreate, leader_id: int) -> Party:
        # Tip!
        # Since SQLAlchemy handles transactions through Session(by default),
        # you do not need to handle transactions like Django's `@transaction.atomic`.
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["code"] = uuid.uuid4()
        obj_in_data["leader_id"] = leader_id
        obj_in_data["access_code"] = generate_code()
        nickname = obj_in_data.pop("nickname")

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()

        party_user = PartyUser(user_id=leader_id, party_id=db_obj.id, nickname=nickname, is_manager=True)
        db.add(party_user)

        db.commit()
        db.refresh(db_obj)
        return db_obj


# TODO PartyUserCreate 랑 user_id 왜 분리됐찌 넣기
class CRUDPartyUser(CRUDBase[PartyUser, PartyUserCreate, PartyUserUpdate]):
    def get_by_user_id(self, db: Session, party_id: int, user_id: int) -> PartyUser:
        return db.query(PartyUser).filter_by(party_id=party_id, user_id=user_id).first()

    def create_party_user(self, db: Session, *, obj_in: PartyUserCreate, user_id: int) -> PartyUser:
        # private일 때 code 필요한데 obj_in에 어케 옵셔널로 넣다뺐다하지...
        obj_in_data = jsonable_encoder(obj_in)
        party_code = obj_in_data.pop("party_code")
        obj_in_data["user_id"] = user_id

        party = db.query(Party).filter(Party.id == obj_in.party_id).first()

        if party is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Party not found")

        if db.query(self.model).filter_by(nickname=obj_in_data["nickname"]).first() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nickname is duplicated.")

        if party.is_private:
            if party_code != party.code:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Party Code.")

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_by_multiple_filter(self, db: Session, *, filter_data: dict[str, Any]) -> Optional[PartyUser]:
        query = db.query(PartyUser)
        conditions = [getattr(PartyUser, k) == v for k, v in filter_data.items()]
        result = query.filter(and_(*conditions)).first()
        return result

    def delete(self, db: Session, *, party_id: int, user_id: int) -> PartyUser:
        party_user = db.query(PartyUser).filter_by(party_id=party_id, user_id=user_id).first()
        if party_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no party or user.")
        print(party_user)
        db.delete(party_user)
        db.commit()
        return party_user


party = CRUDParty(Party)
party_user = CRUDPartyUser(PartyUser)
