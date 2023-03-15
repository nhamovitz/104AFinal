def normalized_error_video(new_video, true_video):
    """
    input: 2 numpy videos in array form
    """
    nframes = len(new_video)
    tframes = len(true_video)
    factor = tframes // nframes
    error = 0
    for i in range(nframes):
        error += normalized_error_frame(new_video[i], true_video[int(i*factor)])

def normalized_error_frame(new_frame, true_frame):
    """
    input: new frame and true frame both numpy arrays
    """
    error = 0
    for r in range(len(new_frame)):
        rerror = 0
        for p in range(len(new_frame[0])):
            perror = 0
            for c in range(3):
                perror += abs(new_frame[r][p][c] - true_frame[r][p][c])
            perror = perror/3
            rerror += perror
        rerror = rerror/len(new_frame[0])
        error += rerror
    error = error/len(new_frame)
    return error
        

