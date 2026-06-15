import os
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import Depends, status, HTTPException
from database import get_session

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")
JWT_EXPIRE_TIME = 60
JWT_ALGORITHM = "HSA256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def hash_password(plain:str)->str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain:str, hash:str)->bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hash.encode("utf-8"))

def generate_jwt_token(user_id:int)->str:
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_TIME)
    payload = {"sub": str(user_id), "exp":expire_time}
    return jwt.encode(payload, JWT_SECRET_KEY, expire_time)

async def get_current_user(
        token:str=Depends(oauth2_scheme),
        session:AsyncSession=Depends(get_session)
)->User:
    credential_error = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="unauthorized access",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        res = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(res.get("sub"))
        if user_id is None:
            raise credential_error
    except jwt.PyJWTError:
        raise credential_error
    
    user = await session.get(User, user_id)
    if not user:
        raise credential_error
    return user