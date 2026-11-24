import heapq
import time
from arango import ArangoClient
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components

from algorithms.mst import kruskal, prim

st.set_page_config(
    layout="wide", page_title="Demo Phát hiện Gian lận SHTT"
)

def get_sample_dataset():
    vertices = {
        "persons": [
            {"_key": "PER_01", "name": "Nguyễn Văn An", "role": "Nhà sáng chế"},
            {"_key": "PER_02", "name": "Trần Minh Bình", "role": "Cổ đông lớn"},
            {"_key": "PER_03", "name": "Lê Thị Châu", "role": "Giám đốc"},
            {"_key": "PER_04", "name": "Phạm Hoàng Dũng", "role": "Nhà sáng chế"},
            {"_key": "PER_05", "name": "Hoàng Văn Em", "role": "Kỹ sư R&D"},
            {"_key": "PER_06", "name": "Vũ Thị Giang", "role": "Chuyên viên"},
            {"_key": "PER_07", "name": "Đặng Quốc Huy", "role": "Nhà sáng chế"},
            {"_key": "PER_08", "name": "Bùi Văn Khánh", "role": "Người đại diện"},
        ],
        "organizations": [
            {"_key": "ORG_01", "name": "Tập đoàn Công nghệ A", "is_shell": False},
            {"_key": "ORG_02", "name": "Cty Tư vấn Alpha", "is_shell": True},
            {"_key": "ORG_03", "name": "Cty Giải pháp Beta", "is_shell": True},
            {"_key": "ORG_04", "name": "Cty Đầu tư Gamma", "is_shell": False},
            {"_key": "ORG_05", "name": "Cty Cổ phần Delta", "is_shell": False},
            {"_key": "ORG_06", "name": "Viện Nghiên cứu X", "is_shell": False},
            {"_key": "ORG_07", "name": "Cty Sáng tạo Y", "is_shell": False},
        ],
        "patents": [
            {"_key": "PAT_01", "title": "Hệ thống AI #01"},
            {"_key": "PAT_02", "title": "Thuật toán tối ưu #02"},
            {"_key": "PAT_03", "title": "Mô hình dữ liệu #03"},
            {"_key": "PAT_04", "title": "Chip lượng tử #04"},
            {"_key": "PAT_05", "title": "Cảm biến sinh học #05"},
            {"_key": "PAT_06", "title": "Vật liệu nano #06"},
            {"_key": "PAT_07", "title": "Pin thể rắn #07"},
            {"_key": "PAT_08", "title": "Mạng cảm biến #08"},
            {"_key": "PAT_09", "title": "Robot tự hành #09"},
        ],
    }

    edges = {
        "invented": [
            {"_key": "INV_01", "_from": "persons/PER_01", "_to": "patents/PAT_01", "weight": 1.0},
            {"_key": "INV_02", "_from": "persons/PER_02", "_to": "patents/PAT_02", "weight": 1.5},
            {"_key": "INV_03", "_from": "persons/PER_03", "_to": "patents/PAT_03", "weight": 1.5},
            {"_key": "INV_04", "_from": "persons/PER_04", "_to": "patents/PAT_04", "weight": 1.0},
            {"_key": "INV_05", "_from": "persons/PER_02", "_to": "patents/PAT_05", "weight": 2.0},
            {"_key": "INV_06", "_from": "persons/PER_03", "_to": "patents/PAT_06", "weight": 2.0},
            {"_key": "INV_07", "_from": "persons/PER_05", "_to": "patents/PAT_07", "weight": 1.2},
            {"_key": "INV_08", "_from": "persons/PER_06", "_to": "patents/PAT_08", "weight": 1.5},
            {"_key": "INV_09", "_from": "persons/PER_07", "_to": "patents/PAT_09", "weight": 1.0},
        ],
        "owns": [
            {"_key": "OWN_01", "_from": "persons/PER_01", "_to": "organizations/ORG_04", "weight": 1.54},
            {"_key": "OWN_02", "_from": "organizations/ORG_04", "_to": "organizations/ORG_05", "weight": 2.0},
            {"_key": "OWN_03", "_from": "persons/PER_02", "_to": "organizations/ORG_06", "weight": 1.2},
            {"_key": "OWN_04", "_from": "persons/PER_03", "_to": "organizations/ORG_07", "weight": 1.3},
            {"_key": "OWN_05", "_from": "organizations/ORG_06", "_to": "organizations/ORG_07", "weight": 1.5},
            {"_key": "OWN_06", "_from": "persons/PER_04", "_to": "organizations/ORG_01", "weight": 1.1},
            {"_key": "OWN_07", "_from": "persons/PER_08", "_to": "organizations/ORG_02", "weight": 1.0},
            {"_key": "OWN_08", "_from": "persons/PER_08", "_to": "organizations/ORG_03", "weight": 1.0},
        ],
        "cites": [
            {"_key": "CIT_01", "_from": "patents/PAT_01", "_to": "patents/PAT_02", "weight": 1.0},
            {"_key": "CIT_02", "_from": "patents/PAT_02", "_to": "patents/PAT_03", "weight": 1.0},
            {"_key": "CIT_03", "_from": "patents/PAT_03", "_to": "patents/PAT_01", "weight": 1.0},
            {"_key": "CIT_04", "_from": "patents/PAT_05", "_to": "patents/PAT_06", "weight": 1.0},
            {"_key": "CIT_05", "_from": "patents/PAT_07", "_to": "patents/PAT_01", "weight": 1.0},
            {"_key": "CIT_06", "_from": "patents/PAT_08", "_to": "patents/PAT_04", "weight": 1.0},
            {"_key": "CIT_07", "_from": "patents/PAT_09", "_to": "patents/PAT_07", "weight": 1.0},
            {"_key": "CIT_08", "_from": "patents/PAT_06", "_to": "patents/PAT_09", "weight": 1.0},
        ],
        "assigned_to": [
            {"_key": "TR_01", "_from": "patents/PAT_04", "_to": "organizations/ORG_02", "weight": 4.0},
            {"_key": "TR_02", "_from": "organizations/ORG_02", "_to": "organizations/ORG_03", "weight": 3.0},
            {"_key": "TR_03", "_from": "organizations/ORG_03", "_to": "organizations/ORG_01", "weight": 5.0},
            {"_key": "TR_04", "_from": "patents/PAT_05", "_to": "organizations/ORG_06", "weight": 1.4},
            {"_key": "TR_05", "_from": "patents/PAT_06", "_to": "organizations/ORG_07", "weight": 1.6},
            {"_key": "TR_06", "_from": "patents/PAT_07", "_to": "organizations/ORG_04", "weight": 6.0},
            {"_key": "TR_07", "_from": "patents/PAT_08", "_to": "organizations/ORG_05", "weight": 7.0},
        ],
    }
    return vertices, edges


def connect_and_load_db(host, db_name, username, password):
    client = ArangoClient(hosts=host)
    sys_db = client.db("_system", username=username, password=password)
    if not sys_db.has_database(db_name):
        sys_db.create_database(db_name)

    db = client.db(db_name, username=username, password=password)
    v_data, e_data = get_sample_dataset()

    for col, docs in v_data.items():
        if not db.has_collection(col):
            db.create_collection(col)
        db.collection(col).truncate()
        db.collection(col).import_bulk(docs)

    for col, docs in e_data.items():
        if not db.has_collection(col):
            db.create_collection(col, edge=True)
        db.collection(col).truncate()
        db.collection(col).import_bulk(docs)

    all_nodes, all_edges = [], []
    for col in ["persons", "organizations", "patents"]:
        for doc in db.aql.execute(f"FOR v IN {col} RETURN v"):
            doc["group"] = col
            all_nodes.append(doc)
    for col in ["invented", "owns", "cites", "assigned_to"]:
        for doc in db.aql.execute(f"FOR e IN {col} RETURN e"):
            doc["type"] = col
            all_edges.append(doc)
    return all_nodes, all_edges


def load_local_data():
    v_data, e_data = get_sample_dataset()
    nodes, edges = [], []
    for col, docs in v_data.items():
        for d in docs:
            item = d.copy()
            item["_id"] = f"{col}/{d['_key']}"
            item["group"] = col
            nodes.append(item)
    for col, docs in e_data.items():
        for d in docs:
            item = d.copy()
            item["type"] = col
            edges.append(item)
    return nodes, edges

def detect_dfs_cycle(nodes, edges):
    adj = {}
    for e in edges:
        if e["type"] == "cites":
            adj.setdefault(e["_from"], []).append(e)
    color = {n["_id"]: 0 for n in nodes}
    parent_edge = {}
    cycle_keys, cycle_path = [], []

    def dfs(u):
        color[u] = 1
        for edge in adj.get(u, []):
            v = edge["_to"]
            if color[v] == 1:
                cycle_keys.append(edge["_key"])
                curr = u
                path = [v.split("/")[1], u.split("/")[1]]
                while curr != v and curr in parent_edge:
                    pe = parent_edge[curr]
                    cycle_keys.append(pe["_key"])
                    curr = pe["_from"]
                    path.append(curr.split("/")[1])
                path.reverse()
                cycle_path.extend(path)
                return True
            elif color[v] == 0:
                parent_edge[v] = edge
                if dfs(v):
                    return True
        color[u] = 2
        return False

    for n in nodes:
        if color[n["_id"]] == 0 and dfs(n["_id"]):
            break
    return cycle_keys, cycle_path


def detect_bfs_shell(nodes, edges, start_id="patents/PAT_04"):
    shell_ids = {n["_id"] for n in nodes if n.get("is_shell")}
    adj = {}
    for e in edges:
        if e["type"] == "assigned_to":
            adj.setdefault(e["_from"], []).append(e)

    queue = [start_id]
    visited = {start_id}
    parent_edge = {}
    target = None

    while queue:
        u = queue.pop(0)
        for edge in adj.get(u, []):
            v = edge["_to"]
            if v not in visited:
                visited.add(v)
                parent_edge[v] = edge
                queue.append(v)
                if v not in shell_ids and u in shell_ids:
                    target = v
                    break
        if target:
            break

    keys, path = [], []
    if target:
        curr = target
        path.append(curr.split("/")[1])
        while curr in parent_edge:
            pe = parent_edge[curr]
            keys.append(pe["_key"])
            curr = pe["_from"]
            path.append(curr.split("/")[1])
        path.reverse()
        keys.reverse()
    return keys, path


def detect_dijkstra(nodes, edges, start_id, end_id):
    adj = {}
    for e in edges:
        adj.setdefault(e["_from"], []).append(e)
    dist = {n["_id"]: float("inf") for n in nodes}
    parent_edge = {}
    dist[start_id] = 0
    pq = [(0, start_id)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == end_id:
            break
        for edge in adj.get(u, []):
            v, w = edge["_to"], edge["weight"]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent_edge[v] = edge
                heapq.heappush(pq, (dist[v], v))

    keys, path = [], []
    if dist[end_id] < float("inf"):
        curr = end_id
        path.append(curr.split("/")[1])
        while curr in parent_edge:
            pe = parent_edge[curr]
            keys.append(pe["_key"])
            curr = pe["_from"]
            path.append(curr.split("/")[1])
        path.reverse()
        keys.reverse()
    return keys, path, dist[end_id]


def detect_kruskal_cluster(edges):
    cluster_nodes = [
        "persons/PER_02", "persons/PER_03",
        "organizations/ORG_06", "organizations/ORG_07",
        "patents/PAT_05", "patents/PAT_06",
    ]
    sub_edges = [
        e for e in edges
        if e["_from"] in cluster_nodes and e["_to"] in cluster_nodes
    ]
    res = kruskal(cluster_nodes, sub_edges)
    mst_edges, total_w = res["mst_edges"], res["total_weight"]
    return [e["_key"] for e in mst_edges], total_w

st.sidebar.header("1. Khung kết nối ArangoDB")
host_url = st.sidebar.text_input("Host URL", "http://localhost:8529")
db_name = st.sidebar.text_input("Database", "ip_fraud_db")
username = st.sidebar.text_input("Username", "root")
password = st.sidebar.text_input("Password", type="password")

if "nodes" not in st.session_state:
    st.session_state.nodes, st.session_state.edges = load_local_data()
    st.session_state.status = "Đang dùng dữ liệu mẫu cục bộ (24 đỉnh, 32 cạnh)"

if st.sidebar.button("Kết nối & Nạp dữ liệu"):
    try:
        n_db, e_db = connect_and_load_db(host_url, db_name, username, password)
        st.session_state.nodes, st.session_state.edges = n_db, e_db
        st.session_state.status = f"Đã kết nối ArangoDB ({len(n_db)} đỉnh, {len(e_db)} cạnh)"
        st.sidebar.success("Kết nối thành công!")
    except Exception as err:
        st.sidebar.warning(f"Chưa kết nối được DB ({err}). Đang dùng dữ liệu cục bộ.")

st.sidebar.caption(st.session_state.status)
st.sidebar.markdown("---")

st.sidebar.header("2. Chọn mẫu gian lận")
scenario = st.sidebar.radio(
    "Kịch bản kiểm tra:",
    [
        "Hiển thị toàn bộ đồ thị",
        "Mẫu 1: Trích dẫn vòng tròn (DFS)",
        "Mẫu 2: Chuyển nhượng công ty bình phong (BFS)",
        "Mẫu 3: Liên kết ẩn 2 thực thể (Dijkstra)",
        "Mẫu 4: Bộ khung cụm nghi vấn (Kruskal MST)",
    ],
)

nodes = st.session_state.nodes
edges = st.session_state.edges
node_ids = [n["_id"] for n in nodes]

start_id, end_id = "persons/PER_01", "organizations/ORG_05"
if "Mẫu 3" in scenario:
    start_id = st.sidebar.selectbox("Thực thể nguồn:", node_ids, index=node_ids.index("persons/PER_01"))
    end_id = st.sidebar.selectbox("Thực thể đích:", node_ids, index=node_ids.index("organizations/ORG_05"))

red_edge_keys = []
log_message = ""
aql_query = ""

t0 = time.perf_counter()
if "Mẫu 1" in scenario:
    red_edge_keys, path = detect_dfs_cycle(nodes, edges)
    log_message = f"[DFS] Phát hiện trích dẫn vòng tròn: {' -> '.join(path)}\nCạnh nghi vấn: {red_edge_keys}"
    aql_query = "FOR v IN patents\n  FOR t, e, p IN 2..4 OUTBOUND v cites\n    FILTER t._id == v._id RETURN p"
elif "Mẫu 2" in scenario:
    red_edge_keys, path = detect_bfs_shell(nodes, edges)
    log_message = f"[BFS] Chuyển nhượng qua công ty bình phong: {' -> '.join(path)}\nCạnh nghi vấn: {red_edge_keys}"
    aql_query = "FOR v, e, p IN 1..4 OUTBOUND 'patents/PAT_04' assigned_to\n  OPTIONS { bfs: true, uniqueVertices: 'global' }\n  FILTER v.is_shell == false AND LENGTH(p.edges) > 1 RETURN p"
elif "Mẫu 3" in scenario:
    red_edge_keys, path, total_w = detect_dijkstra(nodes, edges, start_id, end_id)
    log_message = f"[Dijkstra] Liên kết ngắn nhất: {' -> '.join(path)} (Tổng trọng số = {total_w:.2f})\nCạnh nghi vấn: {red_edge_keys}"
    aql_query = f"FOR v, e IN OUTBOUND SHORTEST_PATH '{start_id}' TO '{end_id}'\n  GRAPH 'ip_fraud_graph' OPTIONS {{ weightAttribute: 'weight' }}\n  RETURN {{ vertex: v._key, edge: e._key }}"
elif "Mẫu 4" in scenario:
    red_edge_keys, total_w = detect_kruskal_cluster(edges)
    log_message = f"[Kruskal MST] Cây khung cụm nghi vấn gồm 5 cạnh: {red_edge_keys}\nTổng trọng số = {total_w:.2f}"
    aql_query = "FOR e IN UNION((FOR x IN invented RETURN x), (FOR x IN owns RETURN x), (FOR x IN cites RETURN x), (FOR x IN assigned_to RETURN x))\n  SORT e.weight ASC RETURN e"
else:
    log_message = f"Toàn bộ đồ thị: {len(nodes)} đỉnh và {len(edges)} cạnh."
    aql_query = "FOR v IN UNION((FOR p IN persons RETURN p), (FOR o IN organizations RETURN o), (FOR pt IN patents RETURN pt)) RETURN v"

exec_ms = (time.perf_counter() - t0) * 1000

st.title("Hệ thống Phát hiện Gian lận trong Sở hữu Trí tuệ")
net = Network(height="460px", width="100%", directed=True, bgcolor="#ffffff")
net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=140)

color_map = {"persons": "#4A90E2", "organizations": "#F5A623", "patents": "#7ED321"}
for n in nodes:
    label = f"{n['_key']}\n({n.get('name', n.get('title', ''))[:15]})"
    net.add_node(n["_id"], label=label, color=color_map[n["group"]], size=22)

for e in edges:
    is_fraud = e["_key"] in red_edge_keys
    net.add_edge(
        e["_from"],
        e["_to"],
        label=f"{e['type']} ({e['weight']})",
        color="#FF0000" if is_fraud else "#CCCCCC",
        width=4.0 if is_fraud else 1.2,
    )

net.save_graph("graph_view.html")
with open("graph_view.html", "r", encoding="utf-8") as f:
    components.html(f.read(), height=480)

col_log, col_aql = st.columns([1.2, 1])
with col_log:
    st.subheader("Khung kết quả & Nhật ký (Log)")
    st.info(f"Thời gian thực thi: {exec_ms:.3f} ms")
    st.code(log_message, language="text")
with col_aql:
    st.subheader("Truy vấn AQL đối chiếu")
    st.code(aql_query, language="sql")