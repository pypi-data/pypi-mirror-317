import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def calculate_color_difference_map(
        disparityMap: np.ndarray,
        groundTruth: np.ndarray
) -> np.ndarray:
    """
    Calculate the color difference map between the disparity map and "ground truth" image.

    :param np.ndarray disparityMap: Calculated disparity map.
    :param np.ndarray groundTruth: The ground truth disparity map.

    :return: **Color difference map** as a normalized numpy array of 8-bit unsigned integers.
    """
    # Calculate the absolute difference between the disparity map and ground truth
    diff = np.abs(groundTruth - disparityMap)

    # Normalize the difference for visualization
    normalizedDiff = cv.normalize(diff, None, 0, 255, cv.NORM_MINMAX)
    colorDiffMap = np.uint8(normalizedDiff)

    print(Fore.GREEN + "Color difference map successfully calculated")

    return colorDiffMap