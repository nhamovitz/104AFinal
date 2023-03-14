
def process_sparse_frames(sparse_vid):
    """
    We want to prepare to interpolate across rows
    To do this, we want to seperate our data by color
    We can back-track off the x-coordinates using the recorded slide k from sparse
    """
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

