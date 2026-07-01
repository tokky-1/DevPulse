from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database.connect import get_db
from sqlalchemy.orm import Session 

healthrouter = APIRouter(prefix="/health")
 
@healthrouter.get("",summary="Liveness Check",
    description="Verifies that the DevPulse application instance is up, running, and capable of responding to basic HTTP requests."
)
def health_check ():
    return JSONResponse (
        content={"status": "ok", "message": "DevPulse is running"},
        status_code=200
    )
   
@healthrouter.get("/ready",
                  summary="Readiness Check",
                  description="Evaluates the application's readiness to handle incoming traffic by validating its connection to the underlying database.")
def ready_check ( db: Session = Depends(get_db) ):
    try:
        db.execute(text("SELECT 1"))
        return JSONResponse (
        content={"status": "ready"},
        status_code=200
    )
    except Exception as e:
         return JSONResponse (
        content={"status": "unavailable", "message": str(e)},
        status_code=503
    )