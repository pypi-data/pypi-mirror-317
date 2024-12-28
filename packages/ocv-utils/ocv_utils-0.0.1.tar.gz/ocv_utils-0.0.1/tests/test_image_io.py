import os
import unittest

import cv2
import numpy as np
from ocv_utils import load_image


class TestLoadImage(unittest.TestCase):

    def test_load_rgb_as_rgb(self):

        shape = (256, 256, 3)
        cv2.imwrite("temp.png", np.random.randint(0, 255, shape, dtype=np.uint8))

        img = load_image("temp.png")
        os.remove("temp.png")

        self.assertEqual(img.shape, shape)
        self.assertEqual(img.dtype, np.uint8)

    def test_load_rgb_as_rgba(self):

        shape = (256, 256, 3)
        cv2.imwrite("temp.png", np.random.randint(0, 255, shape, dtype=np.uint8))

        img = load_image("temp.png", channels="rgba")
        os.remove("temp.png")

        shape = (shape[0], shape[1], 4)

        self.assertEqual(img.shape, shape)
        self.assertEqual(img.dtype, np.uint8)

if __name__ == "__main__":
    unittest.main()