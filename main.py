from fastapi import FastAPI
from routes.auth import router
from routes.github import activity_router
from models.user import User
from models.github_activity import  GitHubActivity
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Jobs.sync_job import sync_all_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()    
    scheduler.add_job(sync_all_users, 'interval', hours=6)
    scheduler.start()
    print("APScheduler started.")    
    try:
        yield
    finally:       
        scheduler.shutdown()
        print("APScheduler shut down.")

app = FastAPI(title="DevPulse", lifespan=lifespan)

app.include_router(router,tags =["Users"] )
app.include_router(activity_router,tags =["Github"] )
