# models/github_activity.py
from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,func,Date
from sqlalchemy.orm import relationship
from database.connect import Base

class GitHubActivity(Base):
    __tablename__ = "github_activities"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    repo_name = Column(String,nullable=False)
    num_commits = Column(Integer,nullable=False)
    language = Column(String,nullable=True)
    activity_date = Column(Date,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="activities")



