from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy import select
from app.database.base import MyDb
from app.models.employees import Employees
from app.utils.config import settings


pwd_context = CryptContext(schemes=["argon2"])


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        "type": "access"
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



async def create_refresh_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "type": "refresh"
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



async def create_new_access_token(token: str, db) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload["type"] != "refresh":
            raise HTTPException(400, "No refresh token")


        user_id = payload["user_id"]

        result = await db.execute(select(Employees).where(Employees.id == user_id))
        user = result.scalars().first()

        if not user:
            raise HTTPException(404, "No user found")

        return {
            "new_access_token": await create_access_token(user.id)
        }
    except ExpiredSignatureError:
        raise HTTPException(401, "Token is expired")
    except JWTError:
        raise HTTPException(401, "Token invalid")


bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(db: MyDb, token = Depends(bearer)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token ichida user_id topilmadi")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token yaroqsiz yoki muddati o'tgan")

    result = await db.execute(select(Employees).where(Employees.id == user_id))
    user_data = result.scalars().first()
    if not user_data:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    return user_data