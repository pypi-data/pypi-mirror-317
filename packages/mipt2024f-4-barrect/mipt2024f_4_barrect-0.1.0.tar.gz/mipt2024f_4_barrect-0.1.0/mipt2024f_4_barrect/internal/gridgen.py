import cv2
import numpy as np
from .gridmap import GridMap


def rect_grid(border: np.ndarray, dest_width: int, dest_height: int) -> GridMap:
    """
    Creates GridMap for perspective transformation

    :param border: Input border
    :param dest_width: Destination width
    :param dest_height: Destination height
    :return: GridMap
    """

    dest_grid = np.int32(
        [
            [0, dest_height],
            [dest_width, dest_height],
            [dest_width, 0],
            [0, 0]
        ]
    )

    return GridMap(border, dest_grid)


NUM_COLS = 10
NUM_ROWS = 10


def bent_corner_grid(
        border: np.ndarray,
        corner_idx: int,
        dest_width: int,
        dest_height: int
) -> GridMap:
    """
    Creates GridMap for bent corner fix

    :param border: Input border
    :param corner_idx: Index of bent corner in border
    :param dest_width: Destination width
    :param dest_height: Destination height
    :return: GridMap
    """

    dest_grid = [
        [0, dest_height],
        [dest_width, dest_height],
        [dest_width, 0],
        [0, 0]
    ]

    prev_vect = border[(corner_idx + 4) % 6] - border[(corner_idx + 5) % 6]
    next_vect = border[(corner_idx + 1) % 6] - border[(corner_idx + 2) % 6]

    prev_opposite = border[(corner_idx + 2) % 6] - border[(corner_idx + 3) % 6]
    next_opposite = border[(corner_idx + 3) % 6] - border[(corner_idx + 4) % 6]

    if corner_idx == 0:
        corner_real_idx = 0
    else:
        corner_real_idx = corner_idx - 1

    real = dest_grid[corner_real_idx]
    prev_vect_real = np.int32(dest_grid[(corner_real_idx + 3) % 4]) - np.int32(dest_grid[corner_real_idx])
    next_vect_real = np.int32(dest_grid[(corner_real_idx + 1) % 4]) - np.int32(dest_grid[corner_real_idx])

    prev_dest = real + prev_vect_real * (1 - cv2.norm(prev_vect) / cv2.norm(prev_opposite))
    next_dest = real + next_vect_real * (1 - cv2.norm(next_vect) / cv2.norm(next_opposite))

    if corner_real_idx == 0:
        dest_grid.insert(4, prev_dest)
        dest_grid.insert(1, next_dest)
    else:
        dest_grid.insert(corner_real_idx, prev_dest)
        dest_grid.insert(corner_real_idx + 2, next_dest)

    border_concat = np.concatenate(
        (border, np.int32([(border[(corner_idx + 5) % 6] + border[corner_idx] + border[(corner_idx + 1) % 6]) // 3])))
    dest_grid.append((np.int32(dest_grid[corner_real_idx]) + np.int32(dest_grid[(corner_real_idx + 1) % 6]) + np.int32(
        dest_grid[(corner_real_idx + 2) % 6])) // 3)

    return GridMap(border_concat, np.int32(dest_grid))
