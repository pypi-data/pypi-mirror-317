"""
The `tools` module contains additional utilities for specific tasks.

Functions:

- `find_aruco_dict`: Identifies the ArUco dictionary used in marker detection.

- `measure_perf`: (custom decorator) Measures the performance (execution time) of a function (optionally saves results to a file).

- `calculate_mse_disparity`: Calculates the Mean Squared Error (MSE) between two disparity maps.

- `calculate_ssim_disparity`: Calculates the Structural Similarity Index (SSIM) between two disparity maps.

- `crop_image`: Crops an image to retain only the center part (specified by percentage).

Usage:
Use this module for miscellaneous tools that enhance functionality.
"""

__all__ = [
    "find_aruco_dict",
    "measure_perf",
    "calculate_mse_disparity",
    "calculate_ssim_disparity",
    "crop_image",
]

from .find_aruco_dict import find_aruco_dict # find aruco dictionary if we don't know it
from .measure_perf import measure_perf # measure performance (time) of a function (custom decorator with option to save the results to a file)
from .calculate_mse_disparity import calculate_mse_disparity # calculate MSE between two disparity maps
from .calculate_ssim_disparity import calculate_ssim_disparity # calculate Structural Similarity Index (SSIM) between two disparity maps
from .crop_image import crop_image # crop image to retain only the center part (specified by percentage)