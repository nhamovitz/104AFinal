import cv2
import numpy as np

class Video:
    def __init__(self, frames):
        # assert len(frames.shape) == 4
        self.frames = frames

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

        # frames = np.zeros((frame_count, height, width, 3))
        frames = []

        i = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret: # Error handling kinda
                print(f"Error reading frame of video {path}")

            # frames[i, :, :, :] = frame
            frames.append(frame)

            # print(type(frame))
            # print(frame.shape)
            cv2.imshow("test", frame)           
            if cv2.waitKey(28) & 0xFF == ord('q'):
                break


            if i == frame_count - 1:
                # we're done
                # do one more read to make sure we get the 'no more data'
                _, frame = cap.read()
                assert frame is None
                cap.release()
            i += 1
        cv2.destroyAllWindows()


        vid = cls(frames)
        vid.frame_count = frame_count
        vid.frame_rate = frame_rate
        vid.info = path

        return vid

    def play_video(self):
        # milliseconds
        frame_delay = int(1000 // self.frame_rate)

        for frame in self.frames:
            # print(type(frame))
            # print(frame.shape)
            cv2.imshow(self.info, frame)

            if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


    
if __name__ == '__main__':
    print("Running demo...")

    from pathlib import Path

    demo_path = Path('.') / 'media' / 'vid1_WIN_20230310_14_20_03_Pro.mp4'
    vid = Video.from_file(str(demo_path))
    vid.play_video()


        
        




