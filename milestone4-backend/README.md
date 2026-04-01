# Milestone 4 Backend API

Flask-based REST API for graph queries and semantic search.

## Project Structure

```
milestone4-backend/
├── app.py                 # Main Flask app
├── config.py             # Configuration from .env
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .env                  # Actual credentials (git-ignored)
├── services/
│   ├── neo4j_service.py      # Neo4j graph queries
│   ├── pinecone_service.py   # Pinecone semantic search
│   └── model_service.py      # ML model loading
├── routes/
│   ├── graph.py         # GET /graph/query, /graph/stats
│   └── semantic.py      # POST /semantic/search, /semantic/health
└── models/
    ├── le_head.pkl      # Head label encoder
    ├── le_relation.pkl  # Relation label encoder
    ├── le_tail.pkl      # Tail label encoder
    ├── scaler.pkl       # MinMaxScaler
    ├── random_forest.pkl   # RF model (99.5%)
    ├── logistic_regression.pkl  # LR model
    └── feature_cols.pkl # Feature names
```

## Setup

### 1. Create Virtual Environment

```bash
cd v:\Infosys\milestone4-backend
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

Copy `.env.example` to `.env` and fill in real values:

```bash
cp .env.example .env
```

Edit `.env`:

```
NEO4J_URI=neo4j+s://YOUR_ID.databases.neo4j.io
NEO4J_USER=YOUR_USER
NEO4J_PASSWORD=YOUR_PASSWORD

PINECONE_API_KEY=YOUR_API_KEY
PINECONE_INDEX_NAME=semantic-search-index

FLASK_ENV=development
FLASK_DEBUG=1
FLASK_PORT=5000
```

### 4. Export ML Models from Milestone 3

From your Milestone 3 notebook, save the preprocessors:

```python
import pickle

# After training/fitting models
with open('models/le_head.pkl', 'wb') as f:
    pickle.dump(le_head, f)
with open('models/le_relation.pkl', 'wb') as f:
    pickle.dump(le_relation, f)
with open('models/le_tail.pkl', 'wb') as f:
    pickle.dump(le_tail, f)
with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('models/random_forest.pkl', 'wb') as f:
    pickle.dump(model_rf, f)
with open('models/logistic_regression.pkl', 'wb') as f:
    pickle.dump(model_lr, f)
with open('models/feature_cols.pkl', 'wb') as f:
    pickle.dump(feature_cols, f)
```

### 5. Run Server

```bash
python app.py
# OR with auto-reload:
flask --app app run --reload
```

Output:
```
✓ Neo4j connected successfully
✓ Pinecone connected successfully
✓ Embedding model loaded (384-dim)
🚀 Starting server on http://localhost:5000
```

## API Endpoints

### Health Check
```
GET http://localhost:5000/health

Response:
{
    "status": "ok",
    "neo4j": "connected",
    "pinecone": "connected"
}
```

### Graph Query
```
GET http://localhost:5000/graph/query?entity=Obama&relation=born_in&limit=20

Response:
{
    "rows": [
        {"head": "Barack Obama", "relation": "born_in", "tail": "Hawaii"},
        ...
    ],
    "total": 5,
    "error": null
}
```

**Parameters:**
- `entity`: Entity name (partial match, case-insensitive)
- `relation`: Relation type
- `limit`: Max results (default 20, max 100)

### Graph Stats
```
GET http://localhost:5000/graph/stats

Response:
{
    "entities": 13781,
    "relations": 237,
    "connected": true,
    "error": null
}
```

### Semantic Search
```
POST http://localhost:5000/semantic/search
Content-Type: application/json

{
    "query": "Who founded Microsoft?",
    "topK": 3
}

Response:
{
    "matches": [
        {"id": "0", "score": 0.92, "text": "Microsoft was founded by Bill Gates"},
        {"id": "1", "score": 0.84, "text": "Google is headquartered in California"},
        ...
    ],
    "total": 3,
    "error": null
}
```

**Parameters:**
- `query`: Search text (required)
- `topK`: Number of results (default 3, max 10)

### Semantic Health
```
GET http://localhost:5000/semantic/health

Response:
{
    "connected": true,
    "model": "all-MiniLM-L6-v2",
    "dimension": 384,
    "error": null
}
```

## Graceful Degradation

If Neo4j or Pinecone connections fail:
- **Graph queries** return empty results
- **Semantic search** returns mock results with demo data
- **Frontend** shows available data without errors

This allows development/testing even when external services unavailable.

## Testing with cURL

```bash
# Health check
curl http://localhost:5000/health

# Graph query
curl "http://localhost:5000/graph/query?entity=Obama&limit=5"

# Semantic search
curl -X POST http://localhost:5000/semantic/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Who founded Microsoft?","topK":3}'
```

## Integration with Frontend

Update frontend `.env`:

```
VITE_API_BASE_URL=http://localhost:5000
```

Frontend will call:
- `GET http://localhost:5000/graph/query?...`
- `POST http://localhost:5000/semantic/search`

## Production Deployment

1. Set environment variables on server
2. Use production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

3. Use reverse proxy (Nginx) for CORS and load balancing
4. Enable HTTPS with SSL certificate
5. Monitor logs and uptime

## Troubleshooting

**Neo4j not connecting?**
- Check internet connection
- Verify Neo4j cloud instance is running
- Check credentials in .env

**Pinecone empty results?**
- Verify API key is correct
- Check index name matches config
- Ensure embeddings are upserted to index

**CORS errors?**
- Add frontend origin to `Config.API_CORS_ORIGINS` in config.py
- Restart server

## Next Steps

- [ ] Export ML models from Milestone 3 to `/models/` directory
- [ ] Configure real credentials in `.env`
- [ ] Test each endpoint with frontend
- [ ] Deploy to cloud (Heroku, Railway, AWS, etc.)
- [ ] Add authentication layer (JWT tokens)
- [ ] Add request logging and monitoring
