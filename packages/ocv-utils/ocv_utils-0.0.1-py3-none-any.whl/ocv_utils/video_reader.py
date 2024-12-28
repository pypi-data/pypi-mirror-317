import cv2
import numpy as np


class VideoReader:
    """
    Simplifies exporting videos with opencv
    """

    def __init__(self, path="video.mp4", size=None, play_mode="normal"):
        """

        :param path: Path to video file
        :param size: Custom frame size of video
        :param play_mode: Play mode. ["normal", "loop", "boomerang"]
        """

        self._video = cv2.VideoCapture(path)
        self._num_frames = int(self._video.get(cv2.CAP_PROP_FRAME_COUNT)) #- 1 # TODO why -1 is necessary
        self._size = size
        self._play_mode = play_mode if play_mode in ["normal", "loop", "boomerang"] else "normal"
        self._play_direction = "forward" # just for boomerang

    def __len__(self):
        return self._num_frames

    def read(self, frame_id=None):
        """
        Read frame_id from video.

        :param frame_id: the frame id of the frame to read
        :return:
        """

        if frame_id is None:
            frame_id = int(self._video.get(cv2.CAP_PROP_POS_FRAMES))
        elif frame_id is not None and frame_id < self._num_frames:
            self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_id) # TODO set the pos to the original one back after reading

        if self._play_mode == "loop":
            if frame_id >= self._num_frames:
                frame_id = 0
                self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        elif self._play_mode == "boomerang":
            if self._play_direction == "forward" and frame_id > self._num_frames - 1:
                self._play_direction = "backward"

            if self._play_direction == "backward":
                frame_id -= 2
                self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_id) # cpu intensive
                if frame_id == 0:
                    self._play_direction = "forward"

        # print("Read_Frame", frame_id)
        ret, img = self._video.read()

        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if self._size is not None:
                img = cv2.resize(img, self._size)
            if self._play_mode != "normal":
                ret = frame_id

        return ret, img

    def get(self, *args, **kwargs):
        # For compatibility with cv2.Capture
        return self._video.get(*args, **kwargs)

    def set(self, *args, **kwargs):
        # For compatibility with cv2.Capture
        return self._video.set(*args, **kwargs)


if __name__ == "__main__":

    vid = VideoReader("/home/alex/PycharmProjects/ocv_utils/tests/assets/test_video.mp4", play_mode="boomerang")
    print(len(vid))

    for _ in range(1000):
        ret, _ = vid.read()
        print(ret)
