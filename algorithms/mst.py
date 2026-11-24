import heapq


def _chuan_hoa_canh(edges):
    """Chuyển đổi các cạnh đầu vào (tuple/list hoặc dict từ ArangoDB) về dạng (u, v, weight, raw_edge)."""
    ds_canh = []
    for e in edges:
        if isinstance(e, dict):
            w = e.get("weight")
            if w is None:
                w = 1
            ds_canh.append((e["_from"], e["_to"], w, e))
        else:
            w = e[2] if len(e) >= 3 else 1
            if w is None:
                w = 1
            ds_canh.append((e[0], e[1], w, e))
    return ds_canh


class UnionFind:
    """Cấu trúc dữ liệu Disjoint Set Union (tối ưu Path Compression & Union by Rank)."""

    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u == root_v:
            return False
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
        return True


def kruskal(vertices, edges):
    """Thuật toán Kruskal tìm Cây khung nhỏ nhất (MST) bằng Union-Find."""
    if not vertices:
        return {"mst_edges": [], "total_weight": 0.0, "connected": True}

    ds_canh = _chuan_hoa_canh(edges)
    ds_canh.sort(key=lambda item: item[2])

    uf = UnionFind(vertices)
    mst_edges = []
    total_weight = 0.0

    for u, v, w, raw_edge in ds_canh:
        if u in uf.parent and v in uf.parent and uf.union(u, v):
            mst_edges.append(raw_edge)
            total_weight += w
            if len(mst_edges) == len(vertices) - 1:
                break

    return {
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "connected": len(mst_edges) == len(vertices) - 1,
    }


def prim(vertices, edges, start=None):
    """Thuật toán Prim tìm Cây khung nhỏ nhất (MST) bằng Min-Heap."""
    if not vertices:
        return {"mst_edges": [], "total_weight": 0.0}

    adj = {v: [] for v in vertices}
    for u, v, w, raw_edge in _chuan_hoa_canh(edges):
        if u in adj and v in adj:
            adj[u].append((w, v, raw_edge))
            adj[v].append((w, u, raw_edge))

    start_node = start if (start is not None and start in adj) else vertices[0]
    visited = {start_node}
    min_heap = []

    for w, nxt, raw_edge in adj[start_node]:
        heapq.heappush(min_heap, (w, start_node, nxt, raw_edge))

    mst_edges = []
    total_weight = 0.0

    while min_heap and len(visited) < len(vertices):
        w, u, v, raw_edge = heapq.heappop(min_heap)
        if v in visited:
            continue

        visited.add(v)
        mst_edges.append(raw_edge)
        total_weight += w

        for next_w, nxt, next_raw in adj[v]:
            if nxt not in visited:
                heapq.heappush(min_heap, (next_w, v, nxt, next_raw))

    return {"mst_edges": mst_edges, "total_weight": total_weight}


def graph_to_weighted_edges(g):
    """Đổi Graph (danh sách kề) sang (vertices, edges) vô hướng, bỏ trùng u-v / v-u."""
    vertices = list(g)
    seen = {}
    for u in g:
        for v, w in g[u]:
            key = tuple(sorted((u, v)))
            if key not in seen or w < seen[key]:
                seen[key] = w
    return vertices, [(a, b, w) for (a, b), w in seen.items()]