import pandas as pd
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ai.ml.data_cleaning import clean_data

def test_data_quality():
    raw_data = {
        'index': [0, 1, 2],
        'Salary Estimate': ['$50K-$70K', '$60K', '$10K-$20K'],
        'Rating': [-1, 4.5, 3.0],                        
        'Founded': [2000, -1, 2010],                     
        'Size': ['-1', 'Small', 'Unknown / Non-Applicable'],
        'Revenue': ['Unknown / Non-Applicable', '$1M', '-1'], 
        'Sector': ['IT', '-1', 'Finance'],
        'Industry': ['Tech', 'Tech', 'Tech'],
        'Type of ownership': ['Private', 'Public', 'Private'],
        'Competitors': ['-1', 'A', 'B']
    }
    df_test = pd.DataFrame(raw_data)

    df_cleaned = clean_data(df_test)

    assert df_cleaned.isnull().sum().sum() == 0, "Erreur: Il reste des valeurs NaN !"
    assert (df_cleaned['Rating'] == -1).sum() == 0, "Erreur: Il reste des -1 dans Rating"
    assert (df_cleaned['Founded'] == -1).sum() == 0, "Erreur: Il reste des -1 dans Founded"

    invalid_values = ['-1', 'Unknown / Non-Applicable']
    for col in df_cleaned.columns:
        remainder = df_cleaned[df_cleaned[col].astype(str).isin(invalid_values)]
        assert len(remainder) == 0, f"Erreur: Il reste des valeurs invalides dans la colonne {col}"

   
    assert 'index' not in df_cleaned.columns, "Erreur: La colonne 'index' n'a pas été supprimée"

    print("✅ Test réussi : Le DataFrame est propre (aucun NaN, aucun -1, aucune valeur interdite).")

if __name__ == "__main__":
    # Assurez-vous que vos fonctions clean_salary, remove_outliers et clean_data 
    # sont bien définies au-dessus dans le même fichier.
    test_data_quality()