import atexit

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.graph import graph_bp
from routes.semantic import semantic_bp
from services.neo4j_service import neo4j_service
from services.pinecone_service import pinecone_service

def create_app():
    """Create and configure Flask app"""
    app = Flask('app')
    
    # Configuration
    Config.validate()
    
    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": Config.API_CORS_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(graph_bp)
    app.register_blueprint(semantic_bp)
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'ok',
            'neo4j': 'connected' if neo4j_service.connected else 'disconnected',
            'pinecone': 'connected' if pinecone_service.connected else 'disconnected'
        }), 200
    
    @app.route('/', methods=['GET'])
    def index():
        """API root"""
        return jsonify({
            'name': 'Milestone 4 Backend API',
            'version': '1.0.0',
            'endpoints': {
                'graph': {
                    'query': 'GET /graph/query?entity=...&relation=...&limit=20',
                    'stats': 'GET /graph/stats'
                },
                'semantic': {
                    'search': 'POST /semantic/search',
                    'health': 'GET /semantic/health'
                },
                'health': 'GET /health'
            }
        }), 200
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    pass

# Create app instance for Flask CLI and imports
app = create_app()


def _shutdown_services() -> None:
    if neo4j_service.driver:
        neo4j_service.close()


atexit.register(_shutdown_services)

if __name__ == '__main__':
    print(f"🚀 Starting server on http://localhost:{Config.FLASK_PORT}")
    try:
        app.run(host='0.0.0.0', port=Config.FLASK_PORT, debug=Config.DEBUG, use_reloader=False)
    except Exception as e:
        print(f"Error starting server: {e}")
