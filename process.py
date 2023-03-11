import cv2
import numpy as np

def sparse(path: str, cut_proportion = 2):
    cap = cv2.VideoCapture(path)

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # these come as floats for some reason
    # note: we want to round up, not round or truncate
    # that's weird to me, but you get an off-by-one error with n = 3 if this is `int(frame_count // cut_proportion), and same with n = 10 and `round(frame_count / cut_proportion)`
    keep_count = None
    if frame_count % cut_proportion == 0:
        keep_count = int(frame_count // cut_proportion)
    else:
        keep_count = int(frame_count // cut_proportion + 1)
    # print(frame_count, int(frame_count // cut_proportion), frame_count / cut_proportion, keep_count)
    width = int(width)
    height = int(height)
    
    sparse_vid = np.empty((keep_count, height, width, 3))

    kept_frames = []
    frame_number = 0

    while (cap.isOpened()):
        _, frame = cap.read()

        if frame_number % cut_proportion == 0:
            index = round(frame_number / cut_proportion)
            sparse_vid[index, :, :, :] = frame
            kept_frames.append(frame_number)            

        if frame_number == frame_count - 1:
            _, frame = cap.read()
            frame_number += 1
            assert frame is None
            cap.release()
            break

        frame_number += 1
    
        
    return sparse_vid, kept_frames

if __name__ == '__main__':
    demo = '.\\media\\vid1_WIN_20230310_14_20_03_Pro.mp4'

    sparse_vid, kept = sparse(demo)
    print("every 2", sparse_vid.shape, kept, len(kept))

    sparse_vid, kept = sparse(demo, 3)
    print("every 3", sparse_vid.shape, kept, len(kept))

    sparse_vid, kept = sparse(demo, 10)
    print("every 10", sparse_vid.shape, kept, len(kept))




