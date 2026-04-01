from flask import Blueprint, request, jsonify
from services.pinecone_service import pinecone_service
from typing import Dict, List

semantic_bp = Blueprint('semantic', __name__, url_prefix='/semantic')

@semantic_bp.route('/search', methods=['POST'])
def search():
    """
    Semantic search on embeddings
    
    Request Body:
        {
            "query": "Who founded Microsoft?",
            "topK": 3
        }
    
    Response:
        {
            "matches": [
                {"id": "0", "score": 0.92, "text": "Microsoft was founded by Bill Gates"},
                ...
            ],
            "total": 3,
            "error": null
        }
    """
    try:
        # Get JSON body
        data = request.get_json()
        if not data:
            return jsonify({
                'matches': [],
                'total': 0,
                'error': 'No JSON body provided'
            }), 400
        
        query = data.get('query', '').strip()
        top_k = min(int(data.get('topK', 3)), 10)
        
        if not query:
            return jsonify({
                'matches': [],
                'total': 0,
                'error': 'Query cannot be empty'
            }), 400
        
        # Search Pinecone
        matches = pinecone_service.semantic_search(query=query, top_k=top_k)
        
        return jsonify({
            'matches': matches,
            'total': len(matches),
            'error': None
        }), 200
    
    except Exception as e:
        return jsonify({
            'matches': [],
            'total': 0,
            'error': str(e)
        }), 500

@semantic_bp.route('/health', methods=['GET'])
def health():
    """
    Check semantic search service health
    
    Response:
        {
            "connected": true,
            "model": "all-MiniLM-L6-v2",
            "dimension": 384,
            "error": null
        }
    """
    try:
        return jsonify({
            'connected': pinecone_service.connected,
            'model': 'all-MiniLM-L6-v2',
            'dimension': 384,
            'error': None
        }), 200
    
    except Exception as e:
        return jsonify({
            'connected': False,
            'model': None,
            'dimension': 0,
            'error': str(e)
        }), 500
