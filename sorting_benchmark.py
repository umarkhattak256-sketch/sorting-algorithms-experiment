"""
Experimental Comparison of Sorting Algorithms
MPI(L)2026 Paper — Benchmark Code
"""

import random
import time
import copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv

# ─────────────────────────────────────────────
# Sorting Algorithm Implementations
# ─────────────────────────────────────────────

def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def selection_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr):
    a = arr[:]
    _quick_sort(a, 0, len(a) - 1)
    return a

def _quick_sort(a, low, high):
    if low < high:
        pi = _partition(a, low, high)
        _quick_sort(a, low, pi - 1)
        _quick_sort(a, pi + 1, high)

def _partition(a, low, high):
    # Median-of-three pivot
    mid = (low + high) // 2
    if a[mid] < a[low]:
        a[low], a[mid] = a[mid], a[low]
    if a[high] < a[low]:
        a[low], a[high] = a[high], a[low]
    if a[mid] < a[high]:
        a[mid], a[high] = a[high], a[mid]
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1

def heap_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i)
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        _heapify(a, i, 0)
    return a

def _heapify(a, n, i):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and a[l] > a[largest]:
        largest = l
    if r < n and a[r] > a[largest]:
        largest = r
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        _heapify(a, n, largest)

def shell_sort(arr):
    a = arr[:]
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a

def counting_sort(arr):
    if not arr:
        return []
    a = arr[:]
    min_val, max_val = min(a), max(a)
    count = [0] * (max_val - min_val + 1)
    for x in a:
        count[x - min_val] += 1
    result = []
    for i, c in enumerate(count):
        result.extend([i + min_val] * c)
    return result

def radix_sort(arr):
    a = arr[:]
    if not a:
        return a
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        a = _counting_sort_by_digit(a, exp)
        exp *= 10
    return a

def _counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in arr:
        index = (i // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output

def tim_sort(arr):
    # Python's built-in sort uses Timsort
    a = arr[:]
    a.sort()
    return a

# ─────────────────────────────────────────────
# Benchmarking
# ─────────────────────────────────────────────

ALGORITHMS = {
    "Bubble Sort":    bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Shell Sort":     shell_sort,
    "Merge Sort":     merge_sort,
    "Heap Sort":      heap_sort,
    "Quick Sort":     quick_sort,
    "Counting Sort":  counting_sort,
    "Radix Sort":     radix_sort,
    "Tim Sort":       tim_sort,
}

# Sizes — skip large sizes for O(n^2) algorithms
SIZES = [100, 500, 1000, 2000, 5000, 10000]
SLOW_LIMIT = 5000  # bubble/selection/insertion skip sizes >= this
REPEATS = 5

INPUT_TYPES = {
    "random":         lambda n: random.sample(range(n * 10), n),
    "sorted":         lambda n: list(range(n)),
    "reverse_sorted": lambda n: list(range(n, 0, -1)),
    "nearly_sorted":  lambda n: _nearly_sorted(n),
}

def _nearly_sorted(n):
    a = list(range(n))
    swaps = max(1, n // 20)
    for _ in range(swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        a[i], a[j] = a[j], a[i]
    return a

def benchmark():
    results = {}  # results[algo][input_type][size] = avg_time
    slow_algos = {"Bubble Sort", "Selection Sort", "Insertion Sort"}

    for name, func in ALGORITHMS.items():
        results[name] = {}
        for itype, gen in INPUT_TYPES.items():
            results[name][itype] = {}
            for n in SIZES:
                if name in slow_algos and n >= SLOW_LIMIT:
                    results[name][itype][n] = None
                    continue
                times = []
                for _ in range(REPEATS):
                    data = gen(n)
                    t0 = time.perf_counter()
                    func(data)
                    times.append(time.perf_counter() - t0)
                results[name][itype][n] = sum(times) / len(times)
                print(f"  {name:16s} | {itype:14s} | n={n:6d} | {results[name][itype][n]*1000:.3f} ms")
    return results

def save_csv(results):
    rows = []
    for algo, itypes in results.items():
        for itype, sizes in itypes.items():
            for n, t in sizes.items():
                rows.append({"algorithm": algo, "input_type": itype, "n": n,
                             "avg_time_sec": t if t is not None else "N/A"})
    with open("/home/claude/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["algorithm", "input_type", "n", "avg_time_sec"])
        writer.writeheader()
        writer.writerows(rows)
    print("Saved results.csv")

def plot_results(results):
    COLORS = [
        '#e6194b','#3cb44b','#4363d8','#f58231','#911eb4',
        '#42d4f4','#f032e6','#bfef45','#fabed4','#469990'
    ]
    input_types = list(INPUT_TYPES.keys())
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for ax_idx, itype in enumerate(input_types):
        ax = axes[ax_idx]
        for color, (name, itypes) in zip(COLORS, results.items()):
            xs, ys = [], []
            for n in SIZES:
                t = itypes[itype][n]
                if t is not None:
                    xs.append(n)
                    ys.append(t * 1000)
            if xs:
                ax.plot(xs, ys, marker='o', label=name, color=color, linewidth=1.8)
        ax.set_title(itype.replace("_", " ").title(), fontsize=12, fontweight='bold')
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Time (ms)")
        ax.legend(fontsize=7, loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

    fig.suptitle("Sorting Algorithm Benchmark Comparison", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig("/home/claude/benchmark_plot.pdf", dpi=150, bbox_inches='tight')
    plt.savefig("/home/claude/benchmark_plot.png", dpi=150, bbox_inches='tight')
    print("Saved benchmark_plot.pdf and benchmark_plot.png")

if __name__ == "__main__":
    print("Running benchmarks...")
    results = benchmark()
    save_csv(results)
    plot_results(results)
    print("Done.")
