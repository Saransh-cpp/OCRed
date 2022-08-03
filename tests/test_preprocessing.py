import os

import cv2
import numpy as np

from ocred.preprocessing import Preprocessor

path = "images/CosmosOne.jpg"


def test_scan():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    img = pre.scan()
    assert isinstance(img, np.ndarray)

    img = pre.scan(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("scanned.png")

    os.remove("scanned.png")

    img = cv2.imread(path)
    pre = Preprocessor(img)

    image = pre.scan()
    assert isinstance(image, np.ndarray)

    orig = img.copy()
    _ = pre.scan(inplace=True, overriden_image=img)
    assert not np.testing.assert_array_equal(img, orig)


def test_rotate():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    img, median_angle = pre.rotate()
    assert isinstance(median_angle, float)
    assert isinstance(img, np.ndarray)

    img, median_angle = pre.rotate(save=True)
    assert isinstance(img, np.ndarray)
    assert isinstance(median_angle, float)
    assert os.path.exists("rotated.png")

    os.remove("rotated.png")

    img, median_angle = pre.rotate(overriden_image=img)
    img1, median_angle = pre.rotate(overriden_image=img)
    assert isinstance(median_angle, float)
    assert isinstance(img, np.ndarray)
    assert isinstance(img1, np.ndarray)
    np.testing.assert_array_equal(img, img1)

    orig = img.copy()
    _ = pre.rotate(inplace=True, overriden_image=img)
    assert not np.testing.assert_array_equal(img, orig)


def test_remove_noise():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    img = pre.remove_noise()
    assert isinstance(img, np.ndarray)

    img = pre.remove_noise(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("noise_free.png")

    os.remove("noise_free.png")

    img = pre.remove_noise(overriden_image=img)
    assert isinstance(img, np.ndarray)

    orig = img.copy()
    _ = pre.remove_noise(inplace=True, overriden_image=img)
    assert not np.testing.assert_array_equal(img, orig)


def test_thicken_font():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    img = pre.thicken_font()
    assert isinstance(img, np.ndarray)

    img = pre.thicken_font(save=True)
    assert isinstance(img, np.ndarray)
    assert os.path.exists("thick_font.png")

    os.remove("thick_font.png")

    img = pre.thicken_font(overriden_image=img)
    assert isinstance(img, np.ndarray)

    orig = img.copy()
    _ = pre.thicken_font(inplace=True, overriden_image=img)
    assert not np.testing.assert_array_equal(img, orig)
