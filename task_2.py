def binary_search(arr: list[float], target: float) -> tuple[int, float]:

    left = 0
    right = len(arr) - 1
    iterations = 0

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # If we haven't found the exact value, return the upper bound
    if left < len(arr):
        return iterations, arr[left]
    else:
        # If target is greater than all elements
        return iterations, float('inf')


# Example usage
if __name__ == "__main__":
    # Test with a sorted array of fractional numbers
    test_array = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]

    # Test case 1: Element exists in array
    target1 = 4.4
    iterations1, upper_bound1 = binary_search(test_array, target1)
    print(f"Searching for {target1}:")
    print(f"Number of iterations: {iterations1}")
    print(f"Upper bound: {upper_bound1}")

    # Test case 2: Element doesn't exist, but upper bound exists
    target2 = 4.5
    iterations2, upper_bound2 = binary_search(test_array, target2)
    print(f"\nSearching for {target2}:")
    print(f"Number of iterations: {iterations2}")
    print(f"Upper bound: {upper_bound2}")

    # Test case 3: Element greater than all array elements
    target3 = 10.0
    iterations3, upper_bound3 = binary_search(test_array, target3)
    print(f"\nSearching for {target3}:")
    print(f"Number of iterations: {iterations3}")
    print(f"Upper bound: {upper_bound3}")
