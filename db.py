from arango import ArangoClient
import config
def connect():
    client = ArangoClient(hosts=config.ARANGO_URL)
    sys_db = client.db("_system", username=config.ARANGO_USER,
                       password=config.ARANGO_PASSWORD)
    if not sys_db.has_database(config.DB_NAME):
        sys_db.create_database(config.DB_NAME)
    return client.db(config.DB_NAME, username=config.ARANGO_USER,
                     password=config.ARANGO_PASSWORD)

def setup_schema(db):
    if not db.has_collection(config.VERTEX_COLLECTION):
        db.create_collection(config.VERTEX_COLLECTION)
    if not db.has_collection(config.EDGE_COLLECTION):
        db.create_collection(config.EDGE_COLLECTION, edge=True)
    if not db.has_graph(config.GRAPH_NAME):
        db.create_graph(config.GRAPH_NAME, edge_definitions=[{
            "edge_collection": config.EDGE_COLLECTION,
            "from_vertex_collections": [config.VERTEX_COLLECTION],
            "to_vertex_collections": [config.VERTEX_COLLECTION],
        }])


def insert_data(db, companies, edges, truncate=True):
    v, e = config.VERTEX_COLLECTION, config.EDGE_COLLECTION
    if truncate:
        db.collection(v).truncate()
        db.collection(e).truncate()
    db.collection(v).import_bulk(companies)
    db.collection(e).import_bulk([
        {"_from": f"{v}/{x['_from']}", "_to": f"{v}/{x['_to']}",
         "weight": x["weight"]} for x in edges
    ])


def _key(doc_id):
    return doc_id.split("/", 1)[1]


def load_graph(db):
    """Trả về (g, shell_nodes). g = {node: [(neighbor, weight), ...]}."""
    v, e = config.VERTEX_COLLECTION, config.EDGE_COLLECTION
    g = {k: [] for k in db.aql.execute(f"FOR c IN {v} RETURN c._key")}
    shell = set(db.aql.execute(
        f"FOR c IN {v} FILTER c.is_shell == true RETURN c._key"))
    for row in db.aql.execute(
            f"FOR x IN {e} RETURN {{f: x._from, t: x._to, w: x.weight}}"):
        g.setdefault(_key(row["f"]), []).append((_key(row["t"]), row["w"]))
    return g, shell
