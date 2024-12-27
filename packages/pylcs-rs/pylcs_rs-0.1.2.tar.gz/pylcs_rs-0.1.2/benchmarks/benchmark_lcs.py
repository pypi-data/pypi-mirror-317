import timeit
import statistics
from typing import Tuple, List
import pylcs
import pylcs_rs


def generate_test_cases() -> List[Tuple[str, str]]:
    return [
        ("aaa", "aabbbaa"),  # 小さいケース
        ("aaa你好", "你好呀"),  # Unicode文字
        ("a" * 1000, "a" * 1000 + "b" * 100),  # 長い一致
        ("abc" * 500, "cba" * 500),  # 繰り返しパターン
        ("hello world" * 100, "world hello" * 100),  # 中程度のケース
        (
            "".join([chr(i) for i in range(65, 91)]) * 20,  # アルファベット
            "".join([chr(i) for i in range(90, 64, -1)]) * 20,
        ),
    ]


def run_benchmark(func, s1: str, s2: str, iterations: int = 5) -> Tuple[float, float]:
    times = []
    for _ in range(iterations):
        start = timeit.default_timer()
        result = func(s1, s2)
        end = timeit.default_timer()
        times.append(end - start)
    return statistics.mean(times), statistics.stdev(times)


def main():
    test_cases = generate_test_cases()
    print(f"{'Input Sizes':<30} | {'pylcs_rs':<20} | {'pylcs':<20}")
    print("-" * 72)

    for s1, s2 in test_cases:
        sizes = f"({len(s1)}, {len(s2)})"

        rs_mean, rs_std = run_benchmark(pylcs_rs.lcs, s1, s2)
        py_mean, py_std = run_benchmark(pylcs.lcs, s1, s2)

        print(
            f"{sizes:<30} | {rs_mean:>8.6f} ±{rs_std:>8.6f} | {py_mean:>8.6f} ±{py_std:>8.6f}"
        )


if __name__ == "__main__":
    main()
