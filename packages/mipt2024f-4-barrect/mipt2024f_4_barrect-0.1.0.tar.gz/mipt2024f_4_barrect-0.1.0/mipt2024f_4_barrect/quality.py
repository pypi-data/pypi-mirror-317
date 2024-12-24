import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.filters import threshold_otsu


def get_ssim(src: np.ndarray, rectified: np.ndarray, make_ssim_image: bool = False):
    """
    Calculate SSIM between original and rectified barcode

    :param src: Original barcode
    :param rectified: Rectified barcode
    :param make_ssim_image: Whether to produce ssim image
    :return: SSIM between original and rectified barcode
    """

    if src.shape != rectified.shape:
        raise ValueError("Image shape mismatch")

    gray1 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(rectified, cv2.COLOR_BGR2GRAY)

    return ssim(gray1, gray2, full=make_ssim_image)


def horizontal_projection(src: np.ndarray):
    """
    Calculate squash of binarized image on x-axis

    :param src: Source image
    :return: Array of column sums
    """

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    thresh = threshold_otsu(gray)
    binary = gray < thresh

    return np.sum(binary, axis=0)


def straightness(src: np.ndarray):
    """
    Calculate straightness of binary image

    :param src: Source image
    :return: Straigtness in [0, 1]
    """

    proj = horizontal_projection(src)

    max_threshold = max(proj)
    proj = [i / max_threshold for i in proj if i != 0]

    return np.average(proj)
