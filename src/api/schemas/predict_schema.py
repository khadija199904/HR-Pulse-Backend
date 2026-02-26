from pydantic import BaseModel  , Field
from typing import List

class JobProfile(BaseModel):

    job_title: str = "Développeur Python"
    job_description: str = "Description du poste à compléter..."
    rating: float = 0.0
    job_state: str = "Remote"
    sector: str = "IT"
    location: str = "Paris, France"
    skills: List[str] = Field(default_factory=lambda: ["Python", "FastAPI"])