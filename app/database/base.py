from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.database.connection import get_db


class Base(DeclarativeBase):
    pass


MyDb = Annotated[AsyncSession, Depends(get_db)]