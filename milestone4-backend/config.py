import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Neo4j
    NEO4J_URI = os.getenv('NEO4J_URI')
    NEO4J_USER = os.getenv('NEO4J_USER')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    
    # Pinecone
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'semantic-search-index')
    
    # API
    API_CORS_ORIGINS = [
        'http://localhost:5173',
        'http://localhost:5174',
        'http://localhost:5175',
        'http://localhost:3000',
    ]
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        required = [
            'NEO4J_URI', 'NEO4J_USER', 'NEO4J_PASSWORD',
            'PINECONE_API_KEY'
        ]
        missing = [key for key in required if not os.getenv(key)]
        if missing:
            print(f"Warning: Missing environment variables: {', '.join(missing)}")
            print("Some features may not work. See .env.example for required setup.")
