import random

def generate_random_list(size, max_val=100000):
    return [random.randint(0, max_val) for _ in range(size)]

def generate_sorted_list(size):
    return list(range(size))

def generate_reverse_sorted_list(size):
    return list(range(size, 0, -1))

def generate_almost_sorted_list(size, swap_count=None):
    if swap_count is None:
        swap_count = size // 50  # 98% sorted logic roughly equivalent to altering 2%
    lst = generate_sorted_list(size)
    for _ in range(max(1, swap_count)):
        i, j = random.sample(range(size), 2)
        lst[i], lst[j] = lst[j], lst[i]
    return lst

def generate_mixed_list(size):
    # e.g., half sorted, half random
    half = size // 2
    lst = generate_sorted_list(half) + generate_random_list(size - half, size)
    return lst

def generate_flat_list(size, unique_vals=5):
    # long lists with few distinct values
    vals = [random.randint(0, 100) for _ in range(unique_vals)]
    return [random.choice(vals) for _ in range(size)]

def get_test_sets_for_size(size):
    return {
        "Random": generate_random_list(size),
        "Sorted": generate_sorted_list(size),
        "Reverse Sorted": generate_reverse_sorted_list(size),
        "Almost Sorted": generate_almost_sorted_list(size),
        "Mixed (Half Sorted)": generate_mixed_list(size),
        "Flat (Few Distinct)": generate_flat_list(size, unique_vals=5)
    }
