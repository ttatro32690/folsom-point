from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch
from ..db.database import get_db
from ..db.elasticsearch import get_es_client
from .service import get_health_status

router = APIRouter()

@router.get("/status")
def status(db: Session = Depends(get_db), es: Elasticsearch = Depends(get_es_client)):
    return get_health_status(db, es)
