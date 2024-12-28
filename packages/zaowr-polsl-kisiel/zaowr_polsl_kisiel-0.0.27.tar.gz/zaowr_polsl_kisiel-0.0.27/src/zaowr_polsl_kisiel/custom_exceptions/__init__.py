"""
The `custom_exceptions` module defines custom exceptions used throughout the package.

Exceptions:

- `CalibrationImagesNotFound`: Raised when no calibration images are found in the specified path.

- `CalibrationParamsPathNotProvided`: Raised when the calibration file path is missing or not a string.

- `StereoCalibrationParamsPathNotProvided`: Raised when the stereo calibration file path is missing or not a string.

- `CalibrationParamsWrongFormat`: Raised when the calibration file format is incorrect or fields are empty.

- `ImgToUndistortPathNotProvided`: Raised when the path for the image to undistort is missing or not a string.

- `UndistortedImgPathNotProvided`: Raised when the path for saving the undistorted image is missing or not a string.

- `RectifiedImgPathNotProvided`: Raised when the path for saving the rectified image is missing or not a string.

- `MissingParameters`: Raised when required parameters are missing from a function call.

- `RectificationMapsPathNotProvided`: Raised when the rectification maps file path is missing or not a string.

- `CharucoCalibrationError`: Raised when there is an error during ChArUco board calibration.

Usage:
These exceptions are designed to provide clear and specific error messages for
common issues encountered while using the package. They should be caught and
handled appropriately to ensure a smooth user experience.
"""

__all__ = [
    "exceptions",
]

from . import exceptions