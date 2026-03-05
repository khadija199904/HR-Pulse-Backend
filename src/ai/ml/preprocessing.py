from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

def get_feature():
    """
    Centralise la définition des colonnes utilisées par le modèle.
    Retourne les listes par type et la liste complète.
    """
    num_features = ['Rating', 'revenue_rank']
    cat_features = ['job_role', 'job_state', 'Sector']
    text_feature = 'Job Description'
    
    # La liste ordonnée pour X
    all_features = num_features + cat_features + [text_feature]
    
    return num_features, cat_features, text_feature, all_features

def get_pipeline(model_obj):
    
    num_features, cat_features, text_feature, _ = get_feature()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features),
            ('text', TfidfVectorizer(max_features=500, stop_words='english'), text_feature),
        ],
        remainder='drop'
    )

    # Pipeline complet
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model_obj)
    ])
    
    
    return pipeline