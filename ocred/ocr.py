from __future__ import annotations

import re
import typing

import cv2
import easyocr
import pytesseract
from scipy import ndimage

from ocred.preprocessing import Preprocessor


class OCR:
    """
    Performs OCR on a given image, saves an image with boxes around the words, and
    converts the extracted text to an MP3 file.

    Add Tesseract OCR's installation location in PATH for functions using it to work.

    Args:

        preprocess:
            Set True if the image is a real life photo of some large meaningful (page of
            a book). Usually set to False when OCRing using `ocr_meaningful_text` to
            preprocess the image.
            Set False if the image is a scanned photo (an e-book). It will not be
            pre-processed before OCRing.
            Use the `Preprocessor` class manually to have more control!
        path:
            Path of the image to be used.

    Examples:
        >>> import sys
        >>> sys.displayhook = lambda x: None
        >>> import ocred
        >>> ocr = ocred.OCR(
        ...     False, # preprocess -> to preprocess the image
        ...     "./images/Page.png"
        ... )
        >>> ocr.ocr_meaningful_text(save_output=True)
    """

    def __init__(self, preprocess: bool, path: str) -> None:
        self.path = path
        self.preprocess = preprocess

        if self.preprocess:
            preprocessed = Preprocessor(self.path)

            # scan the image and copy the scanned image
            preprocessed.scan()
            orig = preprocessed.img.copy()

            # remove noise
            preprocessed.remove_noise()

            # thicken the ink to draw Hough lines better
            preprocessed.thicken_font()

            # calculate the median angle of all the Hough lines
            _, median_angle = preprocessed.rotate()

            # rotate the original scanned image
            rotated = ndimage.rotate(orig, median_angle)

            # remove noise again
            preprocessed = Preprocessor(rotated)
            preprocessed.remove_noise()

            cv2.imwrite("preprocessed.png", preprocessed.img)
            self.path = "preprocessed.png"

    def ocr_meaningful_text(
        self,
        *,
        tesseract_config: str | None = "-l eng --oem 1",
        preserve_orientation: bool | None = False,
        save_output: bool | None = False,
    ) -> str:
        """
        Performs OCR on long meaningful text documents and saves the image with boxes
        around the words. For example - books, PDFs etc.

        Args:
            tesseract_config:
                Configuration passed down to the Tesseract OCR Engine.
            preserve_orientation:
                Preserves the orientation of OCRed text.
            save_output:
                Saves the text to `output.txt` file.

        Returns:
            text:
                The extracted text.
        """
        # reading the image
        img = cv2.imread(self.path)

        # extracting the text
        self.text = pytesseract.image_to_string(img, config=tesseract_config)
        if not preserve_orientation:
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

    def ocr_sparse_text(
        self,
        *,
        languages: list[str] | None = ["en", "hi"],
        decoder: str | None = "greedy",
        save_output: bool | None = False,
    ) -> tuple[str, typing.Any]:
        """
        Performs OCR on sparse text and saves the image with boxes around the words.
        This method can be used to OCR documents in which the characters don't form
        any proper/meaningful sentences, or if there are very less meaningful sentences,
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
            detailed_text:
                Text with extra information (returned by easyocr.Reader.readtext()).
        """
        self.text = ""

        # reading the image using open-cv and easyocr
        img = cv2.imread(self.path)
        reader = easyocr.Reader(
            languages
        )  # slow for the first time (also depends upon CPU/GPU)
        self.detailed_text: typing.Any = reader.readtext(
            self.path, decoder=decoder, batch_size=5
        )

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

        return self.text, self.detailed_text

    def process_extracted_text_from_invoice(self) -> dict[str, typing.Any]:
        """
        This method processes the extracted text from invoices, and returns some useful
        information.

        Returns:
            extracted_info:
                The extracted information.
        """
        if not hasattr(self, "detailed_text"):
            raise ValueError("no invoice OCRed; OCR an invoice first")

        import nltk

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
        order_number: str | int = ""
        for i in range(len(post_processed_word_list)):
            if post_processed_word_list[i].lower() == "order":
                try:
                    order_number = int(post_processed_word_list[i + 1])
                except Exception:
                    order_number = post_processed_word_list[i + 2]
                break

        # find total price
        price: list[typing.Any] | str = ""

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
        if not hasattr(self, "text"):
            raise ValueError("no text OCRed; OCR a document first")
        f = open("output.txt", "w", encoding="utf-8")
        f.write(self.text)
        f.close()

    def text_to_speech(self, *, lang: str | None = "en") -> None:
        """
        DANGER: Deprecated since version v0.2.0.
        Instead, use gTTS manually.

        Converts the extracted text to speech and save it as an MP3 file.

        Args:
            lang:
                Language of the processed text.
        """
        raise DeprecationWarning(
            "text_to_speech is deprecated and was removed in v0.2.0; use gTTS manually",
        )
