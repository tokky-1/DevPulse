from fastapi import FastAPI
from routes.auth import router
from routes.github import activity_router
from models.user import User
from models.github_activity import  GitHubActivity
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Jobs.sync_job import sync_all_users
from routes.health import healthrouter
from error.exception import UserNotFoundException,GitHubAPIException,SyncException
from error.error_handler import user_not_found_handler,github_api_exception_handler,sync_exception_handler
from core.logging_config import setup_logging
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    scheduler = AsyncIOScheduler()    
    scheduler.add_job(sync_all_users, 'interval', hours=6)
    scheduler.start()
    logger.info("APScheduler started.")   
    try:
        yield
    finally:       
        scheduler.shutdown()
        logger.info("APScheduler shut down.")

app = FastAPI(
    title="DevPulse",
    description= "A Developer Activity Tracker API , a backend service that tracks a developer's coding activity by pulling from public APIs (GitHub), stores and analyzes the data, and serves insights through a clean REST API.",
    version="1.0.0",
    contact={"name":"Ayo-Ajayi Oluwatokiloba","email":"tokkyayoajayi@gmail.com"},
    lifespan=lifespan)

app.include_router(healthrouter,tags =["Health"] )
app.include_router(router,tags =["Users"] )
app.include_router(activity_router,tags =["Github"] )
app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(GitHubAPIException, github_api_exception_handler)
app.add_exception_handler(SyncException, sync_exception_handler)