import pandas as pd 
from src.api.utils.get_model import load_ml_model
from src.core.config import MODEL_ML_PATH
from src.data_engineering.features_eng import engineer_features
from src.ai.ml.preprocessing import get_feature


model = load_ml_model(MODEL_ML_PATH)

def get_prediction(job_data):
    _, _, _, features = get_feature()
    df = pd.DataFrame([job_data.model_dump(by_alias=True)])
    df_transformed = engineer_features(df)
    X_input = df_transformed[features]
    
    # PRÉDICTION
    pred_log = model.predict(X_input)
    final_salary = np.expm1(pred_log)[0]
    return final_salary


