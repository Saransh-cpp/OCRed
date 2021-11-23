# OCR module for AiView

[![aiview_ocr](https://github.com/AI-View/OCR/actions/workflows/aiview_ocr.yml/badge.svg)](https://github.com/AI-View/OCR/actions/workflows/aiview_ocr.yml)

This module is the base module for all the OCR related things that will be performed in [AiView](https://github.com/AI-View).

## Structure
`OCR` is performed using the [`OCR`](https://github.com/AI-View/OCR/blob/main/aiview_ocr/ocr.py) class and preprocessing of an image is performed using the [`Preprocessor`](https://github.com/AI-View/OCR/blob/main/aiview_ocr/preprocessing.py) class. All the details are available in the docstrings.

## Installation
1. Install Tesseract for your OS

The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

2. Clone this repository
```
git clone https://github.com/AI-View/OCR
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
# OCRing a book
import aiview_ocr

ocr = aiview_ocr.OCR(
    False, # is_scanned -> to preprocess the image
    "path/to/an/image", # path
    r"D:\Saransh\Softwares\Tesseract-OCR\tesseract.exe", # tesseract_location for windows users
    # r"/usr/bin/tesseract", # tesseract_location for linux users
    # if not working, search for tesseract location using linux terminal command 'which tesseract'
)
ocr.ocr_meaningful_text(save_output=True)
ocr.text_to_speech()
```
```py
# OCRing a signboard
import aiview_ocr

ocr = aiview_ocr.OCR(
    True, # is_scanned -> sign boards don't need to be preprocessed
    "path/to/an/image", # path
    # sign board OCR doesn't use Tesseract
)
extracted_text = ocr.ocr_sparse_text()
print(extracted_text)
```
```py
# OCRing an invoice
import aiview_ocr

ocr = aiview_ocr.OCR(
    True, # is_scanned -> invoices don't need to be preprocessed
    "path/to/an/image", # path
    # invoice OCR doesn't use Tesseract
)
extracted_text = ocr.ocr_sparse_text()
print(extracted_text)

extraxted_info = ocr.process_extracted_text_from_invoice()
print(extraxted_info)
```
```py
# manually preprocessing an image
import cv2
from scipy import ndimage
from aiview_ocr import Preprocessor

preprocess = Preprocessor("path/to/an/image")

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
```
## Testing
The tests are present in the `tests` directory. New tests must be added with any additional features.

To run the tests -
```
python -m unittest -v
```

## Some examples
![roof-500x500](https://user-images.githubusercontent.com/74055102/135721441-7516bbf1-da6f-498b-a30b-d381c66b187e.jpg)
![OCR](https://user-images.githubusercontent.com/74055102/135721446-5ea2e3f9-7cab-41f9-a1b0-52ff6707b0c2.png)
```
जयपुर JAIPUR 321 आगरा AGRA 554 श्री गगांनगर 242 SRIGANGANAGAR JODHPUR 261 जोधपुर
```
![Page](https://user-images.githubusercontent.com/74055102/133644506-3dcf08fc-36f9-404a-b1b7-65117a3f9869.png)
![OCR](https://user-images.githubusercontent.com/74055102/133644598-89551323-df51-45cc-8210-871b2c4dd756.png)
```
Preface  This book deals with computer architecture as well as computer organization and design. Computer architecture is concerned with the structure and behavior of the various functional modules of the computer and how they interact to provide the processing needs of the user. Computer organization is concerned with the way the hardware components are connected together to form a computer system. Computer design is concerned with the development of the hardware for the computer taking into consideration a given set of specifications. The book provides the basic knowledge necessary to understand the hardware operation of digital computers and covers the three subjects associated with computer hardware. Chapters 1 through 4 present the various digital components used in the organization and design of digital computers. Chapters 5 through 7 show the detailed steps that a designer must go through in order  to design an elementary basic computer. Chapters 8 through 10 deal with the organization and architecture of the central processing unit. Chapters 11 and 12 present the organization and architecture of input-output and memory. Chapter 13 introduces the concept of multiprocessing. The plan of the book is to present the simpler material first and introduce the more advanced subjects later, Thus, the first seven chapters cover material needed for the basic understanding of computer organization, design, and programming of a simple digital computer. The last six chapters present the organization and architecture of the separate functional units of the digital computer with an emphasis ‘on more advanced topics.  ‘The material in the third edition is organized  in the same manner as in the second edition and many of the features remain the same. The third edition, however, offers several improvements over the second edition. All chapters  ‘two (6 and 10) have been completely revised to bring the material up to date and to clarify the presentation. Two new chapters were added: chapter 9 on pipeline and vector processing, and chapter 13 on multiprocessors. Two sections deal with the reduced instruction set computer (RISC). Chapter 5 has been revised completely to simplify and clarify the design of the basic computer. New problems have been formulated for eleven of the thirteen chapters.  ‘The physical organization of a particular computer including its registers
```
![CosmosOne](https://user-images.githubusercontent.com/74055102/133640550-eba241af-db0a-46e3-9b24-b4219dd74cfd.jpg)
![preprocessed](https://user-images.githubusercontent.com/74055102/136529402-eb42d8fa-d987-4b09-bb36-8d5a477ed391.png)
![OCR](https://user-images.githubusercontent.com/74055102/136529362-9c82a1f2-ffde-4edc-a154-0692a3b219a8.png)
```
organisms of our globe, including hydrogen, sodiurn, magnesiuia, and iron. May it not be thai, at least, the brighter stars are like our Sun, the upholding and energizing centres of systems of worlds, adapted to be the abode of living beings?  — William Hugeins, 1865  All my life I have wondered about the possibility of life elsewhere. What would it be like? Of what would it be made? All living things on our planet are constructed of organic molecules ~ complex microscopic architectures in which the carbon atom plays a central role. There was once a time before life, when the Earth was barren and utterly desolate. Our world is now overflowing with life. How did it come about? How, in the absence of life, were carbon-based organic molecules made? How did the first living things arise? How did life evolve to produce beings as elaborate and complex as we, able to explore the mystery of Our Own origins? And on ihe countless other planets that mnay circle other suns, is there life also? Is extraterrestrial life, if it exists, based on the same organic molecules as life on Earth? Do the beings of other worlds look much like life on Earth? Or are they stunningly different — other adaptations to other environments? What else is possible? The nature of life on Earth and the search for life elsewhere are two sides of the sarne question — the search for who we are.  In the great dark between the stars there are clouds of gas and dust and organic matter. Dozens of different kinds of organic molecules have been found there by radio telescopes. The abundance of these molecules suggests that the stuff of life is everywhere. Perhaps the origin and evolution of life is, given enough time, a cosmic inevitability. On some of the billions of planets in the Milky Way Galaxy, life may never arise. On others, it May arise and die out, or never evolve beyond its simplest forms. And on some small fraction of worlds there may 35
```
