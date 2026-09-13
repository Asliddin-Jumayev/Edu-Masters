from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, \
    ForeignKey
from app.database.base import Base


class Employees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    photo_url = Column(String(255), nullable=False)
    position = Column(String(80), nullable=False)
    hired_at = Column(Date, nullable=False)
    fired_at = Column(Date, nullable=True, default=None)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))