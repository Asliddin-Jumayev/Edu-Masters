from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.schemes.branches import BranchCreate, BranchResponse, BranchUpdate
from app.utils.checked import check_ident


router = APIRouter(tags=['Branches'], prefix="/branches")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_branch(branch: BranchCreate, db: MyDb):
    result = await db.execute(select(Branch).where(Branch.code == branch.code))
    branch_code = result.scalars().first()

    if branch_code:
        raise HTTPException(409, "Branch already exists")


    obj = Branch(
        **branch.model_dump()
    )
    db.add(obj)
    await db.commit()
    return {"msg": "Branch created successfully"}


@router.get('/', response_model=list[BranchResponse])
async def list_branches(db: MyDb, name: str = None):
    result = await db.execute(select(Branch))

    if name:
        result = await db.execute(select(Branch).where(Branch.name.ilike(f"%{name}")))

    return result.scalars().all()


@router.put('/{branch_id}')
async def update_branch(branch_id: int, branch_data: BranchUpdate, db: MyDb):
    branch = await check_ident(db, Branch, branch_id)

    if branch.code != branch_data.code:
        existing = await db.execute(select(Branch).where(Branch.code == branch_data.code))
        if existing.scalars().first():
            raise HTTPException(409, "Branch with this code already exists")

    branch.name = branch_data.name
    branch.code = branch_data.code
    branch.address = branch_data.address
    branch.phone = branch_data.phone
    branch.city = branch_data.city
    branch.opened_at = branch_data.opened_at

    await db.commit()
    await db.refresh(branch)
    return {"Msg": "Branch edited successfully"}


@router.delete('/{branch_id}')
async def delete_branch(branch_id: int, db: MyDb):
    branch = await check_ident(db, Branch, branch_id)

    await db.delete(branch)
    await db.commit()
    return {"msg": "Branch deleted successfully"}
