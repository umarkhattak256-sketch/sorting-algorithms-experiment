import time
import copy
from algorithms import (
    bubble_sort, selection_sort, insertion_sort, merge_sort, 
    quick_sort, heap_sort, python_builtin_sort
)
from data_generation import get_test_sets_for_size

def benchmark_algorithm(func, dataset, iterations=1):
    total_time = 0
    for _ in range(iterations):
        arr_copy = copy.deepcopy(dataset)
        start_time = time.perf_counter()
        func(arr_copy)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    return total_time / iterations

def main():
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort, # Fast
        "Quick Sort": quick_sort, # Fast
        "Heap Sort": heap_sort, # Fast
        "Python Built-in (Timsort)": python_builtin_sort # Baseline
    }

    # As requested: 
    # Small: 20-100 (needs high iterations)
    # Medium: 1000 - 10000
    # Large: 100000+ (O(n^2) algos will take too long, consider skipping for large)
    sizes_config = [
        (50, 1000),      # Size: 50, run 1000 times for meaningful results
        (5000, 5),       # Size: 5000, run 5 times
        (50000, 1)       # Size: 50000, run 1 time (warning: O(n^2) may be very slow)
    ]

    for size, iterations in sizes_config:
        print(f"\n{'='*50}\nBenchmarking List Size: {size} (Averaged over {iterations} runs)\n{'='*50}")
        datasets = get_test_sets_for_size(size)

        for data_type, data in datasets.items():
            print(f"\n--- Data Structure: {data_type} ---")
            for algo_name, algo_func in algorithms.items():
                if size >= 50000 and algo_name in ["Bubble Sort", "Selection Sort", "Insertion Sort"]:
                    print(f"{algo_name:25}: Skipped (O(N^2) too slow for this size)")
                    continue
                try:
                    avg_time = benchmark_algorithm(algo_func, data, iterations)
                    print(f"{algo_name:25}: {avg_time:.6f} seconds")
                except Exception as e:
                    print(f"{algo_name:25}: Error ({e})")

if __name__ == "__main__":
    main()
