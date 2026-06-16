from sqlalchemy.orm import Session 
import httpx
from fastapi import  HTTPException,status
from repositories.activity_repository import save_activity

async def  sync_github_activity(github_username: str, user_id: int, db: Session):
    url = f"https://api.github.com/users/{github_username}/events"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "FastAPI-GitHub-Syncer"  # GitHub requires a User-Agent header
    }
    
    saved_count = 0
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            events = response.json()
        except httpx.HTTPError as e:
            # Handle potential API errors gracefully (or log them depending on your setup)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)

        for event in events:
            if event.get("type") != "PushEvent":
                continue

            repo_name = event.get("repo", {}).get("name")
            
            commits = event.get("payload", {}).get("commits", [])
            num_commits = len(commits)
            
        
            created_at_str = event.get("created_at", "")
            activity_date = None
            if created_at_str:
                activity_date = created_at_str.split("T")[0]

            
            save_activity(
                db=db,
                user_id=user_id,
                repo_name=repo_name,
                num_commits=num_commits,
                activity_date=activity_date,
                language=None
            )        
            saved_count += 1
        return saved_count