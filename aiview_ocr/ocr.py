import cv2
import easyocr
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
        Set True if the image is of a scanned page, e-book or of a signboard.
        When set to False, the image is treated as a real life photo and is therefore
        processed before OCRing.
    path : str
        Path of the image to be used.
    tesseract_location : str (default = None)
        Location of the executable file of Tesseract (usually used in Windows systems).
        This is only required for OCRing books.
    """

    def __init__(self, is_scanned, path, tesseract_location=None):
        self.path = path
        self.is_scanned = is_scanned
        self.tesseract_location = tesseract_location

        if not self.is_scanned:
            preprocess = Preprocessor(self.path)
            preprocessed = preprocess.scan()
            preprocess.rotate(image=preprocessed, save=True)
            self.path = "rotated.png"

    def ocr_book(self, save_output=False):
        """
        Performs OCR on a book's page and saves the image with boxes around the words.

        Parameters
        ==========
        save_output : bool (default = False)
            Saves the text to `output.txt` file.
        """
        # specifying tesseract's installation path
        if self.tesseract_location is not None:  # pragma: no cover
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_location

        # reading the image
        img = cv2.imread(self.path)

        # extracting the text
        self.text = pytesseract.image_to_string(img, config="-l eng --oem 1")
        self.text = self.text.replace("-\n", "").replace("\n", " ")

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

        if save_output:
            self.save_output()

        return self.text

    def ocr_sign_board(self, languages=["en", "hi"], save_output=False):
        """
        Performs OCR on a signboard and saves the image with boxes around the words.

        Parameters
        ==========
        languages : list (default = ["en", "hi"] where "en" = English and "hi" = Hindi)
            A list of languages that the signboard possible has.
        save_output : bool (default = False)
            Saves the text to `output.txt` file.
        """
        self.text = ""

        # reading the image using open-cv and easyocr
        img = cv2.imread(self.path)
        reader = easyocr.Reader(
            languages
        )  # slow for the first time (also depends upon CPU/GPU)
        result = reader.readtext(self.path)

        for text in result:

            # extracting the coordinates to highlight the text
            coords_lower = text[0][:2]
            coords_upper = text[0][2:4]

            coords_lower.sort(key=lambda x: x[0])
            pt1 = [int(x) for x in coords_upper[-1]]

            coords_lower.sort(key=lambda x: x[0])
            pt2 = [int(x) for x in coords_lower[-1]]

            # highlighting the text
            cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)

            self.text = self.text + " " + text[-2]

        cv2.imwrite("OCR.png", img)

        if save_output:
            self.save_output()

        return self.text

    def save_output(self):
        """
        Saves the extracted text in the `output.txt` file.
        """
        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.text)
        f.close()

    def text_to_speech(self, lang="en"):
        """
        Converts the extracted text to speech and save it as an MP3 file.

        Parameters
        ==========
        lang : str (default = "en" where "en" is English)
            Language of the processed text.
        """
        speech = gTTS(self.text, lang="en", tld="com")
        speech.save("audio.mp3")
