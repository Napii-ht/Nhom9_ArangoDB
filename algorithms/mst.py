import heapq


class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            return False
        if self.rank[ru] < self.rank[rv]:
            self.parent[ru] = rv
        elif self.rank[ru] > self.rank[rv]:
            self.parent[rv] = ru
        else:
            self.parent[rv] = ru
            self.rank[ru] += 1
        return True


def _chuan_hoa_canh(edges):
    """Hỗ trợ cả cạnh dạng tuple (u, v, w) của nhóm lẫn dict từ ArangoDB."""
    ds_canh = []
    for e in edges:
        if isinstance(e, dict):
            ds_canh.append((e["_from"], e["_to"], e.get("weight", 1), e))
        else:
            u, v = e[0], e[1]
            w = e[2] if len(e) > 2 else 1
            ds_canh.append((u, v, w, (u, v, w)))
    return ds_canh


def kruskal(vertices, edges):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Kruskal + Union-Find.
    Trả về: {"mst_edges": [...], "total_weight": float}
    """
    if not vertices:
        return {"mst_edges": [], "total_weight": 0.0}

    ds_canh = _chuan_hoa_canh(edges)
    ds_canh.sort(key=lambda x: x[2])

    uf = UnionFind(vertices)
    mst_edges = []
    total_weight = 0.0

    for u, v, w, raw_edge in ds_canh:
        if uf.union(u, v):
            mst_edges.append(raw_edge)
            total_weight += w
            if len(mst_edges) == len(vertices) - 1:
                break

    return {"mst_edges": mst_edges, "total_weight": total_weight}


def prim(vertices, edges, start=None):
    """
    Tìm cây khung nhỏ nhất (MST) bằng thuật toán Prim (Min-Heap).
    Trả về: {"mst_edges": [...], "total_weight": float}
    """
    if not vertices:
        return {"mst_edges": [], "total_weight": 0.0}

    start_node = start if start is not None else vertices[0]
    adj = {v: [] for v in vertices}

    for u, v, w, raw_edge in _chuan_hoa_canh(edges):
        if u in adj and v in adj:
            adj[u].append((w, v, raw_edge))
            adj[v].append((w, u, raw_edge))

    visited = {start_node}
    mst_edges = []
    total_weight = 0.0
    min_heap = []

    for w, nb, raw_edge in adj[start_node]:
        heapq.heappush(min_heap, (w, start_node, nb, raw_edge))

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


if __name__ == "__main__":
    v_test = ["A", "B", "C", "D"]
    e_test = [("A", "B", 1), ("B", "C", 2), ("A", "C", 4), ("C", "D", 3), ("B", "D", 5)]

    print("Kruskal:", kruskal(v_test, e_test))
    print("Prim:   ", prim(v_test, e_test, start="A"))
