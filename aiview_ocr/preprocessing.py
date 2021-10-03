import cv2
import math
import numpy as np
from scipy import ndimage
from skimage.filters import threshold_local


class Preprocessor:
    """
    Preprocesses an image and makes it ready for OCR.

    Parameters
    ----------
    path : str
        Path of the image.

    """

    def __init__(self, path):
        self.path = path

    def remove_noise(image):

        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return image

    def thicken_font(image):

        image = cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return image

    def scan(self, save=False):
        """
        Transforms an image/document view into B&W view (proper scanned colour scheme).

        Parameters
        ----------
        save : bool (default = False)
            Saves the image.
        Returns
        -------
        scanned image (array)
        """

        # apply threshold to "scannify" it
        image = cv2.imread(self.path)

        # convert our image to grayscale, apply threshold
        # to create scanned paper effect
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thr = threshold_local(image, 11, offset=10, method="gaussian")
        image = (image > thr).astype("uint8") * 255

        if save:
            cv2.imwrite("preprocessed.png", image)

        return image

    def rotate(self, image=None, save=False):
        """
        Rotates an image for a face-on view (view from the top).

        Parameters
        ----------
        image : array (default = None (image located at `path`))
            Pass an image to be rotated.
        save : bool (default = False)
            Saves the rotated image.
        Returns
        -------
        rotated image (array)
        """

        # read the original image
        if image is None:
            image = cv2.imread(self.path)

        img_edges = cv2.Canny(image, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(
            img_edges,
            rho=1,
            theta=np.pi / 180.0,
            threshold=160,
            minLineLength=100,
            maxLineGap=10,
        )

        # calculate all the angles:
        angles = []
        for [[x1, y1, x2, y2]] in lines:
            # drawing Hough lines
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

        # median angle
        median_angle = np.median(angles)
        # actual rotate
        image = ndimage.rotate(image, median_angle)

        if save:
            # save the image
            cv2.imwrite("rotated.png", image)
        return image
