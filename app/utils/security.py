import os
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv
from sqlalchemy import select
from app.models.employees import Employees


load_dotenv()


pwd_context = CryptContext(schemes=["argon2"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

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

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



async def create_refresh_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "type": "refresh"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



async def create_new_access_token(token: str, db) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

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