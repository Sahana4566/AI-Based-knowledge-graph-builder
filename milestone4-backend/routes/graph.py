from flask import Blueprint, request, jsonify
from services.neo4j_service import neo4j_service
from typing import Dict, List

graph_bp = Blueprint('graph', __name__, url_prefix='/graph')

@graph_bp.route('/query', methods=['GET'])
def query():
    """
    Query graph entities and relations
    
    Query Parameters:
        - entity: Filter by entity name (partial match, case-insensitive)
        - relation: Filter by relation type
        - limit: Maximum number of results (default 20, max 100)
    
    Response:
        {
            "rows": [
                {"head": "Barack Obama", "relation": "born_in", "tail": "Hawaii"},
                ...
            ],
            "total": 5,
            "error": null
        }
    """
    try:
        # Get query parameters
        entity = request.args.get('entity', '').strip()
        relation = request.args.get('relation', '').strip()
        limit = min(int(request.args.get('limit', 20)), 100)
        
        # Query Neo4j
        rows = neo4j_service.query_graph(entity=entity, relation=relation, limit=limit)
        
        return jsonify({
            'rows': rows,
            'total': len(rows),
            'error': None
        }), 200
    
    except Exception as e:
        return jsonify({
            'rows': [],
            'total': 0,
            'error': str(e)
        }), 500

@graph_bp.route('/stats', methods=['GET'])
def stats():
    """
    Get graph statistics
    
    Response:
        {
            "entities": 13781,
            "relations": 237,
            "connected": true,
            "error": null
        }
    """
    try:
        entities = neo4j_service.count_entities()
        relations = neo4j_service.count_relations()
        
        return jsonify({
            'entities': entities,
            'relations': relations,
            'connected': neo4j_service.connected,
            'error': None
        }), 200
    
    except Exception as e:
        return jsonify({
            'entities': 0,
            'relations': 0,
            'connected': False,
            'error': str(e)
        }), 500
