from database.connect import SessionLocal
from repositories.user_repository import get_all_user
from services.activity_service import sync_github_activity

async def sync_all_users():
    db = SessionLocal()
    try:
        users = get_all_user(db)
        for user in users:
           await  sync_github_activity(user.github_username,user.id,db)
    finally:
        db.close()
        