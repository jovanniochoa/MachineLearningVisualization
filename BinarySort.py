def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


arr = [7, 20, 154, 190, 209, 421, 599, 600, 934, 1212]
target = 600

result = binary_search(arr, target)

if result == -1:
    print("Element not found")
else:
    print("Element found at index", result)
