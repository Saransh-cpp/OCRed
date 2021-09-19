import os
import unittest
import numpy as np
from aiview_ocr.preprocessing import Preprocessor


class TestOCR(unittest.TestCase):
    def setUp(self):
        self.path = "images/CosmosOne.jpg"

    def test_scan(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img = pre.scan()
        self.assertIsInstance(img, np.ndarray)

        img = pre.scan(save=True)
        self.assertIsInstance(img, np.ndarray)
        assert os.path.exists("preprocessed.png")

        os.remove("preprocessed.png")

    def test_rotate(self):
        pre = Preprocessor(self.path)
        self.assertEqual(pre.path, self.path)

        img = pre.rotate()
        self.assertIsInstance(img, np.ndarray)

        img = pre.rotate(save=True)
        self.assertIsInstance(img, np.ndarray)
        assert os.path.exists("rotated.png")

        os.remove("rotated.png")

        img = pre.rotate(image=img)
        img1 = pre.rotate(image=img)
        self.assertIsInstance(img, np.ndarray)
        self.assertIsInstance(img1, np.ndarray)
        np.testing.assert_array_equal(img, img1)


if __name__ == "__main__":
    unittest.main()
