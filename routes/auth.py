from fastapi import APIRouter,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from services.auth_service import register_user,login_user
from database.connect import get_db
from dependencies import get_current_user
from schemas.auth import TokenResponse,RegisterRequest

router = APIRouter(prefix="/User")
  
@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(request:RegisterRequest ,db:Session = Depends(get_db)):
    return register_user(request, db)

@router.post("/login",response_model=TokenResponse)
def login (form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    return login_user (form_data.username, form_data.password,db=db)
  
@router.get("/me")
def get_user (current_user:int = Depends(get_current_user)):
    return current_user
   