from fastapi import APIRouter, status, Depends
from sqlalchemy import select
from app.database.base import MyDb
from app.models.roles import Role
from app.schemes.roles import RoleCreate, RoleResponse, RoleUpdate
from app.utils.checked import check_ident
from app.utils.security import get_current_user


router = APIRouter(tags=['Roles'], prefix="/roles")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, db: MyDb,
                      current_user = Depends(get_current_user)):

    obj = Role(
        **role.model_dump()
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Role created successfully"}


@router.get('/', response_model=list[RoleResponse])
async def list_roles(db: MyDb):

    result = await db.execute(select(Role))
    return result.scalars().all()


@router.put('/{role_id}')
async def update_role(role_id: int, role: RoleUpdate, db: MyDb,
                      current_user = Depends(get_current_user)):
    role_result = await check_ident(db, Role, role_id)

    role_result.code = role.code
    role_result.name = role.name
    await db.commit()
    return {"msg": "Role updated successfully"}



@router.delete('/{role_id}')
async def delete_role(role_id: int, db: MyDb):

    role = await check_ident(db, Role, role_id)

    await db.delete(role)
    await db.commit()
    return {"msg": "Role delete"}