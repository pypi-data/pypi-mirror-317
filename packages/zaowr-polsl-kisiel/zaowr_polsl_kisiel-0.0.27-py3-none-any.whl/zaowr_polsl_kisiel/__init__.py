"""
This package provides tools and utilities for camera calibration, stereo calibration,
image processing, and related operations.

Modules:

- `calibration`: Tools for camera and stereo calibration.

- `content_loaders`: Functions to load and validate calibration data from files and load the ground truth `.pgm` file or save the disparity map.

- `custom_exceptions`: Custom exceptions for error handling.

- `image_processing`: Utilities for image rectification, distortion removal and disparity map calculation and color difference map calculation.

- `tools`: Additional tools, such as ArUco dictionary identification, performance measurement or image cropping.

Status: Development

Year of development: 2024

Author: Maksymilian Kisiel

Institution: Silesian University of Technology

Faculty: Faculty of Automatic Control, Electronics and Computer Science

Major: Informatics, master degree

Specialization: Interactive Three-Dimensional Graphics (IGT, pol. Interaktywna Grafika Trójwymiarowa, https://www.polsl.pl/rau6/en/igt-specjalization/)
"""

__version__ = "0.0.27"
__status__ = "Development"  # Allowed: "Prototype", "Beta", "Stable"

__all__ = [
    "calibration",
    "content_loaders",
    "exceptions",
    "image_processing",
    "tools",
]

# IMPORT SUBMODULES
from . import calibration
from .calibration import (
    calibrate_camera, # calibrate single camera
    stereo_calibration, # stereo calibration
    calculate_fov, # calculate fov - horizontal and vertical
)

from . import custom_exceptions
from .custom_exceptions import exceptions # custom_exceptions

from . import content_loaders
from .content_loaders import (
    are_params_valid, # validate calibration parameters stored in files and return them if valid
    save_calibration, # save calibration parameters (used for all types of params - single, stereo, rectification)
    load_calibration, # load calibration parameters for single camera
    load_stereo_calibration, # load stereo calibration
    load_rectification_maps, # load rectification maps
    save_disparity_map, # save disparity map
    load_pgm_file, # load the ground truth .pgm file
)

from . import image_processing
from .image_processing import (
    remove_distortion, # remove distortion from single image
    stereo_rectify, # rectify stereo image after stereo calibration
    calculate_disparity_map, # calculate disparity map using StereoBM, StereoSGBM, Custom Block Matching
    calculate_color_difference_map, # calculate color difference map
    plot_disparity_map_comparison, # plot disparity map comparison
)

from . import tools
from .tools import (
    find_aruco_dict, # find aruco dictionary if we don't know
    measure_perf, # measure performance
    calculate_mse_disparity, # calculate MSE between two disparity maps
    calculate_ssim_disparity, # calculate SSIM between two disparity maps
    crop_image, # crop image to retain only the center part (specified by percentage)
)