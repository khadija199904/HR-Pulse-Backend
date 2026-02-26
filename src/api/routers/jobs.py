from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.api.dependencies import get_db
from src.api.crud import jobs_crud
from src.api.schemas.job_schema import JobSkillSchema
from src.data_pipeline.ingestion import run_pipeline
import os
import shutil

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/titles", response_model=list[str])
def get_job_titles(db: Session = Depends(get_db)):
    results = jobs_crud.liste_jobs(db)
    return [r[0] for r in results]

@router.get("/search", response_model=list[JobSkillSchema])
def search_jobs(skills: str, db: Session = Depends(get_db)):
    return jobs_crud.search_jobs_by_skills(db, skills)

@router.post("/upload")
async def upload_jobs(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")
    
    # Ensure data/raw directory exists
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Run pipeline with a limit for demo purposes
        run_pipeline(file_path, limit=5)
        return {"message": f"File {file.filename} uploaded and processed successfully (first 5 records processed)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
