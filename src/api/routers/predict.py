from fastapi import APIRouter, HTTPException
from src.api.schemas.predict_schema import JobProfile , PredictionResponse
from src.api.services.ml_service import get_prediction
from src.api.dependencies import get_current_user
from src.database.models.users import USER
from fastapi import Depends

router = APIRouter(prefix="/predict", tags=["Prédiction"])




@router.post("/predict",response_model=PredictionResponse)
async def predict_salary(profile: JobProfile,current_user: USER = Depends(get_current_user)):
    
    
    try:
        predicted_salary = get_prediction(profile)
        rounded_salary = round(predicted_salary, 2)

        return {
            "salary_estimate": rounded_salary,
            
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )
       
