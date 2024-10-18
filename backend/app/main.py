from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db.database import get_db
from .db.elasticsearch import get_es_client
from elasticsearch import Elasticsearch

app = FastAPI(title="AI-Enabled Agent Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Enabled Agent Platform"}

@app.get("/db-test")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"message": "Successfully connected to the database"}
    except Exception as e:
        return {"message": f"Failed to connect to the database: {str(e)}"}

@app.get("/es-test")
def test_es(es: Elasticsearch = Depends(get_es_client)):
    try:
        # Try to ping the Elasticsearch cluster
        if es.ping():
            return {"message": "Successfully connected to Elasticsearch"}
        else:
            return {"message": "Failed to connect to Elasticsearch"}
    except Exception as e:
        return {"message": f"Failed to connect to Elasticsearch: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
