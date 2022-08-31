import os

import cv2
import numpy as np
import pytest

from ocred.preprocessing import Preprocessor

path = "images/CosmosOne.jpg"


def test_deprecations_and_errors():
    pre = Preprocessor(path)
    img = cv2.imread(path)

    with pytest.raises(DeprecationWarning):
        pre.scan(inplace=True)
    with pytest.raises(DeprecationWarning):
        pre.scan(overriden_image=img)

    with pytest.raises(DeprecationWarning):
        pre.rotate(inplace=True)
    with pytest.raises(DeprecationWarning):
        pre.rotate(overriden_image=img)

    with pytest.raises(DeprecationWarning):
        pre.remove_noise(inplace=True)
    with pytest.raises(DeprecationWarning):
        pre.remove_noise(overriden_image=img)

    with pytest.raises(DeprecationWarning):
        pre.thicken_font(inplace=True)
    with pytest.raises(DeprecationWarning):
        pre.thicken_font(overriden_image=img)


def test_scan():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    scanned = pre.scan()
    assert isinstance(scanned, np.ndarray)
    assert isinstance(pre.img, np.ndarray)
    assert (scanned == pre.img).all()

    img = cv2.imread(path)
    pre = Preprocessor(img)
    scanned = pre.scan(save=True)
    assert isinstance(scanned, np.ndarray)
    assert isinstance(pre.img, np.ndarray)
    assert (scanned == pre.img).all()

    assert os.path.exists("scanned.png")
    os.remove("scanned.png")


def test_rotate():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    rotated, median_angle = pre.rotate(save=True)
    assert isinstance(median_angle, float)
    assert isinstance(rotated, np.ndarray)
    assert isinstance(pre.img, np.ndarray)
    assert (rotated == pre.img).all()
    assert os.path.exists("rotated.png")

    os.remove("rotated.png")


def test_remove_noise():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    noiseless = pre.remove_noise(save=True)
    assert isinstance(noiseless, np.ndarray)
    assert isinstance(pre.img, np.ndarray)
    assert (noiseless == pre.img).all()
    assert os.path.exists("noise_free.png")

    os.remove("noise_free.png")


def test_thicken_font():
    pre = Preprocessor(path)
    assert isinstance(pre.img, np.ndarray)

    thickened = pre.thicken_font(save=True)
    assert isinstance(thickened, np.ndarray)
    assert isinstance(pre.img, np.ndarray)
    assert (thickened == pre.img).all()
    assert os.path.exists("thick_font.png")

    os.remove("thick_font.png")
