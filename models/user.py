# models/user.py
from sqlalchemy import Column,String,Integer,DateTime,func
from sqlalchemy.orm import relationship
from database.connect import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True,nullable=False)
    username = Column(String,nullable=False, unique=True)
    github_username = Column(String,nullable=True)
    email = Column(String,nullable=False, unique=True)
    hashed_password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    activities = relationship("GitHubActivity", back_populates="user")
