import os
import platform
import unittest

from ocred.ocr import OCR


class TestOCR(unittest.TestCase):
    def setUp(self):
        self.path_scanned = "images/Page.png"
        self.path_real = "images/CosmosOne.jpg"
        self.path_sign_board = "images/signboard.jpg"
        self.path_invoice = "images/1146-receipt.jpg"
        self.tesseract_path = r"D:\Saransh\Software\Tesseract-OCR\tesseract.exe"

    def test_ocr_with_scanned_image(self):

        ocr = OCR(
            False,
            self.path_scanned,
            self.tesseract_path if platform.system() == "Windows" else None,
        )

        self.assertEqual(ocr.path, self.path_scanned)
        self.assertIsNone(
            ocr.tesseract_location
        ) if platform.system() != "Windows" else self.assertEqual(
            ocr.tesseract_location, self.tesseract_path
        )
        self.assertFalse(ocr.preprocess)

        text = ocr.ocr_meaningful_text(save_output=True)

        self.assertIsInstance(ocr.text, str)
        self.assertIsInstance(text, str)
        self.assertEqual(text, ocr.text)
        assert os.path.exists("OCR.png")
        assert os.path.exists("output.txt")
        assert not os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("output.txt")

    def test_ocr_with_real_image(self):

        ocr = OCR(
            True,
            self.path_real,
            self.tesseract_path if platform.system() == "Windows" else None,
        )

        self.assertEqual(ocr.path, "preprocessed.png")
        self.assertIsNone(
            ocr.tesseract_location
        ) if platform.system() != "Windows" else self.assertEqual(
            ocr.tesseract_location, self.tesseract_path
        )
        self.assertTrue(ocr.preprocess)

        text = ocr.ocr_meaningful_text()

        self.assertIsInstance(ocr.text, str)
        self.assertIsInstance(text, str)
        self.assertEqual(text, ocr.text)
        assert os.path.exists("OCR.png")
        assert os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech()

        assert os.path.exists("audio.mp3")

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("preprocessed.png")

    def test_ocr_sign_board(self):
        ocr = OCR(
            False,
            self.path_sign_board,
        )

        self.assertEqual(ocr.path, self.path_sign_board)
        self.assertFalse(ocr.preprocess)

        text = ocr.ocr_sparse_text(save_output=True)

        self.assertIsInstance(ocr.text, str)
        self.assertIsInstance(text, str)
        self.assertEqual(text, ocr.text)
        assert os.path.exists("OCR.png")
        assert os.path.exists("output.txt")
        assert not os.path.exists("preprocessed.png")
        assert not os.path.exists("audio.mp3")

        ocr.text_to_speech(lang="hi")

        assert os.path.exists("audio.mp3")

        os.remove("audio.mp3")
        os.remove("OCR.png")
        os.remove("output.txt")

    def test_ocr_invoices(self):
        ocr = OCR(
            False,
            self.path_invoice,
        )

        self.assertEqual(ocr.path, self.path_invoice)
        self.assertFalse(ocr.preprocess)

        text = ocr.ocr_sparse_text()

        self.assertIsInstance(ocr.text, str)
        self.assertIsInstance(text, str)
        self.assertEqual(text, ocr.text)
        assert os.path.exists("OCR.png")
        assert not os.path.exists("preprocessed.png")

        extracted_info = ocr.process_extracted_text_from_invoice()

        self.assertIsInstance(extracted_info, dict)
        self.assertIsInstance(ocr.extracted_info, dict)
        self.assertEqual(ocr.extracted_info, extracted_info)
        self.assertTrue(
            "price" in extracted_info
            and "date" in extracted_info
            and "place" in extracted_info
            and "order_number" in extracted_info
            and "phone_number" in extracted_info
            and "post_processed_word_list" in extracted_info
        )
        self.assertIsInstance(extracted_info["price"], str)
        self.assertIsInstance(extracted_info["date"], list)
        self.assertTrue(len(extracted_info["date"]) == 0)
        self.assertIsInstance(extracted_info["place"], str)
        self.assertIsInstance(extracted_info["phone_number"], list)
        self.assertTrue(len(extracted_info["phone_number"]) == 1)
        self.assertIsInstance(extracted_info["order_number"], int)
        self.assertIsInstance(extracted_info["post_processed_word_list"], list)

        self.path_invoice = "images/1166-receipt.jpg"
        ocr = OCR(
            False,
            self.path_invoice,
        )

        self.assertEqual(ocr.path, self.path_invoice)
        self.assertFalse(ocr.preprocess)

        text = ocr.ocr_sparse_text()

        self.assertIsInstance(ocr.text, str)
        self.assertIsInstance(text, str)
        self.assertEqual(text, ocr.text)
        assert os.path.exists("OCR.png")
        assert not os.path.exists("preprocessed.png")

        extracted_info = ocr.process_extracted_text_from_invoice()

        self.assertIsInstance(extracted_info, dict)
        self.assertIsInstance(ocr.extracted_info, dict)
        self.assertEqual(ocr.extracted_info, extracted_info)
        self.assertTrue(
            "price" in extracted_info
            and "date" in extracted_info
            and "place" in extracted_info
            and "order_number" in extracted_info
            and "phone_number" in extracted_info
            and "post_processed_word_list" in extracted_info
        )
        self.assertIsInstance(extracted_info["price"], str)
        self.assertIsInstance(extracted_info["date"], list)
        self.assertTrue(len(extracted_info["date"]) == 1)
        self.assertIsInstance(extracted_info["place"], str)
        self.assertIsInstance(extracted_info["phone_number"], list)
        self.assertTrue(len(extracted_info["phone_number"]) == 0)
        self.assertIsInstance(extracted_info["order_number"], str)
        self.assertIsInstance(extracted_info["post_processed_word_list"], list)

        os.remove("OCR.png")


if __name__ == "__main__":
    unittest.main()
