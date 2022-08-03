import re
from typing import Any, Dict, List, Optional, Union

import cv2
import easyocr
import nltk
import pytesseract
from gtts import gTTS
from scipy import ndimage

from ocred.preprocessing import Preprocessor


class OCR:
    """
    Performs OCR on a given image, saves an image with boxes around the words, and
    converts the extracted text to an MP3 file.

    Add Tesseract OCR's installation location in PATH for functions using it to work.

    Args:

        preprocess:
            Set True if the image is a real life photo of some large meaningful (page of a
            book). Usually set to False when OCRing using `ocr_meaningful_text` to
            preprocess the image.
            Set False if the image is a scanned photo (an e-book). It will not be
            pre-processed before OCRing.
            All the preprocessing is performed inplace to maintain efficiency. Use the
            `Preprocessor` class manually to have more control!
        path:
            Path of the image to be used.

    Examples:

        >>> import sys
        >>> sys.displayhook = lambda x: None
        >>> import ocred
        >>> ocr = ocred.OCR(
        ...     False, # is_scanned -> to preprocess the image
        ...     "./images/Page.png"
        ... )
        >>> ocr.ocr_meaningful_text(save_output=True)
        >>> ocr.text_to_speech()
    """

    def __init__(self, preprocess: bool, path: str) -> None:
        self.path = path
        self.preprocess = preprocess

        if self.preprocess:
            preprocessed = Preprocessor(self.path)

            # scan the image and copy the scanned image
            scanned = preprocessed.scan(inplace=True)
            orig = scanned.copy()

            # remove noise
            noise_free = preprocessed.remove_noise(
                inplace=True, overriden_image=scanned
            )

            # thicken the ink to draw Hough lines better
            thickened = preprocessed.thicken_font(
                inplace=True, overriden_image=noise_free
            )

            # calculate the median angle of all the Hough lines
            _, median_angle = preprocessed.rotate(
                inplace=True, overriden_image=thickened
            )

            # rotate the original scanned image
            rotated = ndimage.rotate(orig, median_angle)

            # remove noise again
            final_img = preprocessed.remove_noise(inplace=True, overriden_image=rotated)

            cv2.imwrite("preprocessed.png", final_img)
            self.path = "preprocessed.png"

    def ocr_meaningful_text(self, *, save_output: Optional[bool] = False) -> str:
        """
        Performs OCR on long meaningful text documents and saves the image with boxes
        around the words. For example - books, PDFs etc.

        Args:
            save_output:
                Saves the text to `output.txt` file.

        Returns:
            text:
                The extracted text.
        """
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
        self,
        *,
        languages: Optional[List[str]] = ["en", "hi"],
        decoder: Optional[str] = "greedy",
        save_output: Optional[bool] = False,
    ) -> str:
        """
        Performs OCR on sparse text and saves the image with boxes around the words.
        This method can be used to OCR documents in which the characters don't form any
        proper/meaningful sentences, or if there are very less meaningful sentences,
        for example - bills, sign-boards etc.

        Args:
            languages:
                A list of languages that the signboard possible has.
                Note: Provide only the languages that are present in the image, adding
                additional languages misguides the model.
            decoder:
                If the document has a larger number of meaningful sentences then use
                "beamsearch". For most of the cases "greedy" works very well.
            save_output:
                Saves the text to `output.txt` file.

        Returns:
            text:
                The extracted text.
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

    def process_extracted_text_from_invoice(self) -> Dict[str, Any]:
        """
        This method processes the extracted text from invoices, and returns some useful
        information.

        Returns:
            extracted_info:
                The extracted information.
        """
        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("stopwords")

        self.extracted_info = {}
        self.text_list = self.text.split(" ")

        # find date
        date_re = re.compile(
            r"^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|\/)([1-9]|0[1-9]|1[0-2])(\.|-|\/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$",
        )
        date = list(filter(date_re.match, self.text_list))

        # find phone number
        phone_number_re = re.compile(
            r"((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}",
        )
        phone_number = list(filter(phone_number_re.match, self.text_list))

        # find place
        place = self.detailed_text[0][-2]

        # remove puntuations and redundant words
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        removed_punctuation = tokenizer.tokenize(self.text)

        stop_words = set(nltk.corpus.stopwords.words("english"))
        post_processed_word_list = [
            w for w in removed_punctuation if w not in stop_words
        ]

        # find order number
        order_number: Union[str, int] = ""
        for i in range(len(post_processed_word_list)):
            if post_processed_word_list[i].lower() == "order":
                try:
                    order_number = int(post_processed_word_list[i + 1])
                except Exception:
                    order_number = post_processed_word_list[i + 2]
                break

        # find total price
        price: Union[List[Any], str] = ""

        # try finding a number with Rs, INR, ₹ or रे in front of it or Rs, INR at the end
        # of it
        try:
            price = re.findall(
                r"(?:Rs\.?|INR|₹\.?|रे\.?)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)",
                self.text,
            )
            price = list(map(float, price))
            price = max(price)
        # try finding numbers with "grand total" or "total" written in front of them
        except ValueError:
            lowered_list = [x.lower() for x in post_processed_word_list]
            if "grand" in lowered_list:
                indices = [i for i, x in enumerate(lowered_list) if x == "grand"]
                i = indices[-1]
                price = post_processed_word_list[i + 2]
            elif "total" in lowered_list:
                indices = [i for i, x in enumerate(lowered_list) if x == "total"]
                i = indices[-1]
                price = post_processed_word_list[i + 1]

        self.extracted_info.update(
            {
                "price": price,
                "date": date,
                "place": place,
                "order_number": order_number,
                "phone_number": phone_number,
                "post_processed_word_list": post_processed_word_list,
            }
        )

        return self.extracted_info

    def save_output(self) -> None:
        """Saves the extracted text in the `output.txt` file."""
        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.text)
        f.close()

    def text_to_speech(self, *, lang: Optional[str] = "en") -> None:
        """
        Converts the extracted text to speech and save it as an MP3 file.

        Args:
            lang:
                Language of the processed text.
        """
        speech = gTTS(self.text, lang="en", tld="com")
        speech.save("audio.mp3")
