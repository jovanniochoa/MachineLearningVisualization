from flask import Flask, render_template, request, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import io
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

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
    merge_sort(array, 0, len(array) - 1, frames)

    # Animate the bar chart
    anim = FuncAnimation(fig, update_chart, frames=len(frames) + 1, interval=500, repeat=False)

    # Save the animation as a GIF
    gif_path = os.path.join(app.config['UPLOAD_FOLDER'], 'chart.gif')
    anim.save(gif_path, writer='pillow')

    # Convert GIF to base64-encoded string
    with open(gif_path, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')

    # Delete the temporary GIF file
    os.remove(gif_path)

    return encoded_image

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

@app.route('/')
def index():
    return render_template('myindex.html')

@app.route('/display_chart')
def display_chart():
    size = int(request.args.get('size'))

    # Generate random array
    random_array = generate_random_array(size)

    # Display the bar chart and get the encoded image
    encoded_image = display_bar_chart(random_array)

    return encoded_image

@app.route('/static/chart.gif')
def get_chart():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'chart.gif')

if __name__ == '__main__':
    app.run(debug=True)
