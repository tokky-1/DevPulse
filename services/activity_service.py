from sqlalchemy.orm import Session 
import httpx
from datetime import timedelta, date
from repositories.activity_repository import save_activity,get_activity_summary,get_active_dates
from error.exception import GitHubAPIException
import logging
from core.config import settings


logger = logging.getLogger(__name__)

async def sync_github_activity(github_username: str, user_id: int, db: Session):
    url = f"https://api.github.com/users/{github_username}/events"
    headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "FastAPI-GitHub-Syncer",
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}
    logger.info("fetching github activity",extra={"user_id": user_id, "username": github_username})

    saved_count = 0
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            events = response.json()
        except httpx.HTTPError as e:
            logger.error("github activity failed" ,extra={"user_id": user_id, "username": github_username})
            raise GitHubAPIException(f"GitHub API request failed: {str(e)}")
        
        for event in events:
            if event.get("type") != "PushEvent":
                continue

            repo_name = event.get("repo", {}).get("name")
            
            commits = event.get("payload", {}).get("commits", [])
            num_commits = len(commits)
            
        
            created_at_str = event.get("created_at", "")
           
            activity_date = created_at_str.split("T")[0]
            formatted_activity_date = date.fromisoformat(activity_date)
            save_activity(
                db=db,
                user_id=user_id,
                repo_name=repo_name,
                num_commits=num_commits,
                activity_date=formatted_activity_date,
                language=None
            )        
            saved_count += 1
            
        logger.info("github activity synced" ,extra={"user_id": user_id, "username": github_username,"saved_count": saved_count})
        return saved_count
    
def get_user_activity_summary(user_id: int, db: Session):
    return  get_activity_summary(user_id, db)
    
def get_user_commit_streak(user_id: int, db: Session):
    active_dates = get_active_dates(user_id,db)
    if not active_dates:
        return {"streak": 0}
    unique_dates = sorted({d[0] for d in active_dates}, reverse=True)
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # If the latest commit isn't today or yesterday, the current streak is broken (0)
    if unique_dates[0] < yesterday:
        return {"streak": 0 }
    
    streak_count = 0
    current_check_date = unique_dates[0] # Start checking from the most recent commit
    
    # 2. calculate the streak
    for commit_date in unique_dates:
        if commit_date == current_check_date:
            streak_count += 1
            current_check_date -= timedelta(days=1)
        else:            
            break
    return {"streak": streak_count}