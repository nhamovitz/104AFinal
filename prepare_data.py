from process import sparse
from process import run_demo
from interpolation_methods import spline_interpolation, linear_interpolation
import numpy as np
from read_numpy_array_files import read_wonky_file, write_wonky_file

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

def interpolation_frames(all_pixel_data, kept, n):
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
    x_vals = [int(i*(kept[1] - kept[0])/(n+1)) for i in range(n*len(kept))]
    # construct video with splines
    print("Make empty new video")
    spline_video = new_vid(n, all_pixel_data)
    # all_spline_data = [ [ [] for pixel in row ] for row in all_pixel_data]
    all_spline_data = np.zeros((len(all_pixel_data), len(all_pixel_data[0])))
    print("Perform Interpolations")
    for r in range(len(all_spline_data)):
        for p in range(len(all_spline_data[0])):
            # this function is in another file
            r_vec = spline_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,0])
            g_vec = spline_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,1])
            b_vec = spline_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,2])
            for f in range(n):
                spline_video[f,r,p] = [r_vec[f], g_vec[f], b_vec[f] ]
    return spline_video

def new_vid(n, frame):
    return np.zeros((n, len(frame), len(frame[0]),3), dtype=np.uint8)

def interpolate_pixel_data(pixel_data, kept, x_vec):
    # Do spline processing
    spline_vec = spline_interpolation(x_vec, len(kept) - 1, kept, pixel_data)
    return spline_vec


def extra_funct(sparse_vid):
    new_vid = [ [ [0,0,0] for __ in len(sparse_vid[0])] for _ in len(sparse_vid)]
    # iterate through rows and seperate colors
    for r in sparse_vid:
        row = sparse_vid[r]
        red = [p[0] for p in row]
        green = [p[1] for p in row]
        blue = [p[2] for p in row]
        # use interpolation to find the in between
        # Some test stuff, re-assign variables as desired. We do a simple average here. 

        vid_length = 2*len(red)
        new_red = [0] * vid_length
        new_blue = [0] * vid_length
        new_green = [0] * vid_length
        for i in range(vid_length):
            if i%2:
                new_red[i] = red[i//2]
                new_blue[i] = blue[i//2]
                new_green[i] = green[i//2]
            else:
                new_red[i] = (red[i//2] + red[i//2 + 1]) * 0.5
                new_blue[i] = (blue[i//2] + blue[i//2 + 1]) * 0.5
                new_green[i] = (green[i//2] + green[i//2 + 1]) * 0.5
        new_vid[r] = [ [new_red[i], new_blue[i], new_green[i]] for i in range(vid_length) ]
    print(new_vid)
    return new_vid

def linear_frames(all_pixel_data, kept, n):
    # make array for all frame numbers
    x_vals = [int(i*(kept[1] - kept[0])/(n+1)) for i in range(n*len(kept))]
    # construct video with splines
    print("Make empty new video")
    spline_video = new_vid(n, all_pixel_data)
    # all_spline_data = [ [ [] for pixel in row ] for row in all_pixel_data]
    all_spline_data = np.zeros((len(all_pixel_data), len(all_pixel_data[0])))
    print("Perform Interpolations")
    for r in range(len(all_spline_data)):
        for p in range(len(all_spline_data[0])):
            # this function is in another file
            r_vec = linear_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,0])
            g_vec = linear_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,1])
            b_vec = linear_interpolation(x_vals, n, xi_vec = kept, fi_vec = all_pixel_data[r,p,2])
            for f in range(n):
                spline_video[f,r,p] = [r_vec[f], g_vec[f], b_vec[f] ]
    return spline_video


if __name__ == '__main__':
    sparse_vid, kept = run_demo()
    print("Sparse Video Dimensions: ", len(sparse_vid), len(sparse_vid[0]), len(sparse_vid[0][0]))
    # write_wonky_file("compressed_video.npy", sparse_vid)
    all_pix_data = process_sparse_frames(sparse_vid)
    print("All Pixel Data", all_pix_data)
    spline_vid = interpolation_frames(all_pix_data, kept, n = 3 * len(sparse_vid))
    print("Spline Video Dimensions: ", len(spline_vid), len(spline_vid[0]), len(spline_vid[0][0]))
    print(spline_vid)

    write_wonky_file("20_3.npy", a = spline_vid)


    # print(sparse_vid, kept)
    # linear_vid = linear_frames(all_pix_data, kept, n = 20*len(sparse_vid))
    # print("Linear Fit Video Data")
    # print(linear_vid)

