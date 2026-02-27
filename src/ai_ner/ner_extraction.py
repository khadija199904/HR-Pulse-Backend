import time
import pandas as pd
from tqdm import tqdm
from src.ai_ner.get_client import authenticate_client
def run_ner_extraction(df_subset, client):
    """Extrait les compétences en respectant les limites du Free Tier."""
    all_skills = []
    print(f"Extraction NER pour {len(df_subset)} lignes...")

    for i, row in tqdm(df_subset.iterrows(), total=len(df_subset)):
        description = str(row["job_description"])[:1000] 
        try:
            response = client.recognize_entities([description])
            doc = response[0]
            if not doc.is_error:
                skills = [
                    entity.text
                    for entity in doc.entities
                    if entity.category in ["Skill", "Product", "SkillName", "ProgrammingLanguage"]
                ]
                all_skills.append(", ".join(list(set(skills))))
            else:
                all_skills.append("")
        except Exception as e:
            print(f"\nErreur ligne {i}: {e}")
            all_skills.append("")

        time.sleep(1.0)
    
    return all_skills


if __name__ == "__main__":
    run_ner_extraction("DATA/dataset.csv", "DATA/dataset_with_skills.csv", limit=100)