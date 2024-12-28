"""
The `image_processing` module provides utilities for processing images
after camera calibration.

Functions:

- `remove_distortion`: Removes distortion from a single image using calibration parameters.

- `stereo_rectify`: Rectifies a stereo image pair after stereo calibration.

- `calculate_disparity_map`: Calculates a disparity map using different algorithms.

- `calculate_color_difference_map`: Calculates a color difference map between two images (calculated disparity map and ground truth disparity map).

- `plot_disparity_map_comparison`: Plots a comparison of disparity maps.

Usage:
Import this module for image distortion correction, stereo rectification, disparity map calculation (you can also save the disparity map and plot the comparison of different disparity maps) and color difference map calculation.
"""

__all__ = [
    "remove_distortion",
    "stereo_rectify",
    "calculate_disparity_map",
    "calculate_color_difference_map",
    "plot_disparity_map_comparison",
]

from .remove_distortion import remove_distortion # remove distortion from single image
from .stereo_rectify import stereo_rectify # rectify stereo image after stereo calibration
from .calculate_disparity_map import calculate_disparity_map, plot_disparity_map_comparison # calculate disparity map using StereoBM, StereoSGBM, and custom block matching; plot disparity map comparison
from .calculate_color_difference_map import calculate_color_difference_map # calculate color difference map