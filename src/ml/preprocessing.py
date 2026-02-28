from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor



def preprocess_data(X_train,y_train,):
   
    numeric_features = ['revenue_rank']
    categorical_features = ['Sector', 'Industry', 'job_role', 'job_state']

    

    # Créeation les transformateurs
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    models =  { 
        'RF': RandomForestRegressor(n_estimators=100, random_state=42),
        
        }
    for model_name, model in models.items():
        print(f"Entraînement du modèle : {model_name}")
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)])
        
        pipeline.fit(X_train, y_train)


    return pipeline