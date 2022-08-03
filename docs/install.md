# Installation

Follow the steps below to install `ocred` locally.

## Create a virtual environment

Create and activate a virtual environment

```bash
python -m venv env

. env/bin/activate
```

## Install OCRed

- Install Tesseract for your OS and add it to PATH

The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

- `pip` magic

`OCRed` uses modern `Python` packaging and can be installed using `pip` -

```
python -m pip install ocred
```

## Build OCRed from source

If you want to develop `OCRed`, or use its latest commit (!can be unstable!), you might want to install it from the source -

- Install Tesseract for your OS and add it to PATH

The installation guide is available [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)

- Clone this repository

```bash
git clone https://github.com/Saransh-cpp/OCRed
```

- Change directory

```bash
cd OCRed
```

- Install the package in editable mode with the "dev" dependencies

```bash
python -m pip install -e ".[dev]"
```

Feel free to read our [Contributing Guide](https://github.com/Saransh-cpp/OCRed/blob/main/CONTRIBUTING.md) for more information on developing `OCRed`.
