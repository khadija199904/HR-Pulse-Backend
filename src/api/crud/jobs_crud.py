from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.database.models import jobskills

def liste_jobs(db):
    query = db.query(jobskills.JobSkill.job_title).distinct()
    return query.all()


def search_jobs_by_skills(db: Session, skills: str, limit: int = 20):
    skill_list = [s.strip() for s in skills.split(",")]
    
    filters = [jobskills.JobSkill.skills_extracted.contains(skill) for skill in skill_list]
    
    return db.query(jobskills.JobSkill).filter(or_(*filters)).limit(limit).all()