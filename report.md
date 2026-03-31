# Experimental Comparison of Sorting Algorithms

## 1. Introduction
This project aims to experimentally compare the performance of various sorting algorithms. The algorithms involved span those traditionally taught in "Algorithms and Data Structures 1" (such as Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, and Heap Sort). Additionally, Python's built-in `Timsort` is included as a baseline comparison.

## 2. Experimental Setup
### 2.1 Algorithms Implemented
1. **$O(N^2)$ Algorithms:** Bubble Sort, Selection Sort, Insertion Sort.
2. **$O(N \log N)$ Algorithms:** Merge Sort, Quick Sort, Heap Sort.
3. **Advanced ($O(N \log N)$ average/best):** Timsort (`sorted()` in Python).

### 2.2 Test Data Organization
Different types of input data were generated to thoroughly test the algorithms:
- **Lengths:**
  - **Small (~50):** Ran thousands of times to ensure times are meaningful and measurable.
  - **Medium (~5000):** Ran a few times.
  - **Large (50000+):** Ran once; $O(N^2)$ algorithms are mostly skipped at this scale due to extreme time constraints.
- **Structures:**
  - **Random:** Unordered uniform distribution of integers.
  - **Sorted:** Ascending order.
  - **Reverse Sorted:** Descending order.
  - **Almost Sorted:** ~98% of the list is in ascending order.
  - **Mixed (Half Sorted):** First half is sorted, second half is random.
  - **Flat (Few Distinct Values):** Long lists containing only a few unique values.
- **Data Types Used:** Lists of Integers (Python lists act as dynamic arrays).

## 3. Results and Observations
The experiment was run locally handling array lengths grouped into Small (50 items), Medium (5000 items), and Large (50,000 items). Based on the execution benchmarks:

- **Small Inputs (e.g., 50 elements, averaged over 1000 runs):**
  - **Observation:** On extremely small arrays, algorithms with simple logic (like Insertion Sort taking ~0.000038s) compete very closely with computationally complex ones like Merge/Quick Sort (taking ~0.000041s).
  - **Expectation Met?** Yes. Setup and recursion logic in fast algorithms induce overhead.
- **Medium/Large Inputs (e.g., 5000 and 50000 elements):**
  - **Observation:** $O(N \log N)$ algorithms aggressively dominate. Bubble Sort on 5000 random items took ~0.73s, while Quick Sort took ~0.006s. At size 50,000, $O(N^2)$ algorithms are skipped entirely because their predicted time spikes to over 10+ minutes per iteration.
- **Sorted & Almost Sorted Lists:**
  - **Observation:** Insertion Sort drops to near $O(N)$ execution bounds, completing instantly (0.000003s) compared to random sets. Adaptive approaches capitalize on the existing order.
- **Reverse Sorted Data:**
  - **Observation:** Bubble and Insertion Sort double or triple in sorting time, demonstrating their full worst-case bounds.
- **Timsort (Python baseline):**
  - **Observation:** Python's heavily optimized internal array `list.sort()` is consistently faster than all manual python implementations by a factor of 10-30x, partly because it runs in compiled C rather than interpreted Python.

## 4. Conclusion
The experiment verified the theoretical time complexities of the standard algorithms. Simple algorithms ($O(N^2)$) are practically unusable for large datasets but offer low overhead for small lists. Structural properties (like being nearly sorted) drastically change the real-world execution time, favoring adaptive algorithms like Insertion Sort or Timsort.

## 5. Repository
Code/data can be found at: [Insert your GitHub Link Here]
