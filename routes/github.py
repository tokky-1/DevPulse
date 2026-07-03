from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from services.activity_service import get_user_activity_summary,get_user_commit_streak,sync_github_activity_for_user
from database.connect import get_db
from dependencies import get_current_user
from schemas.activity import SummaryResponse,StreakResponse

activity_router = APIRouter(prefix="/Github")
  
@activity_router.post("/request_activity",
    summary="Sync GitHub Push Events",
    description=(
        "Fetches the public event history for a given GitHub username from the GitHub REST API. "
        "It filters out everything except 'PushEvent' activities, extracts the repository name, "
        "calculates the number of commits per push, and persists this activity data into the database "
        "for the authenticated user."
    ))
async def get_activity(current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return await sync_github_activity_for_user(current_user,db)

 
@activity_router.get("/summary",
    response_model=SummaryResponse,
    summary="Get Activity Summary",
    description=(
        "Retrieves a aggregated summary of the authenticated user's tracked GitHub commit history and activity "
        "metrics stored within the database."
    ))
def get_summary(current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_user_activity_summary(current_user,db)

@activity_router.get("/streak",
    response_model=StreakResponse,
    summary="Calculate Commit Streak",
    description=(
        "Analyzes the user's active database records to compute their consecutive daily commit streak. "
        "It verifies if the most recent activity happened either today or yesterday to ensure the streak is still live, "
        "and then counts backwards sequentially across unique days to return the total streak count."
    ))
def get_streak(current_user:int = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_user_commit_streak(current_user,db)
