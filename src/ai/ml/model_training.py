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
from sklearn.feature_extraction.text import TfidfVectorizer
from src.core.config import MODEL_ML_PATH

def get_pipeline(model_obj):
    
    num_features = ['Rating','revenue_rank']
    cat_features = ['job_role', 'job_state', 'Sector']
    text_feature = 'Job Description'

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    text_transformer = TfidfVectorizer(max_features=500, stop_words='english')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features),
            ('text', text_transformer, text_feature),
           
        ],
        remainder='drop')

    # Pipeline complet
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model_obj)
    ])
    features_cols =num_features + cat_features  + [text_feature] 
    
    return pipeline, features_cols


def evaluate_model(pipeline, X_test, y_test, model_name):
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    MAE_dollars = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))
    rmse_dollars = np.sqrt(mean_squared_error(np.expm1(y_test), np.expm1(y_pred)))
    print(f"R² Score : {r2:.4f} | MAE : {MAE_dollars:.2f}$ | RMSE : {rmse_dollars:.2f}$")
    return {"R2": r2, "MAE": mae, "RMSE": rmse}





def train_salary_model(input_csv):
    # 1. Chargement des données
    print(f"Chargement des données depuis : {input_csv}")
    df = pd.read_csv(input_csv)
    
    # 2. Modèles à tester
    models_to_test = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "RidgeCV": RidgeCV(alphas=[0.01, 1.0, 10.0, 20.0, 50.0])
    }

    best_r2 = -1
    best_pipeline = None
    best_model_name = ""

    _, features = get_pipeline(None)
    
    X = df[features]
    y = df['avg_salary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraînement sur le log du salaire (plus stable pour les distributions de salaires)
    y_train_log = np.log1p(y_train)
    y_test_log = np.log1p(y_test)

    for name, model_obj in models_to_test.items():
        print(f"\nEntraînement de {name}...")
        
        
        pipeline, _ = get_pipeline(model_obj)
        
        # Entraînement
        pipeline.fit(X_train, y_train_log)
        
        # Évaluation
        metrics = evaluate_model(pipeline, X_test, y_test_log, name)
        
        # Sélection du meilleur modèle basé sur le R²
        if metrics['R2'] > best_r2:
            best_r2 = metrics['R2']
            best_pipeline = pipeline
            best_model_name = name

    # 4. Sauvegarde du meilleur modèle
    if best_pipeline:
        
        model_path = MODEL_ML_PATH
        joblib.dump(best_pipeline, model_path)
        print(f"\nSuccès ! Meilleur modèle : {best_model_name} (R²: {best_r2:.4f})")
        print(f"Modèle sauvegardé dans : {model_path}")
    




if __name__ == "__main__":
    train_salary_model(DATA_PATH_PROCESSED)
   