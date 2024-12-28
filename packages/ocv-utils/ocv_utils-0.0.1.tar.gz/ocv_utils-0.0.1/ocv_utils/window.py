import cv2
import numpy as np


class Window:

    def __init__(self, name="Ocv-Utils Window", delay=5, verbose=False):
        """

        :param name: Name of the window
        :param delay: delay in milliseconds. 0 is blocking and waits for a key press
        """

        self.window_name = name
        cv2.namedWindow(self.window_name)
        self.delay_time = delay

        self.trackbar_values = {}
        self.key_actions = {
            27: lambda: exit(), # esc
        }

        # Enable Debug Prints
        self.verbose = verbose

    def add_trackbar(self, name, value, max_value):
        def set_trackbar_value(val):
            self.trackbar_values[name] = val
        cv2.createTrackbar(name, self.window_name, int(value), int(max_value), set_trackbar_value)
        self.trackbar_values[name] = value

    def add_key_action(self, key_code, func):
        self.key_actions[key_code] = func


    def imshow(self, imgs):

        for i, img in enumerate(imgs):

            # Convert to Uint8
            if img.dtype == np.float32 or img.dtype == np.float64:
                img = (img * 255).astype(np.uint8)

            # Grayscale to color
            if len(img.shape) == 2 or img.shape[2] == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            imgs[i] = img

        img = np.concatenate(imgs, axis=1)
        cv2.imshow(self.window_name, img)
        pressed_key = cv2.waitKey(self.delay_time)
        if pressed_key != -1: # only if a key was pressed
            print(f'Pressed key: {pressed_key}') if self.verbose else None
            for key, func in self.key_actions.items():
                if pressed_key == int(key):
                    func()

        return self.trackbar_values

if __name__ == "__main__":
    window = Window(delay=0)
    window.add_trackbar("x", 1, 255)
    window.add_key_action(ord('h'), lambda: print("Hello World!"))

    img1 = np.zeros((100, 100), dtype=np.uint8)
    img2 = np.random.random((100, 100, 3))

    trackbar_values = window.imshow([img1, img2])
    print("Trackbar Values:", trackbar_values)