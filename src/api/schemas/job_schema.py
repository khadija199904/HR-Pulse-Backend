from pydantic import BaseModel
from typing import List, Optional

class JobSkillSchema(BaseModel):
    id: int
    job_title: str
    skills_extracted: str

    class Config:
        from_attributes = True

class JobTitleResponse(BaseModel):
    job_title: str
