import math
from typing import Optional, Tuple, Union

import cv2
import numpy as np
import numpy.typing as npt
from scipy import ndimage
from skimage.filters import threshold_local


class Preprocessor:
    """
    Preprocesses an image and makes it ready for OCR.

    Args:
        image:
            Path of the image or a numpy array.

    Examples:
        >>> import cv2
        >>> from scipy import ndimage
        >>> from ocred import Preprocessor
        >>> # scan the image and copy the scanned image
        >>> preprocessed = Preprocessor("images/CosmosTwo.jpg")
        >>> # scan the image and copy the scanned image
        >>> scanned = preprocessed.scan(inplace=True)
        >>> orig = scanned.copy()
        >>> # remove noise
        ... noise_free = preprocessed.remove_noise(
        ...     inplace=True, overriden_image=scanned
        ... )
        >>> # thicken the ink to draw Hough lines better
        >>> thickened = preprocessed.thicken_font(
        ...     inplace=True, overriden_image=noise_free
        ... )
        >>> # calculate the median angle of all the Hough lines
        >>> _, median_angle = preprocessed.rotate(
        ...     inplace=True, overriden_image=thickened
        ... )
        >>> # rotate the original scanned image
        >>> rotated = ndimage.rotate(orig, median_angle)
        >>> # remove noise again
        >>> final_img = preprocessed.remove_noise(inplace=True, overriden_image=rotated)
        >>> cv2.imwrite("preprocessed.png", final_img)
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
        inplace: Optional[bool] = False,
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
            inplace:
                Edits the image inplace.
            iterations:
                Number of times the image is processed.
            overriden_image:
                Overrides the image passes through the constructor.

        Returns:
            noise_free_image:
                The noise free image.
        """
        if not inplace:
            img = self.img.copy() if overriden_image is None else overriden_image.copy()
        else:
            img = self.img if overriden_image is None else overriden_image

        kernel: Union[npt.NDArray[np.int64]] = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=iterations)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.erode(img, kernel, iterations=iterations)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img = cv2.medianBlur(img, 3)

        if save:
            cv2.imwrite("noise_free.png", img)

        return self.img

    def thicken_font(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[bool] = False,
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
            inplace:
                Edits the image inplace.
            iterations:
                Number of times the image is processed.
            overriden_image:
                Overrides the image passes through the constructor.

        Returns:
            thickened_image:
                The thickened image.
        """
        if not inplace:
            img = self.img.copy() if overriden_image is None else overriden_image.copy()
        else:
            img = self.img if overriden_image is None else overriden_image

        img = cv2.bitwise_not(img)
        kernel: Union[npt.NDArray[np.int64]] = np.ones((2, 2), np.uint8)
        img = cv2.dilate(img, kernel, iterations=iterations)
        img = cv2.bitwise_not(img)

        if save:
            cv2.imwrite("thick_font.png", img)

        return img

    def scan(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[bool] = False,
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
                Edits the image inplace.
            overriden_image:
                Overrides the image passes through the constructor.

        Returns:
            scanned_image:
                The scanned image.
        """
        if not inplace:
            img = self.img.copy() if overriden_image is None else overriden_image.copy()
        else:
            img = self.img if overriden_image is None else overriden_image

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr = threshold_local(img, 11, offset=10, method="gaussian")
        img = (img > thr).astype("uint8") * 255

        if save:
            cv2.imwrite("scanned.png", img)

        return img

    def rotate(
        self,
        *,
        save: Optional[bool] = False,
        inplace: Optional[bool] = False,
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
                Edits the image inplace.
            overriden_image:
                Overrides the image passes through the constructor.

        Returns:
            rotated_image:
                The rotated image.
            median_angle:
                The angly by which it is rotated.
        """
        if not inplace:
            img = self.img.copy() if overriden_image is None else overriden_image.copy()
        else:
            img = self.img if overriden_image is None else overriden_image

        img_edges = cv2.Canny(img, 100, 100, apertureSize=3)
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
        img = ndimage.rotate(img, median_angle)

        if save:
            cv2.imwrite("rotated.png", img)

        return img, median_angle
