from src.database.session import SessionLocal
from fastapi import Depends, HTTPException, status ,Header
from sqlalchemy.orm import Session
from src.core.config import SECRET_KEY 
from src.database.models.users import USER
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dépendance pour la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# verificatin de token crée en login
def get_current_user (db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
    try :
       payload = jwt.decode(token,key=SECRET_KEY,algorithms="HS256")
       user_id = payload.get("id")
       if user_id is None:
           raise HTTPException(status_code=403, detail="Token invalide : ID utilisateur absent")
       
    except JWTError:
      raise HTTPException(status_code=401,detail="Token expiré ou corrompu")

    user_db = db.query(USER).filter(USER.id == user_id).first()
    
    
    if not user_db:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user_db