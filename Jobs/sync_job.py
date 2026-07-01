from database.connect import SessionLocal
from repositories.user_repository import get_all_user
from services.activity_service import sync_github_activity
from error.exception import GitHubAPIException
import logging

logger = logging.getLogger(__name__)

async def sync_all_users():
    db = SessionLocal()
    try:
        users = get_all_user(db)
        for user in users:
            try:
                await sync_github_activity(user.github_username, user.id, db)
            except GitHubAPIException as e:
                logger.error(f"Sync failed for user {user.github_username}: {str(e)}")
                continue 
    finally:
        db.close()