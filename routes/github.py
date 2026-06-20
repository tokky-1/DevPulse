from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from services.activity_service import sync_github_activity,get_activity_summary,get_user_activity_summary,get_user_commit_streak
from database.connect import get_db
from dependencies import get_current_user
from schemas.activity import SummaryResponse,StreakResponse

activity_router = APIRouter(prefix="/Github")
  
@activity_router.post("/request_activity")
async def get_activity(github_username:str,current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return await sync_github_activity(github_username,current_user,db)

 
@activity_router.get("/summary",response_model=SummaryResponse)
def get_summary(current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_user_activity_summary(current_user,db)

@activity_router.get("/streak",response_model=StreakResponse)
def get_streak(current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_user_commit_streak(current_user,db)
