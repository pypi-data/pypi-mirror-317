import cv2
import numpy as np
from scipy.interpolate import griddata


def warp_perspective(
        img_src: np.ndarray,
        point_src: np.ndarray,
        point_dest: np.ndarray,
        width: int,
        height: int
) -> np.ndarray:
    """
    Performs opencv builtin perspective transformation on image

    :param img_src: Source image
    :param point_src: Source vertices
    :param point_dest: Dest vertices
    :param width: Out image width
    :param height: Out image height

    :return: Warped image
    """

    matrix = cv2.getPerspectiveTransform(point_src, point_dest)
    return cv2.warpPerspective(img_src, matrix, (width, height))


def warp_by_grid(
        img_src: np.ndarray,
        src_grid: np.ndarray,
        dest_grid: np.ndarray,
        width: int,
        height: int
):
    """
    Performs warp transformation induced by pair of grids. Uses cubic interpolation

    :param img_src: Source image
    :param src_grid: Source grid
    :param dest_grid: Destination grid
    :param width: Out image width
    :param height: Out image height

    :return: Warped image
    """

    grid_x, grid_y = np.mgrid[0:width - 1:width * 1j, 0:height - 1:height * 1j]

    grid_z = griddata(dest_grid, src_grid, (grid_x, grid_y), method='cubic')
    map_x = np.append([], [ar[:, 0] for ar in grid_z]).reshape(width, height)
    map_y = np.append([], [ar[:, 1] for ar in grid_z]).reshape(width, height)
    map_x_32 = map_x.astype('float32')
    map_y_32 = map_y.astype('float32')

    return cv2.transpose(cv2.remap(img_src, map_x_32, map_y_32, cv2.INTER_CUBIC))
