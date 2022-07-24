import os
import unittest

import cv2
import numpy as np

from ocred.preprocessing import Preprocessor


class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.path = "images/CosmosOne.jpg"

    def test_scan(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img = pre.scan()
        self.assertIsInstance(img, np.ndarray)

        img = pre.scan(save=True)
        self.assertIsInstance(img, np.ndarray)
        assert os.path.exists("scanned.png")

        os.remove("scanned.png")

        img = cv2.imread(self.path)

        img = pre.scan(image=img)
        self.assertIsInstance(img, np.ndarray)

    def test_rotate(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img, median_angle = pre.rotate()
        self.assertIsInstance(median_angle, float)
        self.assertIsInstance(img, np.ndarray)

        img, median_angle = pre.rotate(save=True)
        self.assertIsInstance(img, np.ndarray)
        self.assertIsInstance(median_angle, float)
        assert os.path.exists("rotated.png")

        os.remove("rotated.png")

        img, median_angle = pre.rotate(image=img)
        img1, median_angle = pre.rotate(image=img)
        self.assertIsInstance(median_angle, float)
        self.assertIsInstance(img, np.ndarray)
        self.assertIsInstance(img1, np.ndarray)
        np.testing.assert_array_equal(img, img1)

    def test_remove_noise(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img = pre.remove_noise()
        self.assertIsInstance(img, np.ndarray)

        img = pre.remove_noise(save=True)
        self.assertIsInstance(img, np.ndarray)
        assert os.path.exists("noise_free.png")

        os.remove("noise_free.png")

        img = pre.remove_noise(image=img)
        self.assertIsInstance(img, np.ndarray)

    def test_thicken_font(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img = pre.thicken_font()
        self.assertIsInstance(img, np.ndarray)

        img = pre.thicken_font(save=True)
        self.assertIsInstance(img, np.ndarray)
        assert os.path.exists("thick_font.png")

        os.remove("thick_font.png")

        img = pre.thicken_font(image=img)
        self.assertIsInstance(img, np.ndarray)


if __name__ == "__main__":
    unittest.main()
