from typing import Optional
from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):  # when using model object is always a dictionary
    total_commits: int
    total_repos: int
    top_language: Optional[str] = Field(default=None)
    
class StreakResponse(BaseModel): 
    streak: int
    
 