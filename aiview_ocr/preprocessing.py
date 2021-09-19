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
    Methods
    -------
    scan(save=False):
        Transforms the image view into black and white (proper scanned colour scheme).
    rotate(image=None, save=False, resize_height=500):
        Automatically rotates the image to a straight (top-down, face-on) view.
    """

    def __init__(self, path):
        self.path = path

    def scan(self, save=False):
        """
        Transforms an image/document view into B&W view (proper scanned colour scheme).

        Parameters
        ----------
        save : bool (default = False)
            Saves the image.
        Returns
        -------
        Resized image (array)
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

    def rotate(self, image=None, save=False, resize_height=500):
        """
        Rotates an image for a face-on view (view from the top).

        Parameters
        ----------
        image : array (default = None (image located at `path`))
            Pass an image to be rotated.
        save : bool (default = False)
            Saves the rotated image.
        resize_height : int (default = 500)
            Final height to resize an image to (in pixels)
        Returns
        -------
        Rotated image (array)
        """

        # read the original image, copy it,
        # rotate it
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
            # Drawing Hough lines
            # cv2.line(image, (x1, y1), (x2, y2), (128,0,0), 30)
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

        # average angles
        median_angle = np.median(angles)
        # actual rotate
        image = ndimage.rotate(image, median_angle)

        if save:
            # Saving an image itself
            cv2.imwrite("rotated.png", image)
        return image
