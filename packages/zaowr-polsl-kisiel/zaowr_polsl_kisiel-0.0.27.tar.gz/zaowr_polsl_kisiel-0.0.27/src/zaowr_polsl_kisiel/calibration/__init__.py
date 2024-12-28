"""
The `calibration` module provides functions to perform mono and stereo camera calibration,
as well as calculate the field of view (FOV).

Functions:

- `calibrate_camera`: Performs single camera calibration using input data.

- `stereo_calibration`: Calibrates a stereo camera system for depth estimation.

- `calculate_fov`: Calculates the horizontal and vertical field of view of a camera.

Usage:
Import this module to perform calibration-related operations on camera systems.
"""

__all__ = [
    "calibrate_camera",
    "stereo_calibration",
    "calculate_fov",
]

from .calibrate_camera import calibrate_camera  # calibrate single camera
from .stereo_calibration import stereo_calibration, calculate_fov  # stereo calibration and FOV
