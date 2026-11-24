import heapq
import time


def dijkstra(graph, start, target):


    bat_dau = time.perf_counter()

    khoang_cach = {}

    for dinh in graph:
        khoang_cach[dinh] = float("inf")

    khoang_cach[start] = 0

    truoc = {}

    hang_doi = [(0, start)]

    while hang_doi:

        kc_hien_tai, u = heapq.heappop(hang_doi)

        if kc_hien_tai > khoang_cach[u]:
            continue

        if u == target:
            break

        for v, trong_so in graph.get(u, []):

            kc_moi = kc_hien_tai + trong_so

            if kc_moi < khoang_cach[v]:

                khoang_cach[v] = kc_moi
                truoc[v] = u

                heapq.heappush(
                    hang_doi,
                    (kc_moi, v)
                )

    thoi_gian = time.perf_counter() - bat_dau


    if khoang_cach[target] == float("inf"):

        return {
            "distance": None,
            "path": None,
            "time": thoi_gian
        }


    duong_di = []
    hien_tai = target

    while hien_tai != start:

        duong_di.append(hien_tai)
        hien_tai = truoc[hien_tai]

    duong_di.append(start)
    duong_di.reverse()

    return {
        "distance": khoang_cach[target],
        "path": duong_di,
        "time": thoi_gian
    }


def bellman_ford(graph, start, target):


    bat_dau = time.perf_counter()

    dinh = list(graph.keys())

    khoang_cach = {}

    for v in dinh:
        khoang_cach[v] = float("inf")

    khoang_cach[start] = 0

    truoc = {}


    for _ in range(len(dinh) - 1):

        co_thay_doi = False

        for u in graph:

            if khoang_cach[u] == float("inf"):
                continue

            for v, trong_so in graph[u]:

                kc_moi = khoang_cach[u] + trong_so

                if kc_moi < khoang_cach[v]:

                    khoang_cach[v] = kc_moi
                    truoc[v] = u
                    co_thay_doi = True


        if not co_thay_doi:
            break


    for u in graph:

        if khoang_cach[u] == float("inf"):
            continue

        for v, trong_so in graph[u]:

            if khoang_cach[u] + trong_so < khoang_cach[v]:

                thoi_gian = time.perf_counter() - bat_dau

                return {
                    "distance": None,
                    "path": None,
                    "time": thoi_gian,
                    "negative_cycle": True
                }

    thoi_gian = time.perf_counter() - bat_dau


    if khoang_cach[target] == float("inf"):

        return {
            "distance": None,
            "path": None,
            "time": thoi_gian,
            "negative_cycle": False
        }


    duong_di = []
    hien_tai = target

    while hien_tai != start:

        duong_di.append(hien_tai)
        hien_tai = truoc[hien_tai]

    duong_di.append(start)
    duong_di.reverse()

    return {
        "distance": khoang_cach[target],
        "path": duong_di,
        "time": thoi_gian,
        "negative_cycle": False
    }


def find_hidden_link(graph, start, target):


    co_canh_truc_tiep = False

    for v, trong_so in graph.get(start, []):

        if v == target:
            co_canh_truc_tiep = True
            break


    if co_canh_truc_tiep:

        return {
            "found": False,
            "start": start,
            "target": target,
            "hidden_link": None,
            "distance": None,
            "path": [start, target],
            "time": 0,
            "reason": "Hai đỉnh có liên kết trực tiếp"
        }


    ket_qua = dijkstra(
        graph,
        start,
        target
    )


    if ket_qua["distance"] is None:

        return {
            "found": False,
            "start": start,
            "target": target,
            "hidden_link": None,
            "distance": None,
            "path": None,
            "time": ket_qua["time"],
            "reason": "Không tồn tại đường đi"
        }

    # Có đường đi gián tiếp
    return {
        "found": True,
        "start": start,
        "target": target,
        "hidden_link": ket_qua["path"],
        "distance": ket_qua["distance"],
        "path": ket_qua["path"],
        "time": ket_qua["time"],
        "reason": "Tồn tại liên kết gián tiếp"
    }


def aql_shortest_path(
    db,
    start,
    target,
    graph_name,
    weight_attribute="weight"
):


    bat_dau = time.perf_counter()

    query = """
    FOR v, e IN OUTBOUND SHORTEST_PATH
        @start TO @target
        GRAPH @graph_name
        OPTIONS {
            weightAttribute: @weight_attribute,
            defaultWeight: 1
        }
        RETURN {
            vertex: v._id,
            edge: e
        }
    """

    ket_qua = list(
        db.aql.execute(
            query,
            bind_vars={
                "start": start,
                "target": target,
                "graph_name": graph_name,
                "weight_attribute": weight_attribute
            }
        )
    )

    thoi_gian = time.perf_counter() - bat_dau


    if not ket_qua:

        return {
            "distance": None,
            "path": None,
            "time": thoi_gian
        }

    duong_di = []
    tong_trong_so = 0

    for item in ket_qua:

        duong_di.append(item["vertex"])

        canh = item["edge"]

        if canh is not None:

            tong_trong_so += canh.get(
                weight_attribute,
                1
            )

    return {
        "distance": tong_trong_so,
        "path": duong_di,
        "time": thoi_gian
    }


def compare_dijkstra(
    db,
    graph,
    start,
    target,
    graph_name,
    weight_attribute="weight"
):


    python_result = dijkstra(
        graph,
        start,
        target
    )

    aql_result = aql_shortest_path(
        db,
        start,
        target,
        graph_name,
        weight_attribute
    )

    return {
        "python": python_result,
        "aql": aql_result,
        "same_distance": (
            python_result["distance"]
            == aql_result["distance"]
        )
    }


if __name__ == "__main__":

  
    graph_test = {
        "A": [
            ("B", 2),
            ("C", 5)
        ],

        "B": [
            ("C", 1),
            ("D", 4)
        ],

        "C": [
            ("D", 2)
        ],

        "D": []
    }



    print("DIJKSTRA")

    kq = dijkstra(
        graph_test,
        "A",
        "D"
    )

    print("Khoảng cách:", kq["distance"])
    print("Đường đi:", " -> ".join(kq["path"]))
    print("Thời gian:", kq["time"])



    print("\nBELLMAN-FORD")

    kq = bellman_ford(
        graph_test,
        "A",
        "D"
    )

    print("Khoảng cách:", kq["distance"])
    print("Đường đi:", " -> ".join(kq["path"]))
    print("Thời gian:", kq["time"])




    kq = find_hidden_link(
        graph_test,
        "A",
        "D"
    )

    if kq["found"]:

        print("\nLiên kết ẩn: Có")
        print(
            "Đường liên kết:",
            " -> ".join(kq["hidden_link"])
        )
        print("Khoảng cách:", kq["distance"])

    else:

        print("Liên kết ẩn: Không")
        print("Lý do:", kq["reason"])


    kq = find_hidden_link(
        graph_test,
        "A",
        "B"
    )

    if kq["found"]:

        print("Liên kết ẩn: Có")
        print(
            "Đường liên kết:",
            " -> ".join(kq["hidden_link"])
        )

    else:

        print("Liên kết ẩn: Không")
        print("Lý do:", kq["reason"])