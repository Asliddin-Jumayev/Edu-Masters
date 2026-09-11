from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from app.database.base import Base


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    name = Column(String(60), nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True) # soft delete (xavfsiz ochirish)
