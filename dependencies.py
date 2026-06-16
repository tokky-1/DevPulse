from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends

from core.config import settings
from jose import jwt,JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/User/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:     
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except JWTError:
            raise credentials_exception
    return user_id