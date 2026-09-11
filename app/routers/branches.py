from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from app.database.base import MyDb
from app.models.branches import Branch
from app.schemas.branches import BranchCreate, BranchResponse


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