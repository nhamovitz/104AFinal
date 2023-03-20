
import numpy as np
import matplotlib.pyplot as plt
import cv2

from pathlib import Path

from read_numpy_array_files import read_wonky_file
import create_vids

def plot_a_pixel(frames_array, row, column, title="Plot of Spline Interpolation"):
    """
    Input: array of video we are analyzing, row of pixel, column of pixel, title of graph (default to spline)
    Output: Labeled plot of red, green, and blue interpolations
    """

    x_vals = [i for i in range(len(frames_array))]
    
    red = np.zeros(len(frames_array))
    green = np.zeros(len(frames_array))
    blue = np.zeros(len(frames_array))

    for f in x_vals:
        red[f] = frames_array[f][row][column][0]
        green[f] = frames_array[f][row][column][1]
        blue[f] = frames_array[f][row][column][2]

    
    plt.plot(x_vals, red, color = 'red')
    plt.plot(x_vals, green, color = 'green')
    plt.plot(x_vals, blue, color = 'blue')

    high_point = max((red.max(), green.max(), blue.max())) * 1.07
    for x in x_vals:
        plt.plot(x, high_point, '.', color = np.array([red[x], green[x], blue[x]]) / 255)

    plt.xlabel("Frame Number")
    plt.ylabel("RGB value (0 to 255)")
    plt.title(title)
    plt.legend(["Red Interpolation", "Green Interpolation", "Blue Interpolation"])

    plt.show()

def track_color():
    pass

def file_to_plot(npy_file, x_frac=0.5, y_frac=0.5, method="spline"):
    arr = read_wonky_file(npy_file)
    frames_to_plot(arr, x_frac, y_frac, method)


def frames_to_plot(arr, x_frac=0.5, y_frac=0.5, method="spline"):
    """
    Input: x fraction and y fraction of point along image
    """
    row = int(y_frac*len(arr[0]))
    column = int(x_frac*len(arr[0][0]))

    header = "Plot of the " + method + \
            " interpolation at the pixel at row " + str(row) + " and column " + str(column)

    plot_a_pixel(arr, row=row, column=column, title=header)

    return None

if __name__ == "__main__":
    # Spline Plot
    path = str(Path('.') / 'numpy_vids' / ('keys_' + 'spline' + '_n=4.npy'))
    file_to_plot(path)
    frames_to_plot(create_vids.sun()[0], y_frac=0.1)


