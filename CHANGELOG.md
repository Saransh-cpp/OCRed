# [v0.3.0](https://github.com/Saransh-cpp/OCRed/tree/v0.3.0)

## Breaking changes

- The arguments `inplace` and `overriden_image` have been deprecated and removed ([#71](https://github.com/Saransh-cpp/OCRed/pull/71))
- `Preprocessor` now alters the `img` attribute in each method, which can be accessed via `self.img` ([#71](https://github.com/Saransh-cpp/OCRed/pull/71))

## CI

- Added a separate CI pipeline for documentation ([#67](https://github.com/Saransh-cpp/OCRed/pull/67))

## Docs

- Revamped the UI and fixed minor UI bugs ([#67](https://github.com/Saransh-cpp/OCRed/pull/67))

## Tests

- Simplify and fasten tests ([#71](https://github.com/Saransh-cpp/OCRed/pull/71))

# [v0.2.0](https://github.com/Saransh-cpp/OCRed/tree/v0.2.0)

## Features

- Introduced `tesseract_config` argument to pass down configuration for Tesseract OCR Engine in `ocr_meaningful_text` ([#61](https://github.com/Saransh-cpp/OCRed/pull/61))
- Introduced `preserve_orientation` argument to preserve the orientation of OCRed text in `ocr_meaningful_text` ([#61](https://github.com/Saransh-cpp/OCRed/pull/61))
- `OCRed` can now be built from archive ([#56](https://github.com/Saransh-cpp/OCRed/pull/56))

## Breaking changes

- `ocr_sparse_text` now returns the output of `easyocr.Reader.readtext()` too ([#61](https://github.com/Saransh-cpp/OCRed/pull/61))
- `text_to_speech` is deprecated and removed ([#58](https://github.com/Saransh-cpp/OCRed/pull/58))

## Bug fixes

- Fixed the return value of `Preprocessor.remove_noise` ([#62](https://github.com/Saransh-cpp/OCRed/pull/62))

## Misc

- Added custom and more informative errors in the `OCR` class ([#61](https://github.com/Saransh-cpp/OCRed/pull/61))

## Maintenance

- Added a check for docs in the `CI` ([#59](https://github.com/Saransh-cpp/OCRed/pull/58))
- Fixed failing doc deployment ([#59](https://github.com/Saransh-cpp/OCRed/pull/58))
- Added `pyproject-fmt` pre-commit hook ([#57](https://github.com/Saransh-cpp/OCRed/pull/57))
- Fixed building from archive (tarballs) ([#56](https://github.com/Saransh-cpp/OCRed/pull/56))

# [v0.1.2](https://github.com/Saransh-cpp/OCRed/tree/v0.1.2)

## Maintenance

- Removed capitalisation from `PyPI`'s name (`OCRed` -> `ocred`) ([#52](https://github.com/Saransh-cpp/OCRed/pull/52))

## Bug fixes

- Fixed the `DeprecatingWarning` in `text_to_speech` ([#52](https://github.com/Saransh-cpp/OCRed/pull/52))
- Removed capitalisation from `PyPI`'s name (`OCRed` -> `ocred`) ([#52](https://github.com/Saransh-cpp/OCRed/pull/52))

# [v0.1.1](https://github.com/Saransh-cpp/OCRed/tree/v0.1.1)

## Maintenance

- Updated classifiers and links in `pyproject.toml` ([#49](https://github.com/Saransh-cpp/OCRed/pull/49))
- `nltk` is now not a part of the default dependencies ([#49](https://github.com/Saransh-cpp/OCRed/pull/49))
- Added `__version__` to `OCRed`'s namespace ([#50](https://github.com/Saransh-cpp/OCRed/pull/50))

## Deprecations

- `text_to_speech` is deprecated and will be removed in `v0.2.0`, use `gTTS` manually ([#50](https://github.com/Saransh-cpp/OCRed/pull/50))

# [v0.1.0](https://github.com/Saransh-cpp/OCRed/tree/v0.1.0)

- Added ability to `OCR` various textual mediums.
- Added ability to `Preprocess` images.
- Infrastructure built with `GitHub Actions`, `hatch`, `Codecov`, and `readthedocs`.
- Optimised algorithms with `inplace` edits.
- Added documentation with `mkdocstrings`.
- Other chore work like `pre-commit`, `nox` support, etc.
- Tests with `pytest` and coverage with `pytest-cov`.
