import os

ARANGO_URL = os.getenv("ARANGO_URL", "http://localhost:8529")
ARANGO_USER = os.getenv("ARANGO_USER", "root")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "fraud_db")

VERTEX_COLLECTION = "companies"      
EDGE_COLLECTION = "transactions"    
GRAPH_NAME = "fraud_graph"
SIZES = {
    "small": (100, 300),
    "medium": (1_000, 5_000),
    "large": (10_000, 50_000),
}
SEED = 42
