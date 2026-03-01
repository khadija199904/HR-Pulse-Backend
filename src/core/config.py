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
db_azure_url = os.getenv("AZURE_SQL_URL")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL :
    # Fetch variables
     USER = os.getenv("user")
     PASSWORD = os.getenv("password")
     HOST = os.getenv("host")
     PORT = os.getenv("port")
     DBNAME = os.getenv("dbname")
     encoded_password = urllib.parse.quote_plus(PASSWORD)

     # Construct the SQLAlchemy connection string
     DATABASE_URL = f"postgresql+psycopg2://{USER}:{encoded_password}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")







