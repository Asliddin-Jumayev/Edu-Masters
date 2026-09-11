from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime
from app.database.base import Base


class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    city = Column(String(60), nullable=False)
    is_active = Column(Boolean, default=True)
    opened_at = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))






