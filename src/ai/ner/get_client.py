from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from src.core.config import azure_key,azure_endpoint

def authenticate_client():
    """Authenticate Azure Text Analytics client."""
    
    if not azure_key or not azure_endpoint:
        print("Error: Azure AI credentials not found in .env (AZURE_AI_KEY/AZURE_AI_ENDPOINT)")
        return None
        
    return TextAnalyticsClient(endpoint=azure_endpoint, credential=AzureKeyCredential(azure_key))