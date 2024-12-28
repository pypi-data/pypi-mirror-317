"""
The `content_loaders` module handles loading, saving, and validating calibration
and rectification data as well as loading the ground truth (or any other) `.pgm` file.

Functions:

- `are_params_valid`: Validates calibration parameters stored in files and returns them if valid.

- `save_calibration`: Saves calibration parameters (single, stereo, or rectification).

- `load_calibration`: Loads single
-camera calibration parameters from a file.

- `load_stereo_calibration`: Loads stereo camera calibration data from a file.

- `load_rectification_maps`: Loads stereo rectification maps from a file.

- `save_disparity_map`: Saves a disparity map to a file.

- `load_pgm_file`: Loads the ground truth (or any other) `.pgm` file.

Usage:
Use this module to manage calibration and rectification data efficiently and safely. Also, load the ground truth `.pgm` file for comparisons and save the calculated disparity map.
"""

__all__ = [
    "are_params_valid",
    "save_calibration",
    "load_calibration",
    "load_stereo_calibration",
    "load_rectification_maps",
    "save_disparity_map",
    "load_pgm_file",
]

from .are_params_valid import are_params_valid # validate calibration parameters stored in files and return them if valid
from .save_calibration import save_calibration # save calibration parameters (used for all types of params - single, stereo, rectification)
from .load_calibration import load_calibration # load calibration parameters for single camera
from .load_stereo_calibration import load_stereo_calibration # load stereo calibration
from .load_rectification_maps import load_rectification_maps # load rectification maps
from .save_disparity_map import save_disparity_map # save disparity map
from .load_pgm_file import load_pgm_file # load the ground truth `.pgm` file
