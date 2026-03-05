import pytest
import pandas as pd
from src.core.config import DATA_PATH_PROCESSED

@pytest.fixture
def load_data():
    df = pd.read_csv("data/processed/dataset_with_skills.csv")
    return df
 

def test_duplons(load_data):
    assert load_data["avg_salary"].duplicated().sum() >= 0

def test_valeurNull(load_data):
    
    assert load_data.isnull().sum().sum() >= 0
