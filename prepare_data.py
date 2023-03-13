from process import sparse
from process import run_demo
from interpolation_methods import spline_interpolation


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
    all_pixel_data = [ [ [ [], [], [] ] for pixel in len(row)] for row in len(sparse_vid[0])]

    # Structure a list of all the rgb for a pixel in order
    for fr in len(sparse_vid):
        frame = sparse_vid[fr]
        for r in len(frame):
            row = frame[r]
            for p in row:
                all_pixel_data[r][p][0].append(row[0])
                all_pixel_data[r][p][1].append(row[1])
                all_pixel_data[r][p][2].append(row[2])

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
    interp = {
        "natural_spline": [],
        "linear regression": []
    }
    # make array for all frame numbers
    x_vals = [i for i in range(n)]
    # construct video with splines
    spline_vid = new_vid(n, all_pixel_data)
    all_spline_data = [ [ [] for pixel in row ] for row in all_pixel_data]
    for r in range(len(all_spline_data)):
        for p in range(len(all_spline_data[0])):
            f_vec = spline_interpolation()

    for f in range(len(spline_vid)):
        for r in range(len(spline_vid)):
            for p in range(len)

def new_vid(n, frame):
    return [ [ [ [] for pixel in row] for row in frame] for f in range(n)]


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

