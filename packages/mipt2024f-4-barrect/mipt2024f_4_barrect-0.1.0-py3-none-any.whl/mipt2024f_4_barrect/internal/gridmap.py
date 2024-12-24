import numpy as np


class GridMap:
    """
    Data class to store grid mapping between source image and destination image

    Attributes:
        src (np.ndarray): Source grid
        dest (np.ndarray): Destination grid
    """

    src: np.ndarray
    dest: np.ndarray

    def __init__(self, src: np.ndarray, dest: np.ndarray):
        """
        Direct constructor for GridMap

        :param src: Source grid
        :param dest: Destination grid
        """

        self.src = src
        self.dest = dest
