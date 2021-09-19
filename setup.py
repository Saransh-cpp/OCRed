from setuptools import setup, find_packages

f = open("requirements.txt", "r")
install_requires = f.read().splitlines()
f.close()

classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Customer Service",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
]

setup(
    name="aiview_ocr",
    version="0.1.0",
    license="MIT",
    description="The OCR module for AiView startup.",
    packages=find_packages(include=["aiview_ocr"]),
    classifiers=classifiers,
    install_requires=install_requires,
)
