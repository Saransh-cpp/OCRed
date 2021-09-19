import os
import cv2
import pytesseract
from gtts import gTTS
from aiview_ocr.preprocessing import Preprocessor


class OCR:
    """
    Performs OCR on a given image, saves an image with boxes around the words, and
    converts the extracted text to an MP3 file.

    Parameters
    ----------
    is_scanned : bool
        Set True if the image is of a scanned page or an e-book.
        When set to False, the image is treated as a real life photo and is therefore
        processed before OCRing.
    path : str
        Path of the image to be used.
    tesseract_location : str
        Location of the executable file of Tesseract.
    """

    def __init__(self, is_scanned, path, tesseract_location):
        self.path = path
        self.is_scanned = is_scanned
        self.tesseract_location = tesseract_location

        if not self.is_scanned:
            preprocess = Preprocessor(self.path)
            preprocessed = preprocess.scan()
            preprocess.rotate(image=preprocessed, save=True)
            self.path = "rotated.png"

    def ocr(self):
        """
        Performs OCR on the image and saves the image with boxes around the words.
        """
        # specifying tesseract's installation path
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_location

        # reading the image
        img = cv2.imread(self.path)
        image_height, image_width, _ = img.shape

        # extracting the text
        self.text = pytesseract.image_to_string(img, config="-l eng --oem 1")
        print(self.text)

        # adding boxes around the words
        boxes = pytesseract.image_to_data(img)
        for z, box in enumerate(boxes.splitlines()):
            if z != 0:
                box = box.split()

                # if the data has a word
                if len(box) == 12:

                    x, y = int(box[6]), int(box[7])
                    h, w = int(box[8]), int(box[9])

                    cv2.rectangle(img, (x, y), (x + h, y + w), (0, 0, 255), 1)

        cv2.imwrite("OCR.png", img)
        cv2.destroyAllWindows()

    def text_to_speech(self):
        """
        Converts the extracted text to speech and save it as an MP3 file.
        """
        self.text = self.text.replace("-\n", "").replace("\n", " ")
        speech = gTTS(self.text, lang="en", tld="com")
        speech.save("audio.mp3")
