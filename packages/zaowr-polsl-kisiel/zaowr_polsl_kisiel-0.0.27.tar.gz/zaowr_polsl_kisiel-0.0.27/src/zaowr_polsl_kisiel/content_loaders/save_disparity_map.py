import os
import cv2 as cv
import numpy as np
from colorama import Fore, init as colorama_init

colorama_init(autoreset=True)

def save_disparity_map(
    disparityMap: np.ndarray,
    savePath: str,
    show: bool = False,
) -> None:
    """
    Save a disparity map to a specified location and optionally display it.

    :param np.ndarray disparityMap: The disparity map to save.
    :param str savePath: The file path where the disparity map will be saved.
    :param bool show: If True, displays the disparity map in a window.

    :raises TypeError: Raises TypeError if `disparityMap` is not a numpy array.
    :raises ValueError: Raises ValueError if `savePath` is not provided.

    :return: None
    """
    if not isinstance(disparityMap, np.ndarray):
        raise TypeError(Fore.RED + "\nDisparity map must be a numpy array!\n")

    if savePath is None or not isinstance(savePath, str) or len(savePath) == 0:
        raise ValueError(Fore.RED + "\n`savePath` must be a non-empty string!\n")

    # Create the parent directory if it does not exist
    saveDir = os.path.dirname(savePath)
    baseName = os.path.basename(savePath)
    if saveDir and not os.path.exists(saveDir):
        os.makedirs(saveDir)
        print(Fore.BLUE + f"Directory '{saveDir}' created.")

    # Save the disparity map to the specified path
    cv.imwrite(savePath, disparityMap)
    print(Fore.GREEN + f"Disparity map '{baseName}' successfully saved at '{savePath}'")

    # Optionally display the disparity map
    if show:
        cv.imshow('Disparity Map', disparityMap)
        cv.waitKey(0)
        cv.destroyAllWindows()