from pydantic import BaseModel

class JobProfile(BaseModel):

    job_title: str
    job_description: str
    rating: float
    job_state: str
    sector: str
    location: str
    skills: list[str]