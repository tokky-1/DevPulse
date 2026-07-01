from fastapi import Request
from fastapi.responses import JSONResponse
from error.exception import UserNotFoundException,GitHubAPIException,SyncException

async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": exc.message}
    )
async def github_api_exception_handler(request: Request, exc:GitHubAPIException):
    return JSONResponse(
        status_code=502,
        content={"error": exc.message}
    )
async def sync_exception_handler(request: Request, exc: SyncException):
    return JSONResponse(
        status_code=500,
        content={"error": exc.message}
    )