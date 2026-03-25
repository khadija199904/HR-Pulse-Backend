from fastapi import APIRouter,Depends
from src.api.dependencies import get_current_user
from src.database.models.users import USER

router = APIRouter( prefix="/profil", tags=["profil"])
@router.get("/")
def read_profil(current_user: USER = Depends(get_current_user)):
    return {"email": current_user.email}