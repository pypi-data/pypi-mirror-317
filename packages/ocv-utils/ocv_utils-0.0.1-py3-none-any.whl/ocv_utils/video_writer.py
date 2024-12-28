import cv2
import numpy as np


class VideoWriter:
    """
    Simplifies exporting videos with opencv
    """

    def __init__(self, path="./video.mp4", fps=30, channels="rgb"):  # TODO fps more vaiable

        self._path = path
        self._fps = fps
        self._cv_videowriter = None
        self._channels = channels

        self._format = cv2.VideoWriter_fourcc(*'mp4v')  # TODO add support for mp4 and avi

    def add_frame(self, frame):

        if self._cv_videowriter is None:

            height, width = frame.shape[0], frame.shape[1]
            self._cv_videowriter = cv2.VideoWriter(self._path, self._format, self._fps, (width, height))

        if frame.dtype == np.float32 or frame.dtype == np.float64:
            frame = (frame * 255).astype(np.uint8)

        if self._channels == "rgb":
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


        self._cv_videowriter.write(frame)


if __name__ == "__main__":

    img = np.zeros((512, 512, 3))
    video_writer = VideoWriter()

    for i in range(1000):
        video_writer.add_frame(img)
