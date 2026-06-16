from sqlalchemy.orm import Session 
from models.github_activity import GitHubActivity


def save_activity(user_id,repo_name,num_commits,language,activity_date,db:Session ):
    activity_db = GitHubActivity(user_id = user_id ,repo_name = repo_name, num_commits = num_commits ,language= language , activity_date =activity_date ) 
    
    db.add(activity_db)
    db.commit()
    db.refresh(activity_db)

    return activity_db 
  
