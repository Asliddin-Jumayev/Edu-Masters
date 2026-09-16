from datetime import datetime, timezone
from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.employees import Employees
from app.schemes.employees import EmployeesCreate, EmployeesResponse, EmployeesUpdate
from app.utils.checked import check_ident
from app.utils.security import get_password_hash

router = APIRouter(tags=['Employees'], prefix="/employees")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeesCreate, db: MyDb):

    await check_ident(db, Branch, employee.branch_id)

    result = await db.execute(select(Employees).where(Employees.phone == employee.phone))
    user = result.scalars().first()

    if user:
        raise HTTPException(409, "Employee already exists")

    obj = Employees(
        **employee.model_dump(exclude={"password"}),
        password = await get_password_hash(employee.password)
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Employees created successfully"}


@router.get('/', response_model=list[EmployeesResponse])
async def list_employees(db: MyDb, is_active: bool = True):

    result = await db.execute(select(Employees).where(Employees.is_active == is_active))

    return result.scalars().all()


@router.put('/{employee_id}')
async def update_employee(employee_id: int, employee: EmployeesUpdate, db: MyDb):

    employee_result = await check_ident(db, Employees, employee_id)

    if not employee_result.is_active:
        raise HTTPException(400, "Employee does not active")


    await check_ident(db, Branch, employee.branch_id)

    result = await db.execute(
        select(Employees).where(Employees.phone == employee.phone))
    user = result.scalars().first()

    if user:
        raise HTTPException(409, "Employee already exists")

    update_data = employee.model_dump(exclude_unset=True)

    update_data["password"] = await get_password_hash(update_data["password"])

    for field, value in update_data.items():
        setattr(employee_result, field, value)

    await db.commit()
    return {"msg": "Employee updated successfully"}


@router.patch('/{employee_id}')
async def toggle_employee_status(employee_id: int, db: MyDb):
    employee_result = await check_ident(db, Employees, employee_id)
    employee_result.is_active = True
    employee_result.fired_at = None
    await db.commit()
    return {"msg": "Employee status updated successfully"}


@router.delete('/{employee_id}')
async def delete_employee(employee_id: int, db: MyDb):

    employee = await check_ident(db, Employees, employee_id)

    # soft delete
    employee.is_active = False
    employee.fired_at = datetime.now(timezone.utc)

    await db.commit()
    return {"msg": "Employee soft delete"}