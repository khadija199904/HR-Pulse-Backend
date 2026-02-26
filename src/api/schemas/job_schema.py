from pydantic import BaseModel
from typing import List, Optional

class JobSkillSchema(BaseModel):
  
    job_title: str
   

    class Config:
        from_attributes = True

class JobTitleResponse(BaseModel):
    job_title: str
