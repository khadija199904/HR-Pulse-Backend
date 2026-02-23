from sqlalchemy import create_engine 
from src.core.config import db_azure_url
from sqlalchemy.orm import declarative_base , sessionmaker


engine= create_engine(db_azure_url)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()