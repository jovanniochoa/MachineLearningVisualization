import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generate_random_array(size):
    return np.random.randint(1, 100, size)  # Generate random numbers between 1 and 100

def display_bar_chart(array):
    fig, ax = plt.subplots()
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('Random Array Bar Chart')
    bar_container = ax.bar(range(1, len(array) + 1), array)  # Create the initial bar chart

    def update_chart(frame):
        if frame < len(frames):
            frame_data = frames[frame]
            for i, rect in enumerate(bar_container):
                rect.set_height(frame_data[i])
        return bar_container

    # Create frames for sorting animation
    frames = []
    merge_sort(random_array, 0, len(random_array) - 1, frames)

    # Animate the bar chart
    anim = FuncAnimation(fig, update_chart, frames=len(frames) + 1, interval=500, repeat=False)

    plt.show()

def merge_sort(array, start, end, frames):
    if start >= end:
        return

    mid = (start + end) // 2

    merge_sort(array, start, mid, frames)
    merge_sort(array, mid + 1, end, frames)

    merge(array, start, mid, end, frames)

def merge(array, start, mid, end, frames):
    temp_array = array[start:end+1].copy()
    i = 0
    j = mid - start + 1
    k = start

    while i <= mid - start and j <= end - start:
        if temp_array[i] <= temp_array[j]:
            array[k] = temp_array[i]
            i += 1
        else:
            array[k] = temp_array[j]
            j += 1
        k += 1

    while i <= mid - start:
        array[k] = temp_array[i]
        i += 1
        k += 1

    while j <= end - start:
        array[k] = temp_array[j]
        j += 1
        k += 1

    frames.append(array.copy())

# Get user input for the size of the array
size = int(input("Enter the size of the array: "))

# Generate random array
random_array = generate_random_array(size)

# Display the bar chart with sorting animation
display_bar_chart(random_array)
