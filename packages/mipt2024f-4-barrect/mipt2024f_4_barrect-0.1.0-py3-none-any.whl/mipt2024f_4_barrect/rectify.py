import numpy as np
from .internal.gridgen import rect_grid
from .internal.gridgen import bent_corner_grid
from .internal.gridmap import GridMap
from .internal.warp import warp_by_grid
from .internal.warp import warp_perspective


def calc_base_dim(
        border: np.ndarray
) -> int:
    """
    Calculation of base dimension for aspect ratio. Uses bounding box

    :param border: Barcode contour
    :return: Base dimension
    """

    x = border[:, 0]
    y = border[:, 1]

    return (x.max() - x.min() + y.max() - y.min()) // 2


def rectify_perspective_cv(
        img_src: np.ndarray,
        border: np.ndarray,
        dim_x: int = None,
        dim_y: int = None,
        x_ratio: int = 1,
        y_ratio: int = 1
) -> np.ndarray:
    """
    External API for perspective transformation using OpenCV builtins

    :param img_src: Source image
    :param border: Barcode contour
    :param dim_x: Strict definition of result image width
    :param dim_y: Strict definition of result image height
    :param x_ratio: x if aspect ratio is x/y
    :param y_ratio: y if aspect ratio is x/y
    :return: Rectified barcode
    """

    if dim_x is None and dim_y is None:
        dim = calc_base_dim(border)
        dim_x = dim
        dim_y = dim * y_ratio // x_ratio

    gridmap = rect_grid(border, dim_x, dim_y)

    return warp_perspective(img_src, border, gridmap.dest, dim_x, dim_y)


def rectify_perspective(
        img_src: np.ndarray,
        border: np.ndarray,
        dim_x: int = None,
        dim_y: int = None,
        x_ratio: int = 1,
        y_ratio: int = 1
) -> (np.ndarray, GridMap):
    """
    External API for perspective transformation using warp by grid with interpolation

    :param img_src: Source image
    :param border: Barcode contour
    :param dim_x: Strict definition of result image width
    :param dim_y: Strict definition of result image height
    :param x_ratio: x if aspect ratio is x/y
    :param y_ratio: y if aspect ratio is x/y
    :return: Rectified barcode and grid map
    """

    if dim_x is None and dim_y is None:
        dim = calc_base_dim(border)
        dim_x = dim
        dim_y = dim * y_ratio // x_ratio

    gridmap = rect_grid(border, dim_x, dim_y)

    return warp_by_grid(img_src, gridmap.src, gridmap.dest, dim_x, dim_y), gridmap


def rectify_bent_corner(
        img_src: np.ndarray,
        border: np.ndarray,
        corner_idx: int,
        dim_x: int = None,
        dim_y: int = None,
        x_ratio: int = 1,
        y_ratio: int = 1
) -> (np.ndarray, GridMap):
    """
    External API for fixing bent corner

    :param img_src: Source image
    :param border: Barcode contour
    :param corner_idx: Index of vertex of bent corner
    :param dim_x: Strict definition of result image width
    :param dim_y: Strict definition of result image height
    :param x_ratio: x if aspect ratio is x/y
    :param y_ratio: y if aspect ratio is x/y
    :return: Rectified barcode and grid map
    """

    if dim_x is None and dim_y is None:
        dim = calc_base_dim(border)
        dim_x = dim
        dim_y = dim * y_ratio // x_ratio

    gridmap = bent_corner_grid(border, corner_idx, dim_x, dim_y)

    return warp_by_grid(img_src, gridmap.src, gridmap.dest, dim_x, dim_y), gridmap
