# OCRed

[![CI](https://github.com/Saransh-cpp/OCRed/actions/workflows/ci.yml/badge.svg)](https://github.com/Saransh-cpp/OCRed/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/ocred/badge/?version=latest)](https://ocred.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Saransh-cpp/OCRed/main.svg)](https://results.pre-commit.ci/latest/github/Saransh-cpp/OCRed/main)
[![codecov](https://codecov.io/gh/Saransh-cpp/OCRed/branch/main/graph/badge.svg?token=L6ObHKhaZ7)](https://codecov.io/gh/Saransh-cpp/OCRed)
[![discussion](https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github)](https://github.com/Saransh-cpp/OCRed/discussions)

[![Python Versions](https://img.shields.io/pypi/pyversions/ocred)](https://pypi.org/project/ocred/)
[![Package Version](https://badge.fury.io/py/ocred.svg)](https://pypi.org/project/ocred/)
[![PyPI Downloads](https://pepy.tech/badge/ocred)](https://pepy.tech/project/ocred)
![License](https://img.shields.io/github/license/Saransh-cpp/OCRed?color=blue)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-BADGE:END -->

`OCRed` (pronounced as _OCR'd_) provides clever, simple, and intuitive wrapper functionalities for OCRing specific text material. You don't want to learn `OCR` or the libraries that will help you perform `OCR`, but you need to `OCR` something? This friendly neighborhood library hides all of that stuff under simple functions like `ocr_meaningful_text()`.

In other words, instead of manual preprocessing, looking for an OCR library, learning the library, then finally getting what you were looking for, use `OCRed` instead.

On the other hand, if you want to learn `OCR` and use the famous `OCR` libraries by yourself, then this library is not for you. But, it still can be a good start for your journey!

## Structure

`OCR` is performed using the [`OCR`](https://github.com/Saransh-cpp/OCRed/blob/main/ocred/ocr.py) class and preprocessing of an image is performed using the [`Preprocessor`](https://github.com/Saransh-cpp/OCRed/blob/main/ocred/preprocessing.py) class. All the details are available in the [documentation](https://ocred.readthedocs.io/en/latest/).

## Installation

1. Install Tesseract for your OS and add it to PATH

The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

2. Use `pip` magic

`OCRed` uses modern `Python` packaging and can be installed using `pip` -

```
python -m pip install ocred
```

## Usage example

```py
# OCRing a book
import ocred

ocr = ocred.OCR(
    False, # is_scanned -> to preprocess the image
    "path/to/an/image", # path
)
ocr.ocr_meaningful_text(save_output=True)
```

```py
# OCRing a signboard
import ocred

ocr = ocred.OCR(
    True, # is_scanned -> sign boards don't need to be preprocessed
    "path/to/an/image", # path
)
extracted_text = ocr.ocr_sparse_text()
print(extracted_text)
```

```py
# OCRing an invoice
import ocred

ocr = ocred.OCR(
    True, # is_scanned -> invoices don't need to be preprocessed
    "path/to/an/image", # path
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
from ocred import Preprocessor

preprocessed = Preprocessor("path/to/img.jpg")

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
```

## Testing

The tests are present in the `tests` directory. New tests must be added with any additional features.

To run the tests -

```
pytest
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
organisms of our globe, including hydrogen, sodiurn, magnesiuia, and iron. May it not be thai, at least, the brighter stars are like our Sun, the upholding and energizing centres of systems of worlds, adapted to be the abode of living beings?  — William Hugeins, 1865  All my life I have wondered about the possibility of life elsewhere. What would it be like? Of what would it be made? All living things on our planet are constructed of organic molecules ~ complex microscopic architectures in which the carbon atom plays a central role. There was once a time before life, when the Earth was barren and utterly desolate. Our world is now overflowing with life. How did it come about? How, in the absence of life, were carbon-based organic molecules made? How did the first living things arise? How did life evolve to produce beings as elaborate and complex as we, able to explore the mystery of Our Own origins? And on ihe countless other planets that many circle other suns, is there life also? Is extraterrestrial life, if it exists, based on the same organic molecules as life on Earth? Do the beings of other worlds look much like life on Earth? Or are they stunningly different — other adaptations to other environments? What else is possible? The nature of life on Earth and the search for life elsewhere are two sides of the sarne question — the search for who we are.  In the great dark between the stars there are clouds of gas and dust and organic matter. Dozens of different kinds of organic molecules have been found there by radio telescopes. The abundance of these molecules suggests that the stuff of life is everywhere. Perhaps the origin and evolution of life is, given enough time, a cosmic inevitability. On some of the billions of planets in the Milky Way Galaxy, life may never arise. On others, it May arise and die out, or never evolve beyond its simplest forms. And on some small fraction of worlds there may 35
```

## Contributing

If you want to contribute to `OCRed` (thanks!), please have a look at our [Contributing Guide](https://github.com/Saransh-cpp/OCRed/blob/main/CONTRIBUTING.md).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://saransh-cpp.github.io/"><img src="https://avatars.githubusercontent.com/u/74055102?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Saransh</b></sub></a><br /><a href="https://github.com/Saransh-cpp/OCRed/commits?author=Saransh-cpp" title="Code">💻</a> <a href="https://github.com/Saransh-cpp/OCRed/issues?q=author%3ASaransh-cpp" title="Bug reports">🐛</a> <a href="#content-Saransh-cpp" title="Content">🖋</a> <a href="https://github.com/Saransh-cpp/OCRed/commits?author=Saransh-cpp" title="Documentation">📖</a> <a href="#design-Saransh-cpp" title="Design">🎨</a> <a href="#example-Saransh-cpp" title="Examples">💡</a> <a href="#ideas-Saransh-cpp" title="Ideas, Planning, & Feedback">🤔</a> <a href="#infra-Saransh-cpp" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#maintenance-Saransh-cpp" title="Maintenance">🚧</a> <a href="#platform-Saransh-cpp" title="Packaging/porting to new platform">📦</a> <a href="https://github.com/Saransh-cpp/OCRed/pulls?q=is%3Apr+reviewed-by%3ASaransh-cpp" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/Saransh-cpp/OCRed/commits?author=Saransh-cpp" title="Tests">⚠️</a> <a href="#tutorial-Saransh-cpp" title="Tutorials">✅</a> <a href="#mentoring-Saransh-cpp" title="Mentoring">🧑‍🏫</a></td>
    <td align="center"><a href="https://github.com/priyanshi-git"><img src="https://avatars.githubusercontent.com/u/82112540?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Priyanshi Goel</b></sub></a><br /><a href="https://github.com/Saransh-cpp/OCRed/issues?q=author%3Apriyanshi-git" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
