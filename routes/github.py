from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from services.github_service import sync_github_activity
from database.connect import get_db
from dependencies import get_current_user

activity_router = APIRouter(prefix="/Github")
  
@activity_router.post("/request_activity")
async def get_activity(github_username:str,current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return await sync_github_activity(github_username,current_user,db)