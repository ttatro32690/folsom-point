from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch

def get_health_status(db: Session, es: Elasticsearch):
    status_info = {
        "database": {
            "status": "unknown",
            "details": None
        },
        "elasticsearch": {
            "status": "unknown",
            "details": None
        }
    }

    # Check database connection
    try:
        db.execute("SELECT 1")
        status_info["database"]["status"] = "connected"
        status_info["database"]["details"] = "Successfully connected to the database"
    except Exception as e:
        status_info["database"]["status"] = "error"
        status_info["database"]["details"] = f"Failed to connect to the database: {str(e)}"

    # Check Elasticsearch connection
    try:
        if es.ping():
            status_info["elasticsearch"]["status"] = "connected"
            cluster_health = es.cluster.health()
            status_info["elasticsearch"]["details"] = {
                "cluster_name": cluster_health["cluster_name"],
                "status": cluster_health["status"],
                "number_of_nodes": cluster_health["number_of_nodes"],
                "active_primary_shards": cluster_health["active_primary_shards"]
            }
        else:
            status_info["elasticsearch"]["status"] = "error"
            status_info["elasticsearch"]["details"] = "Failed to connect to Elasticsearch"
    except Exception as e:
        status_info["elasticsearch"]["status"] = "error"
        status_info["elasticsearch"]["details"] = f"Failed to connect to Elasticsearch: {str(e)}"

    return status_info
