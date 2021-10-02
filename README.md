# OCR module for AiView

[![aiview_ocr](https://github.com/Saransh-cpp/aiview_ocr/actions/workflows/aiview_ocr.yml/badge.svg)](https://github.com/Saransh-cpp/aiview_ocr/actions/workflows/aiview_ocr.yml)

This module is the base module for all the OCR related things that will be performed in AiView.

## Structure
`OCR` is performed using the [`OCR`](https://github.com/Saransh-cpp/aiview_ocr/blob/main/aiview_ocr/ocr.py) class and preprocessing of an image is performed using the [`Preprocessor`](https://github.com/Saransh-cpp/aiview_ocr/blob/main/aiview_ocr/preprocessing.py) class. All the details are available in the docstrings.

## Installation
1. Install Tesseract for your OS

The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

2. Clone this repository
```
git clone https://github.com/Saransh-cpp/aiview_ocr
```
3. Change directory
```
cd aiview_ocr
```
4. Create a wheel file
```
python setup.py bdist_wheel
```
5. Install the package using the wheel file
```
cd dist
python -m pip install aiview_ocr-0.1.0-py3-none-any.whl
```

**NOTE**: To update the package, first uninstall the existing package and then follow the same steps.

## Usage example
```py
import aiview_ocr

help(aiview_ocr.OCR)

ocr = aiview_ocr.OCR(
    False, # is_scanned
    "path/to/an/image", # path
    r"D:\Saransh\Softwares\Tesseract-OCR\tesseract.exe", # tesseract_location
)
ocr.ocr_book()
ocr.text_to_speech()
```

## Testing
The tests are present in the `tests` directory. New tests must be added with any additional features.

To run the tests -
```
python -m unittest
```
