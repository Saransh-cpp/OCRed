import math
from typing import Optional, Tuple, Union

import cv2
import numpy as np
import numpy.typing as npt
from scipy import ndimage
from skimage.filters import threshold_local

_dep_warn_inplace = "inplace is deprecated and was removed in v0.3.0; Preprocessor now alters self.img directly"
_dep_warn_overriden_image = "overriden_image is deprecated and was removed in v0.3.0; Preprocessor now only alters self.img"


class Preprocessor:
    """
    Preprocesses an image and makes it ready for OCR.

    Args:
        image:
            Path of the image or a numpy array.

    Examples:
        >>> import sys
        >>> sys.displayhook = lambda x: None
        >>> import cv2
        >>> from scipy import ndimage
        >>> from ocred import Preprocessor
        >>> # scan the image and copy the scanned image
        >>> preprocessed = Preprocessor("images/CosmosTwo.jpg")
        >>> # scan the image and copy the scanned image
        >>> preprocessed.scan()
        >>> orig = preprocessed.img.copy()
        >>> # remove noise
        >>> preprocessed.remove_noise()
        >>> # thicken the ink to draw Hough lines better
        >>> preprocessed.thicken_font()
        >>> # calculate the median angle of all the Hough lines
        >>> _, median_angle = preprocessed.rotate()
        >>> # rotate the original scanned image
        >>> rotated = ndimage.rotate(orig, median_angle)
        >>> # remove noise again
        >>> preprocessed = Preprocessor(rotated)
        >>> preprocessed.remove_noise()
        >>> cv2.imwrite("preprocessed.png", preprocessed.img)
        True
    """

    def __init__(
        self,
        image: Union[str, Union[npt.NDArray[np.int64], npt.NDArray[np.float64]]],
    ) -> None:
        if isinstance(image, str):
            self.img = cv2.imread(image)
        else:
            self.img = image

    def remove_noise(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[Union[bool, None]] = None,
        iterations: Optional[int] = 1,
        overriden_image: Union[
            npt.NDArray[np.int64], npt.NDArray[np.float64], None
        ] = None
    ) -> Union[npt.NDArray[np.int64], npt.NDArray[np.float64]]:
        """
        Removes noise from an image.

        Args:
            save:
                Saves the resultant image.
            iterations:
                Number of times the image is processed.
            inplace:
                DANGER: Deprecated since version v0.3.0.
                Was intended to edit the image inplace, but never actually worked.
            overriden_image:
                DANGER: Deprecated since version v0.3.0.
                Was used to pass a new image to the method but was redundant and buggy.

        Returns:
            noise_free_image:
                The noise free image.
        """
        if inplace is not None:
            raise DeprecationWarning(_dep_warn_inplace)
        if overriden_image is not None:
            raise DeprecationWarning(_dep_warn_overriden_image)

        kernel: Union[npt.NDArray[np.int64]] = np.ones((1, 1), np.uint8)
        self.img = cv2.dilate(self.img, kernel, iterations=iterations)
        kernel = np.ones((1, 1), np.uint8)
        self.img = cv2.erode(self.img, kernel, iterations=iterations)
        self.img = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel)
        self.img = cv2.medianBlur(self.img, 3)

        if save:
            cv2.imwrite("noise_free.png", self.img)

        return self.img

    def thicken_font(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[Union[bool, None]] = None,
        iterations: Optional[int] = 2,
        overriden_image: Union[
            npt.NDArray[np.int64], npt.NDArray[np.float64], None
        ] = None
    ) -> Union[npt.NDArray[np.int64], npt.NDArray[np.float64]]:
        """
        Thickens the ink of an image.

        Args:
            save:
                Saves the resultant image.
            iterations:
                Number of times the image is processed.
            inplace:
                DANGER: Deprecated since version v0.3.0.
                Was intended to edit the image inplace, but never actually worked.
            overriden_image:
                DANGER: Deprecated since version v0.3.0.
                Was used to pass a new image to the method but was redundant and buggy.

        Returns:
            thickened_image:
                The thickened image.
        """
        if inplace is not None:
            raise DeprecationWarning(_dep_warn_inplace)
        if overriden_image is not None:
            raise DeprecationWarning(_dep_warn_overriden_image)

        self.img = cv2.bitwise_not(self.img)
        kernel: Union[npt.NDArray[np.int64]] = np.ones((2, 2), np.uint8)
        self.img = cv2.dilate(self.img, kernel, iterations=iterations)
        self.img = cv2.bitwise_not(self.img)

        if save:
            cv2.imwrite("thick_font.png", self.img)

        return self.img

    def scan(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[Union[bool, None]] = None,
        overriden_image: Union[
            npt.NDArray[np.int64], npt.NDArray[np.float64], None
        ] = None
    ) -> Union[npt.NDArray[np.int64], npt.NDArray[np.float64]]:
        """
        Transforms an image/document view into B&W view (proper scanned colour scheme).

        Args:
            save:
                Saves the resultant image.
            inplace:
                DANGER: Deprecated since version v0.3.0.
                Was intended to edit the image inplace, but never actually worked.
            overriden_image:
                DANGER: Deprecated since version v0.3.0.
                Was used to pass a new image to the method but was redundant and buggy.

        Returns:
            scanned_image:
                The scanned image.
        """
        if inplace is not None:
            raise DeprecationWarning(_dep_warn_inplace)
        if overriden_image is not None:
            raise DeprecationWarning(_dep_warn_overriden_image)

        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        thr = threshold_local(self.img, 11, offset=10, method="gaussian")
        self.img = (self.img > thr).astype("uint8") * 255

        if save:
            cv2.imwrite("scanned.png", self.img)

        return self.img

    def rotate(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[Union[bool, None]] = None,
        overriden_image: Union[
            npt.NDArray[np.int64], npt.NDArray[np.float64], None
        ] = None
    ) -> Tuple[Union[npt.NDArray[np.int64], npt.NDArray[np.float64]], float]:
        """
        Rotates an image for a face-on view (view from the top).

        Args:
            save:
                Saves the resultant image.
            inplace:
                DANGER: Deprecated since version v0.3.0.
                Was intended to edit the image inplace, but never actually worked.
            overriden_image:
                DANGER: Deprecated since version v0.3.0.
                Was used to pass a new image to the method but was redundant and buggy.

        Returns:
            rotated_image:
                The rotated image.
            median_angle:
                The angly by which it is rotated.
        """
        if inplace is not None:
            raise DeprecationWarning(_dep_warn_inplace)
        if overriden_image is not None:
            raise DeprecationWarning(_dep_warn_overriden_image)

        img_edges = cv2.Canny(self.img, 100, 100, apertureSize=3)
        lines = cv2.HoughLinesP(
            img_edges,
            rho=1,
            theta=np.pi / 180.0,
            threshold=160,
            minLineLength=100,
            maxLineGap=10,
        )

        angles = []
        for [[x1, y1, x2, y2]] in lines:
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            angles.append(angle)

        median_angle = float(np.median(angles))
        self.img = ndimage.rotate(self.img, median_angle)

        if save:
            cv2.imwrite("rotated.png", self.img)

        return self.img, median_angle
