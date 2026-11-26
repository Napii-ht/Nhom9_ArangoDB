import random
from models import Graph, PlantedPatterns

def generate(n_vertices=100, n_edges=300, seed=42):
    rng = random.Random(seed)
    companies = [{"_key": f"C{i}", "name": f"Cong ty {i}", "is_shell": False}
                 for i in range(n_vertices)]
    edges, seen = [], set()
    tries = 0
    while len(edges) < n_edges and tries < n_edges * 20:
        tries += 1
        a, b = sorted(rng.sample(range(n_vertices), 2))
        if (a, b) in seen:
            continue
        seen.add((a, b))
        edges.append({"_from": f"C{a}", "_to": f"C{b}",
                      "weight": rng.randint(1, 100)})

    planted = PlantedPatterns()

    def add_nodes(keys, shell=False):
        for k in keys:
            companies.append({"_key": k, "name": k, "is_shell": shell})

    def add_path(keys, w):
        for a, b in zip(keys, keys[1:]):
            edges.append({"_from": a, "_to": b, "weight": w})

    cyc = ["CYC1", "CYC2", "CYC3"]
    add_nodes(cyc)
    add_path(cyc + [cyc[0]], 50)
    planted.cycles.append(cyc)

    shells = ["SHELL1", "SHELL2"]
    add_nodes(["SRC", "DST"])
    add_nodes(shells, shell=True)
    chain = ["SRC"] + shells + ["DST"]
    add_path(chain, 80)
    planted.shell_chains.append(chain)
    planted.shell_nodes.update(shells)

    hid = ["HID_X", "HID_M1", "HID_M2", "HID_Y"]
    add_nodes(hid)
    add_path(hid, 1)
    planted.hidden_links.append((hid[0], hid[-1]))

    for target in ("CYC1", "SRC", "HID_X"):
        edges.append({"_from": f"C{rng.randrange(n_vertices)}",
                      "_to": target, "weight": rng.randint(1, 100)})

    return companies, edges, planted


def build_graph(companies, edges) -> Graph:
    """Dựng g = {node: [(neighbor, weight), ...]} từ danh sách cạnh."""
    g = {c["_key"]: [] for c in companies}
    for e in edges:
        g[e["_from"]].append((e["_to"], e["weight"]))
    return g


def shell_set(companies):
    return {c["_key"] for c in companies if c.get("is_shell")}
