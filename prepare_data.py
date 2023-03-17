from process import sparse
from process import run_demo
from interpolation_methods import spline_interpolation, linear_interpolation
import numpy as np
from read_numpy_array_files import read_wonky_file, write_wonky_file
from pathlib import Path

def process_sparse_frames(sparse_vid):
    """
    We want to prepare to interpolate across rows
    To do this, we want to seperate our data by color
    We can back-track off the x-coordinates using the recorded slide k from sparse
    input values:
        sparse_vid that is called from the process file, records video frames and rgb
    return values:
        all_pixel data: records the r,g, and b values for every pixel. record these values as lists to 
        represent changes across frames
    """
    return np.moveaxis(sparse_vid, 0, -1)

    # print("Sparse Video", sparse_vid)
    all_pixel_data = [ [ [ [],[],[] ] for pixel in row] for row in sparse_vid[0]]
    all_pixel_data = np.zeros((len(sparse_vid[0]), len(sparse_vid[0][0]), 3, len(sparse_vid)))

    # Structure a list of all the rgb for a pixel in order
    print("Dimensions of sparse video:", len(sparse_vid), len(sparse_vid[0]), len(sparse_vid[0,0]))
    for fr in range(len(sparse_vid)):
        frame = sparse_vid[fr]
        for r in range(len(frame)):
            row = frame[r]
            for p in range(len(row)):
                pixel = row[p]
                all_pixel_data[r,p,0,fr] = pixel[0]
                all_pixel_data[r,p,1,fr] = pixel[1]
                all_pixel_data[r,p,2,fr] = pixel[2]

    return all_pixel_data

def interpolation_frames(all_pixel_data, kept, n, interpolation_function = spline_interpolation):
    """
    pixel data: returned from process_sparse_frames
        row:
            pixel:
                red data
                green data
                blue data
    n: number of total frames we want
    """
    # make array for all frame numbers
    x_vals = [i*(kept[1] - kept[0])/(n+1) for i in range((n+1)*(len(kept)-1) + 1)]
    # construct video with splines
    print("Make empty new video")
    spline_video = new_vid(len(x_vals), all_pixel_data)
    # all_spline_data = [ [ [] for pixel in row ] for row in all_pixel_data]
    all_spline_data = np.zeros((len(all_pixel_data), len(all_pixel_data[0])))
    print("Perform Interpolations")
    for r in range(len(all_spline_data)):
        for p in range(len(all_spline_data[0])):
            # this function is in another file
            r_vec = interpolation_function(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,0])
            g_vec = interpolation_function(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,1])
            b_vec = interpolation_function(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,2])
            for f in range(len(x_vals)):
                spline_video[f,r,p] = [r_vec[f], g_vec[f], b_vec[f] ]
    return spline_video

def new_vid(n, frame):
    """`n` blank frames with shape of `frame`"""
    return np.zeros((n, len(frame), len(frame[0]),3), dtype=np.uint8)

def linear_frames(all_pixel_data, kept, n):
    return interpolation_frames(all_pix_data, kept, n, linear_interpolation)

if __name__ == '__main__':
    sparse_vid, kept = run_demo()
    print("made sparse vid, kept:")
    # print("Sparse Video Dimensions: ", len(sparse_vid), len(sparse_vid[0]), len(sparse_vid[0][0]))
    # # write_wonky_file("compressed_video.npy", sparse_vid)
    all_pix_data = process_sparse_frames(sparse_vid)
    # print("All Pixel Data", all_pix_data)
    # print("Spline Video Dimensions: ", len(spline_vid), len(spline_vid[0]), len(spline_vid[0][0]))
    # print(spline_vid[-1])
    # print(sparse_vid[-1])


    

    # print(sparse_vid, kept)
    print(kept)
    n = 4
    # spline_vid = interpolation_frames(all_pix_data, kept, n = n)
    # linear_vid = linear_frames(all_pix_data, kept, n = n)
    print("Linear Fit Video Data")
    # print(spline_vi)

    # write_wonky_file(str(Path('.') / 'numpy_vids' / f"keys_linear_n={n}.npy"), linear_vid)

