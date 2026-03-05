import pandas as pd
from src.data_engineering.data_cleaning import clean_data
from src.data_engineering.features_eng import engineer_features
import os

def run_data_pipeline():
    input_path = "./data/raw/jobs.csv"
    output_dir = "./data/processed"
    output_file = os.path.join(output_dir, "processed_data.csv")
    
    if not os.path.exists(input_path):
        print(f"Erreur : Le fichier {input_path} est introuvable.")
        return

    print("Démarrage du pipeline de data engineering...")
    
    # 1. Chargement
    print("Chargement des données brutes...")
    df = pd.read_csv(input_path)
    
    # 2. Nettoyage
    print("Nettoyage des données...")
    df_cleaned = clean_data(df)
    
    # 3. Feature Engineering
    print("Création des features...")
    final_df = engineer_features(df_cleaned)

    os.makedirs(output_dir, exist_ok=True)
    
    # Sauvegarde finale
    final_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print("\nPipeline terminé avec succès !")
    print(f"Fichier disponible ici : {output_file}")
    print(final_df.head())
    
    return final_df

if __name__ == "__main__":
    run_data_pipeline()
