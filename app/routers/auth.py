from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.database.base import MyDb
from app.models.employees import Employees
from app.schemes.auth import RefreshToken
from app.utils.security import verify_password, create_access_token, create_refresh_token, create_new_access_token

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(db: MyDb, user_data: OAuth2PasswordRequestForm = Depends()):

    result = await db.execute(select(Employees).where(Employees.phone == user_data.username))
    employee = result.scalars().first()

    if not employee or not await verify_password(user_data.password, employee.password):
        raise HTTPException(401, "Phone or password incorrect")

    acc_token = await create_access_token(employee.id)
    ref_token = await create_refresh_token(employee.id)

    return {
        "access_token": acc_token,
        "refresh_token": ref_token,
        "token_type": "bearer",
    }


@router.post('/refresh', status_code=status.HTTP_201_CREATED)
async def refresh(token: RefreshToken, db: MyDb):
    return await create_new_access_token(token.refresh_token, db)