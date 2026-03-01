import os
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Définit les variables d'environnement nécessaires pour les tests 
    AVANT que toute autre partie du code ne soit importée.
    """
    os.environ["AZURE_SQL_URL"] = "sqlite:///:memory:"
    os.environ["AZURE_AI_KEY"] = "fake_key"
    os.environ["AZURE_AI_ENDPOINT"] = "https://fake.endpoint"
    os.environ["DATA_PATH"] = "data/raw/jobs.csv"
    os.environ["DATA_PATH_PROCESSED"] = "data/processed/jobs_cleaned.csv"
    os.environ["MODEL_ML_PATH"] = "ml_models_saved/model.pkl"
    os.environ["SECRET_KEY"] = "test_secret_key"
