from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()


DATA_PATH = os.getenv("DATA_PATH")

azure_key = os.getenv("AZURE_AI_KEY")
azure_endpoint = os.getenv("AZURE_AI_ENDPOINT"
db_azure_url = os.getenv("AZURE_SQL_URL")

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL :
#     # Fetch variables
#      USER = os.getenv("POSTGRES_USER")
#      PASSWORD = os.getenv("POSTGRES_PASSWORD")
#      HOST = os.getenv("POSTGRES_HOST")
#      PORT = os.getenv("POSTGRES_PORT")
#      DBNAME = os.getenv("POSTGRES_DB")

#      # Construct the SQLAlchemy connection string
#      DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")






if __name__ == "__main__":
  try:
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT )
    print(f"Connecté au serveur Chroma sur {CHROMA_HOST}:{CHROMA_PORT }")
  except Exception as e:
    print(f"Erreur de connexion : {e}")