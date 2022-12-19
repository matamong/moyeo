from typing import List, Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependency

router = APIRouter()


# In Progress...
# @router.get("/", response_model=List[schemas.User])
# def read_users(
#         db: Session = Depends(dependency.get_db),
#         skip: int = 0,
#         limit: int = 100,
# ) -> Any:
#     users = crud.user.get_multi(db, skip=skip, limit=limit)
#     return users
