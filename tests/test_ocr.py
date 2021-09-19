import os
import unittest
from ocr import OCR


class TestOCR(unittest.TestCase):
    def setUp(self):
        self.path_scanned = "test_images/Page.png"
        self.path_real = "test_images/CosmosOne.jpg"
        self.tesseract_path = r"D:\Saransh\Softwares\Tesseract-OCR\tesseract.exe"

    def test_ocr_with_scanned_image(self):

        ocr = OCR(
            True,
            self.path_scanned,
            self.tesseract_path,
        )

        self.assertEqual(ocr.path, self.path_scanned)
        self.assertEqual(ocr.tesseract_location, self.tesseract_path)
        self.assertTrue(ocr.is_scanned)

        ocr.ocr()

        assert os.path.exists("OCR.png")
        assert not os.path.exists("rotated.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")
        self.assertIsInstance(ocr.text, str)

        os.remove("audio.mp3")
        os.remove("OCR.png")

    def test_ocr_with_real_image(self):

        ocr = OCR(
            False,
            self.path_real,
            self.tesseract_path,
        )

        self.assertEqual(ocr.path, "rotated.png")
        self.assertEqual(ocr.tesseract_location, self.tesseract_path)
        self.assertFalse(ocr.is_scanned)

        ocr.ocr()

        assert os.path.exists("OCR.png")
        assert os.path.exists("rotated.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")
        self.assertIsInstance(ocr.text, str)

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("rotated.png")


if __name__ == "__main__":
    unittest.main()
