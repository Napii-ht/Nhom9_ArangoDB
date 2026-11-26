from collections import deque


def bfs(g, start, max_depth=None):
    """Duyệt BFS từ start. Trả về (order, depth, parent).
    """
    order = []
    depth = {start: 0}
    parent = {start: None}
    hangdoi = deque([start])

    while hangdoi:
        dinh = hangdoi.popleft()
        order.append(dinh)

        if max_depth is not None and depth[dinh] >= max_depth:
            continue

        for ke, _ in g.get(dinh, []):
            if ke not in depth:
                depth[ke] = depth[dinh] + 1
                parent[ke] = dinh
                hangdoi.append(ke)

    return order, depth, parent


def dfs(g, start):
    """Duyệt DFS từ start. Trả về (order, parent)."""
    order = []
    parent = {}
    visited = set()
    nganxep = [(start, None)]

    while nganxep:
        dinh, cha = nganxep.pop()
        if dinh in visited:
            continue

        visited.add(dinh)
        parent[dinh] = cha
        order.append(dinh)

        for ke, _ in reversed(g.get(dinh, [])):
            if ke not in visited:
                nganxep.append((ke, dinh))

    return order, parent


def find_cycles(g):
    """Tìm các chu trình trong đồ thị có hướng bằng DFS ba màu.
    Trắng: chưa thăm; xám: đang nằm trên ngăn xếp DFS;
    đen: đã duyệt xong. Mỗi chu trình được trả về dưới dạng
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}
    parent = {}
    cycles = []
    seen_cycles = set()

    vertices = set(g)
    for neighbors in g.values():
        for ke, _ in neighbors:
            vertices.add(ke)

    def visit(dinh):
        color[dinh] = GRAY

        for ke, _ in g.get(dinh, []):
            state = color.get(ke, WHITE)

            if state == WHITE:
                parent[ke] = dinh
                visit(ke)
            elif state == GRAY:
                path = [dinh]
                current = dinh
                while current != ke:
                    current = parent[current]
                    path.append(current)
                path.reverse()
                cycle = path + [ke]

                body = cycle[:-1]
                if body:
                    rotations = [
                        tuple(body[i:] + body[:i])
                        for i in range(len(body))
                    ]
                    key = min(rotations)
                    if key not in seen_cycles:
                        seen_cycles.add(key)
                        cycles.append(cycle)

        color[dinh] = BLACK

    for dinh in vertices:
        if color.get(dinh, WHITE) == WHITE:
            parent[dinh] = None
            visit(dinh)

    return cycles
    
def find_shell_transfers(g, source, target, shell_nodes,
                         max_depth=4, min_weight=0):
    """BFS tìm các đường chuyển tiền source, target chỉ đi qua
    công ty bình phong. Trả về danh sách đường đi."""
    hangdoi = deque([(source, [source])])
    results = []

    while hangdoi:
        dinh, path = hangdoi.popleft()
        if len(path) - 1 >= max_depth:
            continue

        for ke, w in g.get(dinh, []):
            if w < min_weight or ke in path:
                continue
            if ke == target:
                if len(path) > 1:  
                    results.append(path + [ke])
                continue
            if ke in shell_nodes:
                hangdoi.append((ke, path + [ke]))

    return results
