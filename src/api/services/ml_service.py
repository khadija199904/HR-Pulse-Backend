import pandas as pd 
from src.api.utils.get_model import load_ml_model
from src.core.config import MODEL_ML_PATH


model = load_ml_model(MODEL_ML_PATH)

def get_prediction(data):
    input_df= pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)
    
    return prediction