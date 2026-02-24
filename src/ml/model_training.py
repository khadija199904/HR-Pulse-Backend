import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.core.config import DATA_PATH_PROCESSED
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
from sklearn.impute import SimpleImputer
import os

def extract_skills_features(df):
    # On définit les mots-clés stratégiques
    skills_to_track = ['python', 'excel', 'aws', 'spark', 'sql', 'tableau', 'machine learning', 'azure']
    
    for skill in skills_to_track:
        # Création d'une colonne binaire : 1 si le skill est présent, 0 sinon
        df[f'has_{skill.replace(" ", "_")}'] = df['Job Description'].str.lower().apply(
            lambda x: 1 if skill in str(x) else 0
        )
    return df, [f'has_{skill.replace(" ", "_")}' for skill in skills_to_track]

def get_pipeline(model,numeric_features, categorical_features):
    """Crée le pipeline de preprocessing + modèle"""
   # Dans ton script de training
   
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    return Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])



def evaluate_model(pipeline, X_test, y_test, model_name):
    # Générer les prédictions
    y_pred = pipeline.predict(X_test)
    
    # Calcul des métriques
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    print(f"\n--- Rapport de Performance : {model_name} ---")
    print(f"R² Score (Précision)    : {r2:.4f}")
    print(f"MAE (Erreur Moyenne)    : {mae:.2f} $")
    print(f"RMSE (Écart Moyen)      : {rmse:.2f} $")
    print(f"MSE (Erreur au carré)   : {mse:.2f}")
    
    return {"R2": r2, "MAE": mae, "RMSE": rmse}

def apply_aggressive_fe(df):
    df = df.copy()
    
    # Seniorité Binaire (p-value était trop haute, on simplifie)
    df['is_senior'] = df['Job Title'].str.contains('senior|sr|lead|principal|manager', case=False).astype(int)

    # Nettoyage des Rôles (On garde le Top 3, le reste = 'other')
    top_roles = ['data scientist', 'data analyst', 'data engineer']
    df['job_role_clean'] = df['job_role'].apply(lambda x: x if str(x).lower() in top_roles else 'other')

    # Nettoyage Géographique (Top 5 States)
    top_states = df['job_state'].value_counts().nlargest(5).index
    df['job_state_clean'] = df['job_state'].apply(lambda x: x if x in top_states else 'other')

    # Score de puissance (Interaction Taille x Revenu)
    df['company_power_score'] = df['size_score'] * df['revenue_rank']
    
    return df


def training_workflow(file_path):
    # Chargement
    df = pd.read_csv(file_path)
    df = apply_aggressive_fe(df)
    df, extracted_skills_columns = extract_skills_features(df)
    # Séparation
    numeric_features = ['Rating', 'revenue_rank', 'is_senior', 'company_power_score'] + extracted_skills_columns
    categorical_features = ['job_role_clean', 'job_state_clean', 'Sector']
    
    X = df[numeric_features + categorical_features]
    y = df['avg_salary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraînement
    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        'Ridge': Ridge(alpha=0.1),
        "RidgeCV": RidgeCV(alphas=[0.01, 1.0, 10.0, 20.0, 50.0])
    }

    best_r2 = -1
    best_model = None

    for name, model_obj in models.items():
        # Création du pipeline (Preproc + Modèle)
        pipeline = get_pipeline(model_obj, numeric_features, categorical_features)
        y_train_log = np.log1p(y_train)
        y_test_log = np.log1p(y_test)

# On entraîne le modèle sur le Log
        pipeline.fit(X_train, y_train_log)
       
        
        # Évaluation complète
        metrics = evaluate_model(pipeline, X_test, y_test_log, name)
        
        # Sauvegarde du meilleur modèle basé sur le R²
        if metrics['R2'] > best_r2:
            best_r2 = metrics['R2']
            best_model = pipeline
            best_model_name = name

    os.makedirs("ml_models", exist_ok=True)
    print(f"\n Meilleur modèle : {best_model_name} (R²: {best_r2:.4f})")
    joblib.dump(best_model, "ml_models/best_salary_model.pkl")
    print("Modèle sauvegardé dans 'models/best_salary_model.pkl'")
    




if __name__ == "__main__":
    
     training_workflow(DATA_PATH_PROCESSED)
   