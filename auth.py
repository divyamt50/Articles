import os
from datetime import timedelta, datetime, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

#password hashing
def hash_password(plain:str)->str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#password verification
def password_verify(plain:str, hashed:str)->bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

# create token
def create_access_token(user_id:int)->str:
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    payload = {"sub":str(user_id), "exp":expire_time}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

async def get_current_user(
        token:str = Depends(oauth2_scheme),
        session:AsyncSession = Depends(get_session)
)->User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except jwt.PyJWTError:
        raise credentials_error
    
    user = await session.get(User, int(user_id))
    if user is None:
        raise credentials_error
    return user