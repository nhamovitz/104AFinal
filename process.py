


import cv2
import numpy as np

def sparse(path: str, cut_proportion = 2):
    cap = cv2.VideoCapture(path)

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

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
    
    sparse_vid = np.empty((keep_count, height, width, 3), dtype=np.uint8)

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

    return sparse_vid, kept_frames, frame_rate


def write_black_with_codec(codec, extension):
    height, width = 720, 1280
    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(f".\\media\\test\\{codec}_{extension}.{extension}", fourcc, 30, (height, width))
    for _ in range(150):
        blank_frame = np.zeros((height, width))
        writer.write(blank_frame)
    writer.release()



def write_video(frames: np.ndarray, name: str, fps: float):
    _, height, width, _ = frames.shape

    codec = cv2.VideoWriter_fourcc(*'XVID') # maybe smth different?
    writer = cv2.VideoWriter(name + '.avi', codec, fps, (height, width))

    for frame in frames:
        blank_frame = np.zeros_like(frame)
        writer.write(blank_frame)

    writer.release()


def run_demo():
    from pathlib import Path
    demo = str(Path('.') / 'media' / 'keys.mp4')
    
    # sparse_vid, kept, _ = sparse(demo)
    # print("every 2", sparse_vid.shape, kept, len(kept))

    # sparse_vid, kept, _ = sparse(demo, 3)
    # print("every 3", sparse_vid.shape, kept, len(kept))

    # sparse_vid, kept, _ = sparse(demo, 10)
    # print("every 10", sparse_vid.shape, kept, len(kept))

    # redone_vid, _, _ = sparse(demo, 1)

    # print(redone_vid.shape)

    # for codec in ('DIVX', 'XVID', 'MJPG', 'X264', 'WMV1', 'WMV2', 'MP4V', 'MPEG', 'H264', 'mp4v', 'mpv4'):
    #     for ext in ('mp4', 'avi', 'mpg'):
    #         try:
    #             video_with_codec(codec, ext)
    #         except Exception as e:
    #             print(f"{codec=}, {ext=}, {e=}")

    # write_black_with_codec('mpv4', 'mpg')

    interval = 5
    sparse_vid, kept, frame_rate = sparse(demo, interval)
    print(f"every {interval}", sparse_vid.shape, kept, len(kept))

    return sparse_vid, kept

if __name__ == '__main__':
    run_demo()

