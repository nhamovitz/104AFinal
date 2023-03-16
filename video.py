import cv2
import numpy as np

class Video:

    def __init__(self, frames, metadata_from = None):
        print("Creating video object from ndarray")

        assert len(frames.shape) == 4
        assert frames.dtype == np.uint8
        assert frames.shape[4 - 1] == 3
        self.frames = frames

        print(f"{self.frames.shape=}")

        if metadata_from:
            if type(metadata_from) == str:
                self.info = metadata_from
                print(f"with info {metadata_from}")
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
        # assert vid1.shape == vid2.shape
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
    from process import run_demo

    demo_path = Path('.') / 'media' / 'keys.mp4'
    vid = Video.from_file(str(demo_path))
    vid.play_video()

    # orig_frames = vid.frames
    # new_shape = (146, 240, 424, 3)
    # new_frames = np.zeros(new_shape)
    # new_frames = orig_frames[0:144 + 1, ...]
    # vid = Video(new_frames, "first 146 frames of vid")
    


    # def flip_on(axis):
    #     def f(frames):
    #         return np.flip(frames, axis).copy()
    #     return f

    # analyze_against(vid, flip_on(0), "Reverse")
    # analyze_against(vid, flip_on(1), "upside_down")
    # analyze_against(vid, flip_on(2), "sideways")
    # analyze_against(vid, lambda frames: np.roll(frames, 1, 3).copy(), "colors")
    # analyze_against(vid, lambda frames: np.zeros_like(frames), "black")

    from process import run_demo
    import video
    import create_vids


    sparse, _ = run_demo()
    # sparse = create_vids.simple()
    sparse = video.Video(sparse, "sparse version")
    sparse.frame_rate = 2
    # print(sparse.frames[-1])
    sparse.play_video()

    import read_numpy_array_files

    spl = read_numpy_array_files.read_wonky_file(str(Path('.') / 'numpy_vids' / ('keys_' + 'spline' + '_n=4.npy')))

    spl = video.Video(spl, "(spline) interpolation")
    spl.frame_rate = vid.frame_rate
    # print(interped.frames[-1])
    spl.play_video()

    cut_vid_shape = spl.frames.shape
    cut_vid = np.zeros(cut_vid_shape)

    # cut_vid = np.delete(vid.frames, [146, 147, 148, 149], 3)
    cut_vid = vid.frames[0:145 + 1, ...]
    cut_vid = Video(cut_vid, "four frames gone")



    print(f"Error analysis for spline.")
    abs_error = Video.abs_error(cut_vid, spl)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(cut_vid, spl))}")
    spl_err = Video(abs_error)
    spl_err.frame_rate = vid.frame_rate
    spl_err.info = "spl_err"
    spl_err.play_video()





    lin = read_numpy_array_files.read_wonky_file(str(Path('.') / 'numpy_vids' / ('keys_' + 'linear' + '_n=4.npy')))

    lin = video.Video(lin, "(lin) interpolation")
    lin.frame_rate = vid.frame_rate
    # print(interped.frames[-1])

    lin.play_video()

    print(f"Error analysis for lin.")
    abs_error = Video.abs_error(cut_vid, lin)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(cut_vid, lin))}")
    lin_err = Video(abs_error)
    lin_err.frame_rate = vid.frame_rate
    lin_err.info = "lin err"
    lin_err.play_video()


