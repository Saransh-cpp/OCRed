import os
import platform
import unittest
from aiview_ocr.ocr import OCR


class TestOCR(unittest.TestCase):
    def setUp(self):
        self.path_scanned = "images/Page.png"
        self.path_real = "images/CosmosOne.jpg"
        self.path_sign_board = "images/signboard.jpg"
        self.tesseract_path = r"D:\Saransh\Softwares\Tesseract-OCR\tesseract.exe"

    def test_ocr_with_scanned_image(self):

        ocr = OCR(
            True,
            self.path_scanned,
            self.tesseract_path if platform.system() == "Windows" else None,
        )

        self.assertEqual(ocr.path, self.path_scanned)
        self.assertIsNone(
            ocr.tesseract_location
        ) if platform.system() != "Windows" else self.assertEqual(
            ocr.tesseract_location, self.tesseract_path
        )
        self.assertTrue(ocr.is_scanned)

        text = ocr.ocr_meaningful_text(save_output=True)

        self.assertIsInstance(text, str)
        assert os.path.exists("OCR.png")
        assert os.path.exists("output.txt")
        assert not os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")
        self.assertIsInstance(ocr.text, str)

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("output.txt")

    def test_ocr_with_real_image(self):

        ocr = OCR(
            False,
            self.path_real,
            self.tesseract_path if platform.system() == "Windows" else None,
        )

        self.assertEqual(ocr.path, "preprocessed.png")
        self.assertIsNone(
            ocr.tesseract_location
        ) if platform.system() != "Windows" else self.assertEqual(
            ocr.tesseract_location, self.tesseract_path
        )
        self.assertFalse(ocr.is_scanned)

        text = ocr.ocr_meaningful_text()

        self.assertIsInstance(text, str)
        assert os.path.exists("OCR.png")
        assert os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")
        self.assertIsInstance(ocr.text, str)

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("preprocessed.png")

    def test_ocr_sign_board(self):
        ocr = OCR(
            True,
            self.path_sign_board,
        )

        self.assertEqual(ocr.path, self.path_sign_board)
        self.assertTrue(ocr.is_scanned)

        text = ocr.ocr_sparse_text(save_output=True)

        self.assertIsInstance(text, str)
        assert os.path.exists("OCR.png")
        assert os.path.exists("output.txt")
        assert not os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech(lang="hi")

        assert os.path.exists("audio.mp3")
        self.assertIsInstance(ocr.text, str)

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("output.txt")


if __name__ == "__main__":
    unittest.main()
