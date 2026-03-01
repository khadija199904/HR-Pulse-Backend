from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from src.api.crud import jobs_crud
from src.api.schemas.job_schema import JobSkillSchema


router = APIRouter(prefix="/jobs", tags=["Jobs"])



@router.get("/titles", response_model=list[str])
def get_job_titles(db: Session = Depends(get_db)):
    results = jobs_crud.liste_jobs(db)
    return [r[0] for r in results]



@router.get("/search", response_model=list[JobSkillSchema])
def search_jobs(skills: str, db: Session = Depends(get_db)):
    return jobs_crud.search_jobs_by_skills(db, skills)


