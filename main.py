from fastapi import FastAPI
from routes.auth import router
from routes.github import activity_router
from models.user import User
from models.github_activity import  GitHubActivity

app = FastAPI(title="DevPulse")

app.include_router(router,tags =["Users"] )
app.include_router(activity_router,tags =["Github"] )
