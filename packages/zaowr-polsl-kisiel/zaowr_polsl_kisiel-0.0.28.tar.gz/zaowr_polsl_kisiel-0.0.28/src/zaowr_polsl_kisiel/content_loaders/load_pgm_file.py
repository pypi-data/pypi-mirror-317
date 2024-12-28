import cv2 as cv
import numpy as np
import os
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def load_pgm_file(
        pgmPath: str,
        targetShape: tuple[int, int]
) -> np.ndarray:
    """
    Load the **".pgm"** file and resize it to match the target shape of the disparity map.

    :param str pgmPath: Path to the ground truth `.pgm` file.
    :param tuple[int, int] targetShape: Target shape to resize the ground truth image.

    :raises FileNotFoundError: If the ground truth `.pgm` file is not found.

    :return: Resized **ground truth disparity map** as a numpy array.
    """
    print(Fore.GREEN + f"Loading ground truth disparity map from '{pgmPath}'...")

    if not os.path.exists(pgmPath):
        raise FileNotFoundError(Fore.RED + f"File '{pgmPath}' not found!")

    # Read the .pgm file and resize to match the disparity map shape (if necessary)
    groundTruth = cv.resize(cv.imread(pgmPath, cv.IMREAD_GRAYSCALE), (targetShape[1], targetShape[0]))

    return groundTruth