from algorithms.traversal import bfs, dfs, find_cycles


def test_bfs_levels():
    g = {
        "A": [("B", 1), ("C", 1)],
        "B": [("A", 1), ("D", 1), ("E", 1)],
        "C": [("A", 1), ("F", 1)],
        "D": [("B", 1)],
        "E": [("B", 1), ("F", 1)],
        "F": [("C", 1), ("E", 1)],
    }

    order, depth, parent = bfs(g, "A")

    assert depth["D"] == 2
    assert parent["D"] == "B"
    assert order[0] == "A"


def test_bfs_max_depth():
    g = {
        1: [(2, 1)],
        2: [(3, 1)],
        3: [],
    }

    order, depth, parent = bfs(g, 1, max_depth=1)

    assert order == [1, 2]
    assert 3 not in depth
    assert parent[2] == 1


def test_find_cycles():
    g = {
        1: [(2, 1)],
        2: [(3, 1)],
        3: [(1, 1)],
    }

    cycles = find_cycles(g)

    assert len(cycles) == 1
    assert cycles[0] == [1, 2, 3, 1]


def test_dfs_returns_order_and_parent():
    g = {
        "A": [("B", 1), ("C", 1)],
        "B": [("D", 1)],
        "C": [],
        "D": [],
    }

    order, parent = dfs(g, "A")

    assert order[0] == "A"
    assert parent["A"] is None
    assert parent["D"] == "B"
