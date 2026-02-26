from sqlalchemy import Column , Integer ,String ,DateTime, func,Boolean
from src.database.session import Base
from sqlalchemy.orm import relationship

class USER(Base) :
    
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True)
    email=Column(String(100),nullable=False,unique=True)
    username = Column(String(50),nullable=False,unique=True)
    password_hash = Column(String,nullable=False)
    is_active = Column(Boolean ,unique=True)

    created_at = Column(DateTime,default=func.now())
    
