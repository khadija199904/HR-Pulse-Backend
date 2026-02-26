import pandas as pd
from .data_cleaning import clean_data


def engineer_features(df_cleaned):
    df = df_cleaned.copy()
     # 1. Création du revenue_rank (Basé sur le Revenue)
    def revenue_level(val):
      val = str(val).lower()
      if 'billion' in val:
          return 2  
      if 'million' in val:
          return 1 
      return 0 
    
    df['revenue_rank'] = df['Revenue'].apply(revenue_level)
    
    # 2. Création du Métier (Basé sur le Job Title)
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
    
    # 3. Extraction de l'État (Location)
    df['job_state'] = df['Location'].apply(lambda x: x.split(',')[-1].strip() if ',' in str(x) else 'Remote')
    
    # Sélection des colonnes finales pour le modèle
    

    output_path = "./data/raw/cleaned_data.csv"
    df_final = df
    # Sauvegarder le DataFrame
    df_final.to_csv(output_path, index=False, encoding='utf-8')

    print(f" Données sauvegardées avec succès dans : {output_path}")
    return df_final



if __name__ == "__main__":
    df = pd.read_csv("./data/raw/jobs.csv")
    df_cleaned = clean_data(df)
    final_df = engineer_features(df_cleaned)
    print(final_df.head())