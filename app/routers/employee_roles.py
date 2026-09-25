from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database.base import MyDb
from app.models.branches import Branch
from app.models.employee_roles import EmployeeRole
from app.models.employees import Employees
from app.models.roles import Role
from app.schemes.employee_roles import EmployeeRolesCreate, EmployeeRolesResponse, EmployeeRolesUpdate
from app.utils.checked import check_ident

router = APIRouter(tags=['Employee_Roles'], prefix="/employee_roles")


# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_employee_role(employee_role: EmployeeRolesCreate, db: MyDb):
#
#     result = await db.scalar(select(EmployeeRole).
#                               where(
#         EmployeeRole.employee_id == employee_role.employee_id,
#         EmployeeRole.branch_id == employee_role.branch_id,
#         EmployeeRole.role_id == employee_role.role_id
#     ))
#
#     if result:
#         raise HTTPException(409, "Employee role already exists")
#
#
#     await check_ident(db, Employees, employee_role.employee_id)
#     await check_ident(db, Role, employee_role.role_id)
#     await check_ident(db, Branch, employee_role.branch_id)
#
#     obj = EmployeeRole(
#         **employee_role.model_dump()
#     )
#     db.add(obj)
#     await db.commit()
#     return {"msg": "Employee role created successfully"}

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_employee_role(employee_role: EmployeeRolesCreate, db: MyDb):
    # Foreign Key lar bor-yo'qligini check_ident bilan tekshiramiz
    await check_ident(db, Employees, employee_role.employee_id)
    await check_ident(db, Role, employee_role.role_id)
    await check_ident(db, Branch, employee_role.branch_id)

    # Duplikatni alohida SELECT qilmasdan, saqlashda IntegrityError orqali ushlaymiz
    try:
        obj = EmployeeRole(**employee_role.model_dump())
        db.add(obj)
        await db.commit()
        return {"Msg": "Employee role created successfully"}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Employee role already exists")


@router.get('/', response_model=list[EmployeeRolesResponse])
async def list_employee_roles(db: MyDb):

    result = await db.execute(select(EmployeeRole))

    return result.scalars().all()


@router.put('/', response_model=dict)
async def update_employee_role(employee_role: EmployeeRolesUpdate,db: MyDb):

    await check_ident(db, Employees, employee_role.employee_id)
    await check_ident(db, Role, employee_role.role_id)
    await check_ident(db, Branch, employee_role.branch_id)

    # 2. Ushbu xodimda berilgan rol bormi-yo'qligini qidiramiz
    result = await db.execute(select(EmployeeRole).where(
EmployeeRole.employee_id == employee_role.employee_id,
            EmployeeRole.role_id == employee_role.role_id
        )
    )
    role_obj = result.scalars().first()

    if not role_obj:
        raise HTTPException(404, "Not found" )

    role_obj.branch_id = employee_role.branch_id

    await db.commit()
    await db.refresh(role_obj)

    return {"Msg": "Employee role updated successfully"}


@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_employee_role(employee_id: int, role_id: int, db: MyDb):

    result = await db.execute(select(EmployeeRole).where(
            EmployeeRole.employee_id == employee_id,
            EmployeeRole.role_id == role_id
        )
    )
    role_obj = result.scalars().first()

    if not role_obj:
        raise HTTPException(404, "Not found" )

    await db.delete(role_obj)
    await db.commit()

    return {"Msg": "Employee role deleted successfully"}