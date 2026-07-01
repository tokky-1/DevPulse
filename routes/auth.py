from fastapi import APIRouter,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from services.auth_service import register_user,login_user
from database.connect import get_db
from dependencies import get_current_user
from schemas.auth import TokenResponse,RegisterRequest

router = APIRouter(prefix="/User")
  
@router.post("/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a New User",
    description=(
        "Creates a new user profile in the system. "
        "It validates that the username is unique, securely hashes the plain-text password "
        "using bcrypt, and saves the user credentials (username, email, and GitHub username) to the database."
    )
)
async def register(request:RegisterRequest ,db:Session = Depends(get_db)):
    return register_user(request, db)

@router.post("/login",
    response_model=TokenResponse,
    summary="User Login / Token Generation",
    description=(
        "Authenticates a user using standard OAuth2 password credentials (username and password). "
        "If the credentials are valid, it issues a signed JSON Web Token (JWT) access token "
        "and sets the token type to 'bearer'."
    ))
def login (form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    return login_user (form_data.username, form_data.password,db=db)
  
@router.get("/me",
    summary="Get Current User Profile",
    description=(
        "Retrieves the profile information or ID of the currently authenticated user. "
        "This endpoint is protected and requires a valid OAuth2 Bearer access token "
        "passed in the Authorization header."
    ))
def get_user (current_user:int = Depends(get_current_user)):
    return current_user
   