from collections import defaultdict, deque


def greedy_coloring(vertices, edges, order=None):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)

    ds_duyet = order if order is not None else sorted(vertices, key=lambda v: len(adj[v]), reverse=True)
    mau = {}

    for v in ds_duyet:
        mau_da_dung = {mau[nb] for nb in adj[v] if nb in mau}
        c = 0
        while c in mau_da_dung:
            c += 1
        mau[v] = c

    return mau


def _kiem_tra_lien_thong(vertices, edges):
    adj = {v: set() for v in vertices}
    co_canh = set()

    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
        co_canh.add(u)
        co_canh.add(v)

    if len(co_canh) <= 1:
        return True

    start = next(iter(co_canh))
    visited = {start}
    q = deque([start])

    while q:
        curr = q.popleft()
        for nxt in adj[curr]:
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)

    return co_canh.issubset(visited)


def check_euler(vertices, edges, directed=False):
    if not edges:
        return {"type": "none", "reason": "Khong co canh"}

    if not _kiem_tra_lien_thong(vertices, edges):
        return {"type": "none", "reason": "Do thi khong lien thong"}

    if not directed:
        deg = {v: 0 for v in vertices}
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1

        bac_le = [v for v, d in deg.items() if d % 2 == 1]
        if len(bac_le) == 0:
            return {"type": "eulerian", "start": edges[0][0]}
        elif len(bac_le) == 2:
            return {"type": "semi-eulerian", "start": bac_le[0]}
        else:
            return {"type": "none", "reason": "So dinh bac le khong hop le"}

    in_deg = {v: 0 for v in vertices}
    out_deg = {v: 0 for v in vertices}
    for u, v in edges:
        out_deg[u] += 1
        in_deg[v] += 1

    dinh_bat_dau = []
    dinh_ket_thuc = []
    for v in vertices:
        hieu = out_deg[v] - in_deg[v]
        if hieu == 1:
            dinh_bat_dau.append(v)
        elif hieu == -1:
            dinh_ket_thuc.append(v)
        elif hieu != 0:
            return {"type": "none", "reason": "Lech bac vao ra"}

    if len(dinh_bat_dau) == 0 and len(dinh_ket_thuc) == 0:
        return {"type": "eulerian", "start": edges[0][0]}
    elif len(dinh_bat_dau) == 1 and len(dinh_ket_thuc) == 1:
        return {"type": "semi-eulerian", "start": dinh_bat_dau[0]}
    else:
        return {"type": "none", "reason": "Khong thoa dieu kien Euler"}


def find_euler_path(vertices, edges, directed=False):
    tt = check_euler(vertices, edges, directed=directed)
    if tt["type"] == "none":
        return None

    start = tt["start"]
    ke = defaultdict(list)
    for idx, (u, v) in enumerate(edges):
        ke[u].append((v, idx))
        if not directed:
            ke[v].append((u, idx))

    da_di_canh = [False] * len(edges)
    stack = [start]
    ket_qua = []

    while stack:
        curr = stack[-1]
        while ke[curr] and da_di_canh[ke[curr][-1][1]]:
            ke[curr].pop()

        if ke[curr]:
            nxt, eid = ke[curr].pop()
            da_di_canh[eid] = True
            stack.append(nxt)
        else:
            ket_qua.append(stack.pop())

    ket_qua.reverse()
    if len(ket_qua) != len(edges) + 1:
        return None
    return ket_qua


def find_hamiltonian_path(vertices, edges, directed=False, cycle=False, limit=12):
    n = len(vertices)
    if n > limit:
        raise ValueError("Hamilton la NP-day-du, chi chay do thi nho")
    if cycle and n < 3:
        return None
    if n == 0:
        return None
    if n == 1:
        return [vertices[0]] if not cycle else None

    adj = {v: set() for v in vertices}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            if not directed:
                adj[v].add(u)

    visited = set()

    def quay_lui(path):
        if len(path) == n:
            if not cycle:
                return path[:]
            if path[0] in adj[path[-1]]:
                return path + [path[0]]
            return None

        curr = path[-1]
        for nxt in vertices:
            if nxt not in visited and nxt in adj[curr]:
                visited.add(nxt)
                path.append(nxt)

                kq = quay_lui(path)
                if kq is not None:
                    return kq

                path.pop()
                visited.remove(nxt)

        return None
    
    for s in (vertices[:1] if cycle else vertices):
        visited.clear()
        visited.add(s)
        res = quay_lui([s])
        if res is not None:
            return res

    return None

def graph_to_edges(g):
    vertices = list(g)
    edges = list({tuple(sorted((u, v))) for u in g for v, _ in g[u]})
    return vertices, edges

if __name__ == "__main__":
    v_test = ["A", "B", "C", "D"]
    e_test = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]

    print("Coloring:", greedy_coloring(v_test, e_test))
    print("Euler check:", check_euler(v_test, e_test))
    print("Euler path:", find_euler_path(v_test, e_test))
    print("Hamilton path:", find_hamiltonian_path(v_test, e_test, cycle=False))
    print("Hamilton cycle:", find_hamiltonian_path(v_test, e_test, cycle=True))
