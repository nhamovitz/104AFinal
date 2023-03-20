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
                # self.frame_count = metadata_from.frame_count
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

    def show_frame(self, frame_number):
        assert frame_number < self.frames.shape[0]
        while True:
            cv2.imshow(
                f"{self.info}, frame {frame_number}",
                self.frames[frame_number]
            )
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


    @classmethod
    def abs_error(cls, vid1, vid2):
        # assert vid1.shape == vid2.shape
        err = np.abs(
            np.subtract(
                vid1.frames.astype(np.int16), vid2.frames.astype(np.int16)
            ),
        )
        return err.astype(np.uint8)

    @classmethod
    def rel_error(cls, vid1, vid2):
        return cls.abs_error(vid1, vid2) / 255

    def write_to_file(self, name: str):
        _, height, width, _ = self.frames.shape

        codec = cv2.VideoWriter_fourcc(*'XVID') # maybe smth different?
        writer = cv2.VideoWriter(name + '.avi', codec, self.frame_rate, (height, width))

        for frame in self.frames:
            writer.write(frame)

        writer.release()



def analyze_against(vid: Video, func, description: str, play_variant = True):
    """
    find the error when applying `func` to the frames of `vid`.
    vid: input video
    func: function accepting np.array with shape (length, height, width, 3)
    description: of what transformation func will perform
    play_variant: if True, `analyze_against` will play the transformed video and the "absolute error" video. defaults to True
    """
    frames = vid.frames.copy()
    new_frames = func(frames)
    new_vid = Video(new_frames, metadata_from = vid)
    if description:
        if new_vid.info:
            new_vid.info += ", " + description
        else:
            new_vid.info = description

    if play_variant:
        new_vid.play_video(fast=False)

    print(f"Error analysis for variant {description}.")
    abs_error = Video.abs_error(vid, new_vid)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(vid, new_vid))}")
    if play_variant:
        rel_error = Video(abs_error, metadata_from = new_vid)
        rel_error.info += ", abs error"
        rel_error.play_video()


def demo1(vid):
    """play video, and then play and play error of: reversed, upside down, flipped x-y, color channels rotated, equal length of black"""
    
    vid.play_video()

    def flip_on(axis):
        def f(frames):
            return np.flip(frames, axis).copy()
        return f

    analyze_against(vid, flip_on(0), "Reverse")
    analyze_against(vid, flip_on(1), "upside_down")
    analyze_against(vid, flip_on(2), "sideways")
    analyze_against(vid, lambda frames: np.roll(frames, 1, 3).copy(), "colors")
    analyze_against(vid, lambda frames: np.zeros_like(frames), "black")


    
if __name__ == '__main__':
    print("Running demo...")

    from pathlib import Path
    from process import run_demo
    import read_numpy_array_files
    import create_vids


    demo_path = Path('.') / 'media' / 'keys.mp4'
    vid = Video.from_file(str(demo_path))
    # vid.frame_rate *= 0.7
    # # mini_sun, sun = create_vids.sun()
    # vid = Video(sun, "`sun`")
    # vid.frame_rate = 1.1
    # print(mini_sun)
    # vid.play_video()

    # print(mini_sun)
    # print(np.flip(mini_sun, 1))
    # print(np.abs(mini_sun - np.flip(mini_sun, 1)))

    # while True:
    # demo1(vid)
    # exit()

    # lagrange = read_numpy_array_files.read_wonky_file(str(Path('.') / 'numpy_vids' /'sun_lagrange_neville_n=10.npy'))
    # lagrange = Video(lagrange, "lagrange")
    # lagrange.frame_rate = 4
    # lagrange.play_video()
    
    # sparse, _ = run_demo()
    # # sparse = create_vids.simple()
    # sparse = Video(sparse, "sparse version")
    # sparse.frame_rate = 2
    # # print(sparse.frames[-1])
    # sparse.play_video()


    spl = read_numpy_array_files.read_wonky_file(
        str(Path('.') / 'numpy_vids' / ('keys_' + 'spline' + '_n=4.npy'))
        # "numpy_vids\\surfing1_sparse=5_spline_interpolation_n=None.npy"
    )
    spl = Video(spl, "(spline) interpolation")
    spl.frame_rate = vid.frame_rate
    # print(interped.frames[-1])
    spl.play_video()

    cut_vid = np.zeros(spl.frames.shape)
    cut_vid = vid.frames[0:cut_vid.shape[0], ...]
    cut_vid = Video(cut_vid, "two frames gone")


    print(f"Error analysis for spline.")
    abs_error = Video.abs_error(cut_vid, spl)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(cut_vid, spl))}")
    spl_err = Video(abs_error)
    spl_err.frame_rate = vid.frame_rate #* 0.15
    spl_err.info = "spl_err"
    spl_err.play_video()




    lin = read_numpy_array_files.read_wonky_file(
        str(Path('.') / 'numpy_vids' / ('keys_' + 'linear' + '_n=4.npy'))
        # "numpy_vids\\surfing1_sparse=5_linear_interpolation_n=None.npy"

        )
    lin = Video(lin, "(lin) interpolation")
    lin.frame_rate = vid.frame_rate
    # print(interped.frames[-1])
    lin.play_video()
    print(f"Error analysis for lin.")
    abs_error = Video.abs_error(cut_vid, lin)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(cut_vid, lin))}")
    lin_err = Video(abs_error)
    lin_err.frame_rate = vid.frame_rate #* 0.15
    lin_err.info = "lin err"
    lin_err.play_video()


    print(f"Difference between splines")
    abs_error = Video.abs_error(spl, lin)
    print(f"Mean absolute error: {np.mean(abs_error)}")
    print(f"Mean relative error: {np.mean(Video.rel_error(cut_vid, lin))}")
    diff = Video(abs_error)
    diff.frame_rate = vid.frame_rate
    diff.info = "spline / linear difference"
    diff.play_video()


    spl_err.show_frame(43)
    lin_err.show_frame(43)
    diff.show_frame(43)


    disagree = np.count_nonzero(diff.frames)
    print(f"{disagree=}, {spl_err.frames.size=}")
    print(f"ratio = {disagree / spl_err.frames.size}")



