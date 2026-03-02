from sqlalchemy import create_engine 
from src.core.config import DATABASE_URL
from sqlalchemy.orm import declarative_base , sessionmaker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


engine= create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind = engine)

Base = declarative_base()

SQLAlchemyInstrumentor().instrument(engine=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
  
   try:
        with engine.connect() as connection:
            print("Connection successful!")
   except Exception as e:
        print(f"Failed to connect: {e}")
 


