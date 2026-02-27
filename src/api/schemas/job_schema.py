from pydantic import BaseModel

class JobSkillSchema(BaseModel):
    id: int
    job_title: str

    class Config:
        from_attributes = True

class JobTitleResponse(BaseModel):
    job_title: str
