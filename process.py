import cv2
import numpy as np

def sparse(path: str, cut_proportion = 2):
    cap = cv2.VideoCapture(path)

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width, height = cap.get(cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT)

    sparse_vid = np.empty(
        (frame_count // cut_proportion,
        height, width, 3)
    )

    kept_frames = []
    frame_number = 0

    while (cap.isOpened()):
        _, frame = cap.read()

        if frame_number % cut_proportion == 0:
            sparse_vid[frame_number, :, :, :] = frame
            kept_frames.append(frame_number)

        frame_number += 1

        if frame_number == frame_count - 1:
            cap.release()
        
    return sparse_vid, kept_frames





