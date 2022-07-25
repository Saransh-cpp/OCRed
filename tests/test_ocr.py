import os

from ocred.ocr import OCR

path_scanned = "images/Page.png"
path_real = "images/CosmosOne.jpg"
path_sign_board = "images/signboard.jpg"
path_invoice = "images/1146-receipt.jpg"


def test_ocr_with_scanned_image():

    ocr = OCR(
        False,
        path_scanned,
    )

    assert ocr.path == path_scanned
    assert ocr.preprocess is False

    text = ocr.ocr_meaningful_text(save_output=True)

    assert isinstance(ocr.text, str)
    assert isinstance(text, str)
    assert text == ocr.text
    assert os.path.exists("OCR.png")
    assert os.path.exists("output.txt")
    assert not os.path.exists("preprocessed.png")
    assert not os.path.exists("audio.mp3")

    ocr.text_to_speech()

    assert os.path.exists("audio.mp3")

    os.remove("audio.mp3")
    os.remove("OCR.png")
    os.remove("output.txt")


def test_ocr_with_real_image():

    ocr = OCR(
        True,
        path_real,
    )

    assert ocr.path == "preprocessed.png"
    assert ocr.preprocess is True

    text = ocr.ocr_meaningful_text()

    assert isinstance(ocr.text, str)
    assert isinstance(text, str)
    assert text == ocr.text
    assert os.path.exists("OCR.png")
    assert os.path.exists("preprocessed.png")
    assert not os.path.exists("audio.mp3")

    ocr.text_to_speech()

    assert os.path.exists("audio.mp3")

    os.remove("audio.mp3")
    os.remove("OCR.png")
    os.remove("preprocessed.png")


def test_ocr_sign_board():
    ocr = OCR(
        False,
        path_sign_board,
    )

    assert ocr.path == path_sign_board
    assert ocr.preprocess is False

    text = ocr.ocr_sparse_text(save_output=True)

    assert isinstance(ocr.text, str)
    assert isinstance(text, str)
    assert text == ocr.text
    assert os.path.exists("OCR.png")
    assert os.path.exists("output.txt")
    assert not os.path.exists("preprocessed.png")
    assert not os.path.exists("audio.mp3")

    ocr.text_to_speech(lang="hi")

    assert os.path.exists("audio.mp3")

    os.remove("audio.mp3")
    os.remove("OCR.png")
    os.remove("output.txt")


def test_ocr_invoices():
    global path_invoice
    ocr = OCR(
        False,
        path_invoice,
    )

    assert ocr.path == path_invoice
    assert ocr.preprocess is False

    text = ocr.ocr_sparse_text()

    assert isinstance(ocr.text, str)
    assert isinstance(text, str)
    assert text == ocr.text
    assert os.path.exists("OCR.png")
    assert not os.path.exists("preprocessed.png")

    extracted_info = ocr.process_extracted_text_from_invoice()

    assert isinstance(extracted_info, dict)
    assert isinstance(ocr.extracted_info, dict)
    assert ocr.extracted_info == extracted_info
    assert (
        "price" in extracted_info
        and "date" in extracted_info
        and "place" in extracted_info
        and "order_number" in extracted_info
        and "phone_number" in extracted_info
        and "post_processed_word_list" in extracted_info
    ) is True
    assert isinstance(extracted_info["price"], str)
    assert isinstance(extracted_info["date"], list)
    assert len(extracted_info["date"]) == 0
    assert isinstance(extracted_info["place"], str)
    assert isinstance(extracted_info["phone_number"], list)
    assert len(extracted_info["phone_number"]) == 1
    assert isinstance(extracted_info["order_number"], int)
    assert isinstance(extracted_info["post_processed_word_list"], list)

    path_invoice = "images/1166-receipt.jpg"
    ocr = OCR(
        False,
        path_invoice,
    )

    assert ocr.path == path_invoice
    assert ocr.preprocess is False

    text = ocr.ocr_sparse_text()

    assert isinstance(ocr.text, str)
    assert isinstance(text, str)
    assert text == ocr.text
    assert os.path.exists("OCR.png")
    assert not os.path.exists("preprocessed.png")

    extracted_info = ocr.process_extracted_text_from_invoice()

    assert isinstance(extracted_info, dict)
    assert isinstance(ocr.extracted_info, dict)
    assert ocr.extracted_info == extracted_info
    assert (
        "price" in extracted_info
        and "date" in extracted_info
        and "place" in extracted_info
        and "order_number" in extracted_info
        and "phone_number" in extracted_info
        and "post_processed_word_list" in extracted_info
    ) is True
    assert isinstance(extracted_info["price"], str)
    assert isinstance(extracted_info["date"], list)
    assert len(extracted_info["date"]) == 1
    assert isinstance(extracted_info["place"], str)
    assert isinstance(extracted_info["phone_number"], list)
    assert len(extracted_info["phone_number"]) == 0
    assert isinstance(extracted_info["order_number"], str)
    assert isinstance(extracted_info["post_processed_word_list"], list)

    os.remove("OCR.png")
