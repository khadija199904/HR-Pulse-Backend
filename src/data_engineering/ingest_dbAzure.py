import pandas as pd
import os
from src.ai.ner.get_client import authenticate_client
from src.core.config import db_azure_url
from src.database.models.jobskills import JobSkill
from src.database.session import SessionLocal,engine,Base
from src.ai.ner.ner_extraction import run_ner_extraction
from src.data_engineering.data_cleaning  import clean_data



def ingest_data(file_path):
    """Charge, nettoie via data_cleaning et formate le fichier jobs.csv."""
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} non trouvé.")
        return None
    
    # 1. Chargement du CSV brut
    df_raw = pd.read_csv(file_path)
    
    df_cleaned = clean_data(df_raw)
    
    print(f"Données nettoyées. Valeurs manquantes Job Title : {df_cleaned['Job Title'].isna().sum()}")

    # 2. Création des colonnes nécessaires pour le NER et SQL
    df_cleaned = df_cleaned.reset_index().rename(columns={'index': 'id'})
    
    df_cleaned['job_title'] = df_cleaned['Job Title'].apply(
        lambda x: x.strip() if isinstance(x, str) else "na"
    )
    
    # 3. Sélection et renommage des colonnes finales
    df_final = df_cleaned[['id', 'job_title', 'Job Description']].copy()
    df_final.rename(columns={'Job Description': 'job_description'}, inplace=True)
    
    return df_final

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

def run_pipeline(file_path, limit=None):
    """Orchestrateur utilisant run_ner_extraction pour transformer et injecter les données."""
    
    # --- ÉTAPE 1: Chargement et Nettoyage ---
    df = ingest_data(file_path)
    if df is None: 
        return
    
    # Sélection du subset selon la limite passée au pipeline
    df_sample = df.head(limit).copy()
    
    # --- ÉTAPE 2: Authentification ---
    client = authenticate_client()
    if not client:
        print("Échec de l'authentification Azure.")
        return

    # --- ÉTAPE 3: Extraction (NER) ---
    extracted_results = run_ner_extraction(df_sample, client)
    df_sample['skills_extracted'] = extracted_results

    # --- ÉTAPE 4: Injection SQL ---
    inject_to_sql(df_sample)
    
    return df_sample

if __name__ == "__main__":
    from src.core.config import DATA_PATH
    run_pipeline(DATA_PATH,limit=100)
     