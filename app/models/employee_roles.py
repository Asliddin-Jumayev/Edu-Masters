from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base


class EmployeeRole(Base):
    __tablename__ = "employee_roles"
    employee_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey("branches.id"))