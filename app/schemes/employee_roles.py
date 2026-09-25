from pydantic import BaseModel


class EmployeeRolesBase(BaseModel):
    employee_id: int
    role_id: int
    branch_id: int


class EmployeeRolesCreate(EmployeeRolesBase):
    pass


class EmployeeRolesUpdate(EmployeeRolesBase):
    pass


class EmployeeRolesResponse(EmployeeRolesBase):
    pass