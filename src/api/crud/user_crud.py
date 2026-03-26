from src.core.security import password_hash
from src.database.models.users import USER
from src.api.schemas.user_schema import UserCreate

def create_user (user : UserCreate):
    hashed_password = password_hash(user.password)
    new_user = USER(email= user.email,username=user.username,password_hash=hashed_password)
    return new_user 

