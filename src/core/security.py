from passlib.context import CryptContext
from .config import SECRET_KEY
from jose import jwt


pwd = CryptContext(schemes=["argon2"],deprecated="auto")

def password_hash(password):
    return pwd.hash(password)


def verify_password_hash(password,hashed_password):
    return pwd.verify(password,hashed_password)




def create_token(user):
    payload = { "id": user.id}
    print(f"DEBUG: SECRET_KEY is {type(SECRET_KEY)} and value is {SECRET_KEY}")
    token = jwt.encode(payload,key=SECRET_KEY,algorithm="HS256")
    return token