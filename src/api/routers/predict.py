from fastapi import APIRouter
from src.api.schemas.predict_schema import JobProfile
from src.api.services.ml_service import get_prediction

router = APIRouter(prefix="/predict", tags=["Prédiction"])




@router.post("/predict")
async def predict_salary(profile: JobProfile):
   
    prediction = get_prediction(profile)
    return {
        "salary_estimate": round(prediction, 2),
        
    }