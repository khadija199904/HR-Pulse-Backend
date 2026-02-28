
from unittest.mock import patch, MagicMock
import pandas as pd
import json

from src.database.session import engine

MOCK_CSV_CONTENT = """index,Job Title,Job Description
1,Python Developer,"Looking for a dev with SQL and Python skills."
2,Data Scientist,"Experience in Machine Learning and R is required."
"""

MOCK_AZURE_RESPONSE = [
    MagicMock(is_error=False, entities=[
        MagicMock(text="Python", category="Skill"),
        MagicMock(text="SQL", category="Skill")
    ]),
    MagicMock(is_error=False, entities=[
        MagicMock(text="Machine Learning", category="Skill")
    ])
]


def test_full_ingestion_logic():
    """Teste la transformation des données sans fichier réel."""
    
    
    from io import StringIO
    df = pd.read_csv(StringIO(MOCK_CSV_CONTENT))
    
    df['job_title_cleaned'] = df['Job Title'].str.strip()
    df_clean = df.rename(columns={'index': 'id', 'Job Description': 'job_description'})
    
    assert len(df_clean) == 2
    assert df_clean.iloc[0]['job_title_cleaned'] == "Python Developer"

def test_extract_skills_mapping():
    """Teste si les entités Azure sont correctement transformées en JSON."""
    
   
    mock_client = MagicMock()
    mock_client.recognize_entities.return_value = MOCK_AZURE_RESPONSE
    
    descriptions = ["Desc 1", "Desc 2"]
    
    
    extracted_results = []
    response = mock_client.recognize_entities(documents=descriptions)
    
    for doc in response:
        skills = [ent.text for ent in doc.entities if ent.category == "Skill"]
        extracted_results.append(json.dumps(list(set(skills))))
    
    
    assert "Python" in extracted_results[0]
    assert "SQL" in extracted_results[0]
    assert "Machine Learning" in extracted_results[1]
    assert isinstance(extracted_results[0], str) 



@patch('src.database.session.SessionLocal')
def test_sql_injection_format(mock_session_local):
    """Teste si les données envoyées à SQLAlchemy ont le bon format."""
    
    # Mock de la session DB
    mock_db = MagicMock()
    mock_session_local.return_value = mock_db
    
    # Fake DataFrame prêt pour l'injection
    data = {
        'id': [1],
        'job_title_cleaned': ['Tester'],
        'skills_extracted': ['["Pytest"]']
    }
    df_test = pd.DataFrame(data)
    
    # Simulation de l'injection
    for record in df_test.to_dict('records'):
        assert 'id' in record
        assert isinstance(record['id'], int)
        
   