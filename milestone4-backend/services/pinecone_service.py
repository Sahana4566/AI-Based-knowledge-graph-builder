from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from config import Config
from typing import List, Dict, Optional

class PineconeService:
    def __init__(self):
        self.pc = None
        self.index = None
        self.model = None
        self.connected = False
        self._initialize()
    
    def _initialize(self):
        """Initialize Pinecone client and load embedding model"""
        try:
            if not Config.PINECONE_API_KEY:
                print("Pinecone: API key not configured")
                return
            
            # Initialize Pinecone
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
            
            # Get index reference
            index_name = Config.PINECONE_INDEX_NAME
            if index_name not in self.pc.list_indexes().names():
                print(f"Warning: Index '{index_name}' not found in Pinecone")
                return
            
            self.index = self.pc.Index(index_name)
            
            # Load embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            self.connected = True
            print("✓ Pinecone connected successfully")
            print(f"✓ Embedding model loaded (384-dim)")
        
        except Exception as e:
            print(f"✗ Pinecone initialization failed: {str(e)}")
            self.connected = False
            self.index = None
            self.model = None
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Semantic search on embeddings
        
        Args:
            query: Search query text
            top_k: Number of top results
        
        Returns:
            List of {id, score, text} dictionaries
        """
        if not self.connected or not self.index or not self.model:
            print("Pinecone not available, returning mock results")
            return self._mock_results(query, top_k)
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])
            query_vector = query_embedding[0].tolist()
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            matches = []
            for match in results.get('matches', []):
                matches.append({
                    'id': match['id'],
                    'score': round(float(match.get('score', 0)), 3),
                    'text': match.get('metadata', {}).get('text', f'Document {match["id"]}')
                })
            
            return matches
        
        except Exception as e:
            print(f"Pinecone search error: {str(e)}")
            return self._mock_results(query, top_k)
    
    def _mock_results(self, query: str, top_k: int) -> List[Dict]:
        """Return mock results for testing"""
        mock_docs = [
            "Barack Obama was the President of the United States",
            "Microsoft was founded by Bill Gates",
            "Google is headquartered in California",
            "Tesla was founded by Elon Musk",
            "Amazon is an e-commerce company"
        ]
        
        # Simple keyword matching for demo
        results = []
        for i, doc in enumerate(mock_docs[:top_k]):
            score = 0.8 - (i * 0.1)  # Decreasing scores
            results.append({
                'id': str(i),
                'score': score,
                'text': doc
            })
        
        return results

# Singleton instance
pinecone_service = PineconeService()
