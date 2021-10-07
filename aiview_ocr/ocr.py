import re
import cv2
import nltk
import easyocr
import pytesseract
from gtts import gTTS
from scipy import ndimage
from aiview_ocr.preprocessing import Preprocessor


class OCR:
    """
    Performs OCR on a given image, saves an image with boxes around the words, and
    converts the extracted text to an MP3 file.

    Parameters
    ==========
    is_scanned : bool
        Set False if the image is a real life photo of some large meaningful (page of a
        book). Usually set to False when OCRing using `ocr_meaningful_text` to
        preprocess the image.
        Set True if the image is a scanned photo (an e-book). It will not be
        pre-processed before OCRing.
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

            # scan the image and copy the scanned image
            scanned = preprocess.scan()
            orig = scanned.copy()

            # remove noise
            noise_free = preprocess.remove_noise(scanned)

            # thicken the ink to draw Hough lines better
            thickened = preprocess.thicken_font(noise_free)

            # calculate the median angle of all the Hough lines
            _, median_angle = preprocess.rotate(thickened)

            # rotate the original scanned image
            preprocessed = ndimage.rotate(orig, median_angle)

            # remove noise again
            preprocessed = preprocess.remove_noise(preprocessed)

            cv2.imwrite("preprocessed.png", preprocessed)
            self.path = "preprocessed.png"

    def ocr_meaningful_text(self, save_output=False):
        """
        Performs OCR on long meaningful text documents and saves the image with boxes
        around the words. For example - books, PDFs etc.

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
        self.oriented_text = pytesseract.image_to_string(img, config="-l eng --oem 1")
        self.text = self.oriented_text.replace("-\n", "").replace("\n", " ")

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

    def ocr_sparse_text(
        self, languages=["en", "hi"], decoder="greedy", save_output=False
    ):
        """
        Performs OCR on sparse text and saves the image with boxes around the words.
        This method can be used to OCR documents in which the character don't form some
        proper/meaningful sentences or if there are very less meaningful sentences,
        for example - bills, sign-boards etc.

        Parameters
        ==========
        languages : list (default = ["en", "hi"] where "en" = English and "hi" = Hindi)
            A list of languages that the signboard possible has.
            Note: Provide only the languages that are present in the image, as adding
            additional languages misguides the model.
        decoder : str (default = "greedy)
            If the document has a larger number of meaningful sentences then use
            "beamsearch". For most of the cases "greedy" works very well.
        save_output : bool (default = False)
            Saves the text to `output.txt` file.
        """
        self.text = ""

        # reading the image using open-cv and easyocr
        img = cv2.imread(self.path)
        reader = easyocr.Reader(
            languages
        )  # slow for the first time (also depends upon CPU/GPU)
        self.detailed_text = reader.readtext(self.path, decoder=decoder, batch_size=5)

        for text in self.detailed_text:

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

    def process_extracted_text_from_invoice(self):

        # TODO: Try Order number, phone number

        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("stopwords")

        self.extracted_info = {}

        date = re.findall(r"\d+[/.-]\d+[/.-]\d+", self.text)

        place = self.detailed_text[0][-2]

        try:
            price = re.findall(r"[\₹](\d+(?:\.\d{1,2})?)", self.text)
            price = list(map(float, price))
            price = max(price)
        except Exception:
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            removed_punctuation = tokenizer.tokenize(self.text)

            stop_words = set(nltk.corpus.stopwords.words("english"))
            post_processed_word_list = [
                w for w in removed_punctuation if w not in stop_words
            ]

            for i in range(len(post_processed_word_list)):
                if post_processed_word_list[i].lower() == "total":
                    price = post_processed_word_list[i + 1]
                    break

        self.extracted_info.update(
            {
                "price": price,
                "date": date,
                "place": place,
                "post_processed_word_list": post_processed_word_list,
            }
        )

        return self.extracted_info

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
