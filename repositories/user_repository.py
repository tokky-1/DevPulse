from sqlalchemy.orm import Session 
from models.user import User


def create_user(username, email, github_username, hashed_password,db:Session ):
    User_db = User(username = username ,email = email,github_username = github_username,hashed_password = hashed_password) 
    
    db.add(User_db)
    db.commit()
    db.refresh(User_db)

    return User_db 

def get_user_by_username(username,db:Session):
   return db.query(User).filter(User.username == username).first()
   
def get_all_user(db:Session):
    return db.query(User).all()
