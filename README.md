# OCR module for AiView

This module is the base module for all the OCR related things that will be performed in AiView.

## Structure
`OCR` is performed using the [OCR]() class and preprocessing of an image is performed using the `Preprocessor` class. All the details are available in the docstrings.

## Installation
1. Install Tesseract for your OS
The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)
2. Clone this repository
```
git clone https://github.com/
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

## Usage example
```py
import aiview_ocr

help(aiview_ocr.OCR)

ocr = aiview_ocr.OCR(
    False, # is_scanned
    "path/to/an/image", # path
    r"D:\Saransh\Softwares\Tesseract-OCR\tesseract.exe", # tesseract_location
)
ocr.ocr()
ocr.text_to_speech()
```

## Testing
The tests are present in the `tests` directory. New tests must be added with any additional features.

To run the tests -
```
python -m unittest
```