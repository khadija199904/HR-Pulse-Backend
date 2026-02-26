import pandas as pd
import os
from src.core.config import DATA_PATH_PROCESSED


# 1. Chargement des deux fichiers
df_clean = pd.read_csv(DATA_PATH_PROCESSED)
df_skills = pd.read_csv('./data/raw/extracted_skills_only.csv')

# 2. Sécurité : On réinitialise les index pour aligner parfaitement les lignes
df_clean = df_clean.reset_index(drop=True)
df_skills = df_skills.reset_index(drop=True)

# 3. Concaténation horizontale (on colle les colonnes côte à côte)
df_final = pd.concat([df_clean, df_skills], axis=1)

# Optionnel : Supprimer les colonnes en double si elles existent (ex: 'index' ou 'id')
df_final = df_final.loc[:, ~df_final.columns.duplicated()]
output_path = "./data/processed/dataset_with_skills.csv"

# Sécurité : créer le dossier s'il n'existe pas
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df_final.to_csv(output_path, index=False, encoding='utf-8')

print(f"Colonnes après fusion : {df_final.columns.tolist()}")