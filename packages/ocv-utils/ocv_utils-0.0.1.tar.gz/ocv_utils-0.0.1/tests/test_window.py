import unittest
import numpy as np
from ocv_utils import Window


class TestWindow(unittest.TestCase):

    def test_add_slider(self):
        window = Window()
        window.add_trackbar("x", 128, 256)

        trackbar_values = window.imshow([np.zeros((100, 100))])


        self.assertEqual(trackbar_values["x"], 128)


if __name__ == "__main__":
    unittest.main()