import pandas as pd
import numpy as np
from .data_cleaning import clean_data


def engineer_features(df_cleaned):
    df = df_cleaned.copy()
    # Création de l'âge de l'entreprise
    current_year = 2026
    df['company_age'] = df['Founded'].apply(lambda x: current_year - x if x > 0 else np.nan)
    df['company_age'] = df['company_age'].fillna(df['company_age'].median())
    #1. Création du type d'entreprise
    def categorize_age(age):
        if age < 5: 
            return 'Startup'
        elif age < 15: 
            return 'Scale-up'
        elif age < 50: 
            return 'Established'
        else: 
            return 'Legacy'
    
    df['company_type'] = df['company_age'].apply(categorize_age)
     # 2. Création du revenue_rank (Basé sur le Revenue)
    def revenue_level(val):
      val = str(val).lower()
      if 'billion' in val:
          return 2  
      if 'million' in val:
          return 1 
      return 0 
    
    df['revenue_rank'] = df['Revenue'].apply(revenue_level)
    
    # 3 Création du Métier (Basé sur le Job Title)
    def categorize_role(title):
        title = str(title).lower()
        if 'data scientist' in title or 'scientist' in title:
          return 'Data Scientist'
        if 'analyst' in title or 'analytics' in title:
          return 'Data Analyst'
        if 'engineer' in title or 'mle' in title:
           return 'Data Engineer / MLE'
        if 'manager' in title or 'director' in title or 'head' in title:
           return 'Manager / Director'
        return 'Other'
    
    df['job_role'] = df['Job Title'].apply(categorize_role)
    
    # 4. Extraction de l'État (Location)
    df['job_state'] = df['Location'].apply(lambda x: x.split(',')[-1].strip() if ',' in str(x) else 'Remote')
    
    # 5. Extraction du niveau de seniorité
    def extract_seniority(title):
        title = str(title).lower()
   
        leadership = ['principal', 'vp', 'director', 'head', 'lead', 'staff', 'manager']
        seniors = ['senior', 'sr', 'iii', 'iv']
        juniors = ['junior', 'jr', 'entry', 'associate', 'intern']

        if any(word in title for word in leadership):
            return 1
        if any(word in title for word in seniors):
            return 2
        if any(word in title for word in juniors):
            return 3
        
        return 4 # Mid-level 
    
    df['seniority_score'] = df['Job Title'].apply(extract_seniority)
    # 6. Création d'une colonne binaire senior
    df['is_senior'] = df['Job Title'].str.contains('senior|sr|lead|principal|manager', case=False).astype(int)
    # 7. Création du score de taille
    df['size_score'] = df['Size'].apply(lambda x: 1 if 'small' in str(x).lower() else 2 if 'medium' in str(x).lower() else 3)
    # 8. Création du score de capacité de l'entreprise
    df['company_power_score'] = df['size_score'] * df['revenue_rank']

    output_path = "./data/processed/processed_data.csv"
   
    # Sauvegarder le DataFrame
    df.to_csv(output_path, index=False, encoding='utf-8')

    print(f" Données sauvegardées avec succès dans : {output_path}")
    return df



if __name__ == "__main__":
    df = pd.read_csv("./data/raw/jobs.csv")
    df_cleaned = clean_data(df)
    final_df = engineer_features(df_cleaned)
    print(final_df.head())