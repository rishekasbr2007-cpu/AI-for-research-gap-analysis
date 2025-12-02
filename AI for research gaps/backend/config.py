import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    SPRINGER_API_KEY = os.getenv('SPRINGER_API_KEY', '')
    SEMANTIC_SCHOLAR_API_KEY = os.getenv('SEMANTIC_SCHOLAR_API_KEY', '')
    
    # App Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'research-intelligence-secret-key-2024')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # API URLs
    PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    SPRINGER_API_URL = "https://api.springernature.com/meta/v2/json"
    SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1"
    CROSSREF_URL = "https://api.crossref.org/works"
    
    # Rate limiting
    MAX_RESULTS_PER_SOURCE = 10
    REQUEST_TIMEOUT = 30