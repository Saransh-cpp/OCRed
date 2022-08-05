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
