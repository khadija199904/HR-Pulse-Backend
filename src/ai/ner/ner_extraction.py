import time
from tqdm import tqdm

def run_ner_extraction(df_subset, client):
    """Extrait les compétences en respectant les limites du Free Tier."""
    df_working = df_subset.copy()
    all_skills = []
    print(f"Extraction NER pour {len(df_working)} lignes...")

    for i, row in tqdm(df_working.iterrows(), total=len(df_working)):
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
    # On sauvegarde la collone extracted_skills
    output_path = "./data/processed/extracted_skills_only.csv"
    df_working["extracted_skills"] = all_skills
    df_working["extracted_skills"].to_csv(output_path, index=True)

    
    return all_skills