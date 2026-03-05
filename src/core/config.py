from dotenv import load_dotenv
import os
import urllib.parse


# Load environment variables from .env
load_dotenv()

# chemins
DATA_PATH = os.getenv("DATA_PATH")
DATA_PATH_PROCESSED = os.getenv("DATA_PATH_PROCESSED")
MODEL_ML_PATH = os.getenv("MODEL_ML_PATH")

azure_key = os.getenv("AZURE_AI_KEY")
azure_endpoint = os.getenv("AZURE_AI_ENDPOINT")
db_azure_url = os.getenv("AZURE_DB_URL")


if not db_azure_url :
     
    
    # Fetch variables
     USER = os.getenv("USERNAME")
     PASSWORD = os.getenv("PASSWORD")
     HOST = os.getenv("HOST")
     DBNAME = os.getenv("DATABASE")
     encoded_password = urllib.parse.quote_plus(PASSWORD)

     # Construct the SQLAlchemy connection string
     db_azure_url = f"mssql+pyodbc://{USER}:{encoded_password}@{HOST}.database.windows.net/{DBNAME}?driver=ODBC+Driver+18+for+SQL+Server"
     

     raise ValueError(
        "CRITICAL: Connection string is empty. "
        "Check if AZURE_DB_URL or USERNAME/PASSWORD are set in the environment."
    )

 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")







