from schemas.auth import RegisterRequest
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import  HTTPException,status
from core.config import settings
from repositories.user_repository import create_user, get_user_by_username
hashcontext=CryptContext(schemes=["bcrypt"])

def createhash(password:str):  
    return hashcontext.hash(password)
    
def verifyhash(plainpassword:str, hashedpassword:str):
    return hashcontext.verify(plainpassword,hashedpassword)

def register_user(request:RegisterRequest,db:Session,):
    if get_user_by_username(request.username, db):
       raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="username already exists")

    hashed_password = createhash(request.password)

    return create_user(request.username,request.email,request.github_username,hashed_password,db)

def create_access_token(user_id: int):
    payload = {"sub": str(user_id)}
    expire = datetime.utcnow() + timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp":expire})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def login_user(username, password, db:Session):
    user = get_user_by_username(username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username doesn't exists")

    if not verifyhash(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    return {"access_token": create_access_token(user.id), "token_type": "bearer"}
    
    
