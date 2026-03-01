import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.core.config import DATA_PATH_PROCESSED
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def evaluate_model(pipeline, X_test, y_test, model_name):
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print(f"\n--- Rapport : {model_name} ---")
    print(f"R² Score : {r2:.4f} | MAE : {mae:.2f}$ | RMSE : {rmse:.2f}$")
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
    # 1. Chargement et Feature Engineering
    df = pd.read_csv(file_path)
    df = apply_aggressive_fe(df)

    # 2. Définition des colonnes par type
    numeric_features = ['revenue_rank', 'is_senior', 'company_power_score']
    categorical_features = ['job_role_clean', 'job_state_clean', 'Sector']
    

    # 3. Séparation X et y
    # Note: On inclut bien la colonne texte dans X
    X = df[numeric_features + categorical_features  ]
    y = df['avg_salary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Création du Préprocesseur avec TF-IDF
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            
        ])

    # 5. Modèles à tester
    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Ridge": Ridge(alpha=0.1),
    }

    best_r2 = -1
    best_pipeline = None

    for name, model_obj in models.items():
        # Pipeline complet
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model_obj)
        ])

        # Entraînement sur le log du salaire (plus stable)
        y_train_log = np.log1p(y_train)
        y_test_log = np.log1p(y_test)

        pipeline.fit(X_train, y_train_log)
        
        # Évaluation
        metrics = evaluate_model(pipeline, X_test, y_test_log, name)
        
        if metrics['R2'] > best_r2:
            best_r2 = metrics['R2']
            best_pipeline = pipeline
            best_model_name = name

    # 6. Sauvegarde
    os.makedirs("ml_models", exist_ok=True)
    joblib.dump(best_pipeline, "ml_models/best_salary_model.pkl")
    print(f"\n Meilleur modèle sauvegardé : {best_model_name} (R²: {best_r2:.4f})")
    




if __name__ == "__main__":
    
     training_workflow(DATA_PATH_PROCESSED)
   