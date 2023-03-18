from process import sparse
from process import run_demo
from interpolation_methods import spline_interpolation, linear_interpolation
from interpolation import best_neville
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

def new_vid(n, frame):
    """`n` blank frames with shape of `frame`"""
    return np.zeros((n, len(frame), len(frame[0]),3), dtype=np.uint8)


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
            print(f"{(r, p)=}")
            # this function is in another file
            r_vec = interpolation_function(x_vals, xi_vec = kept, fi_vec = all_pixel_data[r,p,0])
            g_vec = interpolation_function(x_vals, xi_vec = kept, fi_vec = all_pixel_data[r,p,1])
            b_vec = interpolation_function(x_vals, xi_vec = kept, fi_vec = all_pixel_data[r,p,2])
            for f in range(len(x_vals)):
                spline_video[f,r,p] = [r_vec[f], g_vec[f], b_vec[f]]
    return spline_video


def linear_frames(all_pixel_data, kept, n):
    return interpolation_frames(all_pixel_data, kept, n, linear_interpolation)

def lagrange_neville(x_vals, xi_vec, fi_vec):
    points = list(zip(xi_vec, fi_vec))
    Q_best = best_neville(points)
    print("Constructed Q table")
    return [Q_best(x) for x in x_vals]

def run_interpolation(video, sparse_interval, interp_with, reconstruct_granularity = None):
    video = Path(video)

    output_file = Path('.') / 'numpy_vids' / f"{video.stem}_sparse={sparse_interval}_{interp_with.__name__}_n={reconstruct_granularity}.npy"

    if output_file.exists():
        print(f"corresponding `.npy` file {output_file.name} already exists")
        return

    demo = str(Path('.') / 'media' / video)
    
    sparse_vid, kept, _ = sparse(demo, sparse_interval)
    # write_wonky_file("compressed_video.npy", sparse_vid)
    all_pix_data = process_sparse_frames(sparse_vid)
    # print("All Pixel Data", all_pix_data)
    print(f"Reshaped sparse vid from {sparse_vid.shape} to {all_pix_data.shape}.")

    # n = interval - 1 # ??
    if reconstruct_granularity is None:
        reconstruct_granularity = sparse_interval - 1
    interp_with = lagrange_neville
    interp_vid = interpolation_frames(
        all_pix_data, kept,
        n = reconstruct_granularity, interpolation_function = interp_with)

    write_wonky_file(str(output_file), interp_vid)


if __name__ == '__main__':
    run_interpolation(
        'sun.mp4',
        30,
        lagrange_neville,
        reconstruct_granularity = 10,
    )

