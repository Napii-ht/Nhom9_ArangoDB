import time

from shortest_path import (
    dijkstra,
    aql_shortest_path
)


def benchmark_dijkstra(
    graph,
    start,
    target,
    so_lan=10
):


    danh_sach_thoi_gian = []
    ket_qua = None

    for _ in range(so_lan):

        bat_dau = time.perf_counter()

        ket_qua = dijkstra(
            graph,
            start,
            target
        )

        thoi_gian = time.perf_counter() - bat_dau

        danh_sach_thoi_gian.append(
            thoi_gian * 1000
        )

    thoi_gian_tb = (
        sum(danh_sach_thoi_gian)
        / len(danh_sach_thoi_gian)
    )

    return {
        "time_ms": thoi_gian_tb,
        "distance": ket_qua["distance"],
        "path": ket_qua["path"]
    }


def benchmark_aql(
    db,
    start,
    target,
    graph_name,
    weight_attribute="weight",
    so_lan=10
):


    danh_sach_thoi_gian = []
    ket_qua = None

    for _ in range(so_lan):

        ket_qua = aql_shortest_path(
            db,
            start,
            target,
            graph_name,
            weight_attribute
        )

        danh_sach_thoi_gian.append(
            ket_qua["time"] * 1000
        )

    thoi_gian_tb = (
        sum(danh_sach_thoi_gian)
        / len(danh_sach_thoi_gian)
    )

    return {
        "time_ms": thoi_gian_tb,
        "distance": ket_qua["distance"],
        "path": ket_qua["path"]
    }


def run_benchmark(
    db,
    graph,
    graph_name,
    start,
    target,
    weight_attribute="weight",
    so_lan=10
):
    """
    Chạy benchmark Python và AQL.
    """

    python_result = benchmark_dijkstra(
        graph,
        start,
        target,
        so_lan
    )

    aql_result = benchmark_aql(
        db,
        start,
        target,
        graph_name,
        weight_attribute,
        so_lan
    )

    return {
        "python": python_result,
        "aql": aql_result,
        "same_distance": (
            python_result["distance"]
            == aql_result["distance"]
        )
    }


def print_benchmark(
    ten_dataset,
    so_dinh,
    so_canh,
    ket_qua
):

    print("\n========================================")
    print("DATASET:", ten_dataset)
    print("Số đỉnh:", so_dinh)
    print("Số cạnh:", so_canh)
    print("========================================")

    print(
        "Python Dijkstra:",
        round(
            ket_qua["python"]["time_ms"],
            4
        ),
        "ms"
    )

    print(
        "AQL SHORTEST_PATH:",
        round(
            ket_qua["aql"]["time_ms"],
            4
        ),
        "ms"
    )

    print(
        "Khoảng cách Python:",
        ket_qua["python"]["distance"]
    )

    print(
        "Khoảng cách AQL:",
        ket_qua["aql"]["distance"]
    )

    print(
        "Kết quả giống nhau:",
        ket_qua["same_distance"]
    )

    print(
        "Đường đi Python:",
        ket_qua["python"]["path"]
    )

    print(
        "Đường đi AQL:",
        ket_qua["aql"]["path"]
    )


if __name__ == "__main__":

    # Đồ thị kiểm tra Python
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

    ket_qua_python = benchmark_dijkstra(
        graph_test,
        "A",
        "D",
        so_lan=10
    )

    print(
        "Thời gian trung bình:",
        round(
            ket_qua_python["time_ms"],
            4
        ),
        "ms"
    )

    print(
        "Khoảng cách:",
        ket_qua_python["distance"]
    )

    print(
        "Đường đi:",
        ket_qua_python["path"]
    )