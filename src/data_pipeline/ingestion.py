import pandas as pd
import os
import json
from src.ai_ner.get_client import authenticate_client
from src.core.config import db_azure_url
from src.database.models.jobskills import JobSkill
from src.database.session import SessionLocal,engine,Base





def extract_skills(client, descriptions):
    """Extract skills from a list of descriptions using Azure NER."""
    if not client:
        return [json.dumps([])] * len(descriptions)
        
    try:
        response = client.recognize_entities(documents=descriptions)
        extracted_skills = []
        for doc in response:
            if doc.is_error:
                print(f"Document error: {doc.error}")
                extracted_skills.append(json.dumps([]))
                continue
            
            skills = [entity.text for entity in doc.entities if entity.category in ["Skill", "Product", "SkillName", "ProgrammingLanguage"]]
            extracted_skills.append(json.dumps(list(set(skills))))
        return extracted_skills
    except Exception as e:
        print(f"Error during NER extraction: {e}")
        return [json.dumps([])] * len(descriptions)

def ingest_data(file_path):
    """Load and clean the jobs.csv file."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return None
    
    df = pd.read_csv(file_path)
    print(df['Job Title'].isna().sum())
    df['job_title_cleaned'] = df['Job Title'].apply(lambda x: x.strip() if isinstance(x, str) else "na")
    df_clean = df[['index', 'job_title_cleaned', 'Job Description']].copy()
    df_clean.rename(columns={'index': 'id', 'job_title_cleaned': 'job_title', 'Job Description': 'job_description'}, inplace=True)
    return df_clean

def inject_to_sql(df):
    """Inject cleaned data into Azure SQL."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db_azure_url:
        print("Error: AZURE_SQL_URL not found in .env")
        return
    
    try:
       
        for record in df.to_dict('records'):
            jobskill = JobSkill(
                id=int(record['id']),
                job_title=record['job_title'],
                skills_extracted=record['skills_extracted']
            )
            db.merge(jobskill) 
            
        db.commit()
        print(f"Successfully injected {len(df)} records into Azure SQL.")
    except Exception as e:
        print(f"Error during SQL injection: {e}")

def run_pipeline(file_path, limit=3):
    """Run the full ingestion, extraction, and injection pipeline."""
    df = ingest_data(file_path)
    if df is None: return
    
    df_sample = df.head(limit).copy()
    client = authenticate_client()
    
    if client:
        descriptions = df_sample['job_description'].apply(lambda x: str(x)[:5000]).tolist()
        print(f"Extracting skills for {len(descriptions)} jobs...")
        skills = extract_skills(client, descriptions)
        df_sample['skills_extracted'] = skills
        
        inject_to_sql(df_sample)
    
    return df_sample

if __name__ == "__main__":
    from src.core.config import DATA_PATH
    run_pipeline(DATA_PATH, limit=2)
     