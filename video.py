import cv2
import numpy as np

class Video:
    def __init__(self, frames, metadata_from = None):
        assert len(frames.shape) == 4
        assert frames.dtype == np.uint8
        assert frames.shape[4 - 1] == 3
        self.frames = frames

        if metadata_from:
            if type(metadata_from) == str:
                self.info = metadata_from
                print(f"Creating video with info {metadata_from}")
            if type(metadata_from) == type(self):
                self.frame_count = metadata_from.frame_count
                self.frame_rate  = metadata_from.frame_rate
                self.info        = metadata_from.info


    @classmethod
    def from_file(cls, path):
        print(f"Creating Video object from file at {path}")
        cap = cv2.VideoCapture(path)

        # if they're not integers then something is already deeply wrong
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width       = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # this very well could be a float
        frame_rate  = cap.get(cv2.CAP_PROP_FPS)

        print(f"{frame_count=}, {width=}, {height=}, {frame_rate=}")

        frames = np.zeros((frame_count, height, width, 3), dtype=np.uint8)

        i = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret: # Error handling kinda
                print(f"Error reading frame of video {path}")

            frames[i, ...] = frame
            # cv2.imshow("test", frame)           
            # if cv2.waitKey(28) & 0xFF == ord('q'):
            #     break

            if i == frame_count - 1:
                # we're done
                # do one more read to make sure we get the 'no more data'
                _, frame = cap.read()
                assert frame is None
                cap.release()
            i += 1

        vid = cls(frames)
        vid.frame_count = frame_count
        vid.frame_rate = frame_rate
        vid.info = path

        return vid

    def play_video(self, fast = False):
        # milliseconds
        if not fast:
            frame_delay = int(1000 // self.frame_rate)
        else:
            frame_delay = int(1000 // (self.frame_rate * 2.5))

        for frame in self.frames:
            cv2.imshow(self.info, frame)
            if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
                break
    
        cv2.destroyAllWindows()

    @classmethod
    def abs_error(cls, vid1, vid2):
        return np.abs(vid1.frames - vid2.frames)

    @classmethod
    def rel_error(cls, vid1, vid2):
        return cls.abs_error(vid1, vid2) / 255


def analyze_against(vid: Video, func, description: str, play_variant = True):
    frames = vid.frames.copy()
    new_frames = func(frames)
    new_vid = Video(new_frames, metadata_from = vid)
    if description:
        if new_vid.info:
            new_vid.info += ", " + description
        else:
            new_vid.info = description

    if play_variant:
        new_vid.play_video(fast=True)

    print(f"Error analysis for variant {description}.")
    abs_error = Video.abs_error(vid, new_vid)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(vid, new_vid))}")
    if play_variant:
        rel_error = Video(abs_error, metadata_from = new_vid)
        rel_error.info += ", abs error"
        rel_error.play_video()




    
if __name__ == '__main__':
    print("Running demo...")

    from pathlib import Path

    demo_path = Path('.') / 'media' / 'vid1_WIN_20230310_14_20_03_Pro.mp4'
    vid = Video.from_file(str(demo_path))
    vid.play_video()


    def flip_on(axis):
        def f(frames):
            return np.flip(frames, axis).copy()
        return f

    # analyze_against(vid, flip_on(0), "Reverse")
    # analyze_against(vid, flip_on(1), "upside_down")
    # analyze_against(vid, flip_on(2), "sideways")
    # analyze_against(vid, lambda frames: np.roll(frames, 1, 3).copy(), "colors")
    # analyze_against(vid, lambda frames: np.zeros_like(frames), "black")

    from process import run_demo
    import video


    sparse, _ = run_demo()
    sparse = video.Video(sparse, "total interpolation")
    sparse.frame_rate = 1
    print(sparse.frames[-1])
    sparse.play_video()

    import read_numpy_array_files

    spline_on_demo = read_numpy_array_files.read_wonky_file('20_3.npy')

    spline = video.Video(spline_on_demo, "spline interpolation")
    spline.frame_rate = 1
    print(spline.frames[-1])

    spline.play_video()


        




