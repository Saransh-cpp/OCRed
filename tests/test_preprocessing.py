import os

import cv2
import numpy as np

from ocred.preprocessing import Preprocessor

path = "images/CosmosOne.jpg"


def test_scan():
    pre = Preprocessor(path)
    assert pre.path == path

    img = pre.scan()
    assert isinstance(img, np.ndarray)

    img = pre.scan(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("scanned.png")

    os.remove("scanned.png")

    img = cv2.imread(path)

    img = pre.scan(image=img)
    assert isinstance(img, np.ndarray)


def test_rotate():
    pre = Preprocessor(path)
    assert pre.path == path

    img, median_angle = pre.rotate()
    assert isinstance(median_angle, float)
    assert isinstance(img, np.ndarray)

    img, median_angle = pre.rotate(save=True)
    assert isinstance(img, np.ndarray)
    assert isinstance(median_angle, float)
    assert os.path.exists("rotated.png")

    os.remove("rotated.png")

    img, median_angle = pre.rotate(image=img)
    img1, median_angle = pre.rotate(image=img)
    assert isinstance(median_angle, float)
    assert isinstance(img, np.ndarray)
    assert isinstance(img1, np.ndarray)
    np.testing.assert_array_equal(img, img1)


def test_remove_noise():
    pre = Preprocessor(path)
    assert pre.path == path

    img = pre.remove_noise()
    assert isinstance(img, np.ndarray)

    img = pre.remove_noise(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("noise_free.png")

    os.remove("noise_free.png")

    img = pre.remove_noise(image=img)
    assert isinstance(img, np.ndarray)


def test_thicken_font():
    pre = Preprocessor(path)
    assert pre.path == path

    img = pre.thicken_font()
    assert isinstance(img, np.ndarray)

    img = pre.thicken_font(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("thick_font.png")

    os.remove("thick_font.png")

    img = pre.thicken_font(image=img)
    assert isinstance(img, np.ndarray)
