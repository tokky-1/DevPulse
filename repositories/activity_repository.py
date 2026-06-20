from sqlalchemy.orm import Session 
from models.github_activity import GitHubActivity
from sqlalchemy import func

def save_activity(user_id,repo_name,num_commits,language,activity_date,db:Session ):
    try:
        activity_db = GitHubActivity(user_id = user_id ,repo_name = repo_name, num_commits = num_commits ,language= language , activity_date =activity_date ) 
        db.add(activity_db)
        db.commit()
        db.refresh(activity_db)
        return activity_db
    except Exception as e:
        db.rollback()
        raise e
        
def get_activities_by_user(user_id: int, db: Session):
    activites = db.query(GitHubActivity).filter(GitHubActivity.user_id == user_id).all()
    return activites

def get_activities_by_date_range(user_id: int, start_date, end_date, db: Session):
    activites = db.query(GitHubActivity).filter(GitHubActivity.user_id == user_id, GitHubActivity.activity_date >= start_date, GitHubActivity.activity_date <= end_date).all()
    return activites

def get_activity_summary(user_id: int, db: Session):
    total_commits = db.query(func.coalesce(func.sum(GitHubActivity.num_commits), 0)).filter(GitHubActivity.user_id == user_id).scalar()
    total_repos = db.query(func.count(func.distinct(GitHubActivity.repo_name))).filter(GitHubActivity.user_id == user_id).scalar()
    top = (
        db.query(GitHubActivity.language, func.sum(GitHubActivity.num_commits).label('commits'))
        .filter(GitHubActivity.user_id == user_id)
        .group_by(GitHubActivity.language)
        .order_by(func.sum(GitHubActivity.num_commits).desc())
        .first()
    )
    top_language = top[0] if top else None
    return {
    "total_commits": total_commits,
    "total_repos": total_repos,
    "top_language": top_language
        }

def get_active_dates(user_id:int, db:Session):
    active_dates = db.query(GitHubActivity.activity_date).distinct().filter(GitHubActivity.user_id == user_id).order_by(GitHubActivity.activity_date.asc()).all()
    return active_dates

