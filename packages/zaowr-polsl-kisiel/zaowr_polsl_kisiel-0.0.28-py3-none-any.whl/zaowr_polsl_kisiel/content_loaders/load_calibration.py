from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Any

from ..custom_exceptions.exceptions import CalibrationParamsPathNotProvided, CalibrationParamsWrongFormat

from json import load as jload
from numpy import array as npArray
from numpy import ndarray as npNdArray

# To avoid creating a class at runtime, for type-hinting alone.
if TYPE_CHECKING:
    # Map the `dict` fields here
    class CalibrationParams(TypedDict):
        """
        A dictionary structure defining the parameters of camera calibration.

        Keys:
            - **mse** (float): Mean Square Error of the calibration process.

            - **rms** (float): The overall RMS re-projection error.

            - **objPoints** (np.ndarray): 3D points in the real-world coordinate space.

            - **imgPoints** (np.ndarray): 2D points in the image plane.

            - **cameraMatrix** (np.ndarray): The intrinsic camera matrix.

            - **distortionCoefficients** (np.ndarray): Radial and tangential distortion coefficients:
                - k1, k2, k3 (radial),

                - p1, p2 (tangential).

            - **rotationVectors** (list): Camera orientation per view (rotation).

            - **translationVectors** (list): Camera position per view (translation).
        """
        mse: float
        rms: float
        objPoints: npNdArray
        imgPoints: npNdArray
        cameraMatrix: npNdArray
        distortionCoefficients: npNdArray
        rotationVectors: list
        translationVectors: list

def load_calibration(calibrationParamsPath: str) -> CalibrationParams:
    """
    Load the camera calibration from specified JSON file

    :param str calibrationParamsPath: Path to the JSON calibration file

    :return: CalibrationParams dict[str, Any] - Returns calibration parameters of the camera in form of a dict:
        - **mse** (float) - Mean Square Error,
        - **rms** (float) - The overall RMS re-projection error in floating number format,
        - **objPoints** (np.ndarray) - 3D point in real world space,
        - **imgPoints** (np.ndarray) - 2D points in image plane,
        - **cameraMatrix** (np.ndarray) - Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters,
        - **distortionCoefficients** (np.ndarray) - Distortion Coefficients: (k<sub>1</sub>, k<sub>2</sub>, p<sub>1</sub>, p<sub>2</sub>, k<sub>3</sub>), which include radial (k<sub>n</sub>) and tangential (p<sub>n</sub>) distortion values,
        - **rotationVectors** (list) - Rotation Vector, the image pixel rotation angles in radians converted to vector by Rodrigues method,
        - **translationVectors** (list) - Translation Vector, the vector depicting shift in pixel values along x and y axis.

    :raises CalibrationParamsPathNotProvided: Raises an error if the path was not provided or it isn't an instance of a string.
    :raises CalibrationParamsWrongFormat: Raises an error if the calibration file is not in the correct format or parameters are empty.
    """

    # Check if the provided path is valid
    if (calibrationParamsPath == "") or (not isinstance(calibrationParamsPath, str)):
        raise CalibrationParamsPathNotProvided

    with open(calibrationParamsPath, "r") as f:
        jsonDump = jload(f)

    try:
        mse = jsonDump["mse"]
        rms = jsonDump["rms"]
        objPoints = npArray(jsonDump["objPoints"])
        imgPoints = npArray(jsonDump["imgPoints"])
        cameraMatrix = npArray(jsonDump["cameraMatrix"])
        distortionCoefficients = npArray(jsonDump["distortionCoefficients"])
        rotationVectors = jsonDump["rotationVectors"]
        translationVectors = jsonDump["translationVectors"]


        if not isinstance(mse, float):
            raise CalibrationParamsWrongFormat

        if not isinstance(rms, float):
            raise CalibrationParamsWrongFormat

        # Rise if the size of the list is 0
        # arr = [] -> (not arr) -> True
        if (not objPoints.size) or (not isinstance(objPoints, list | npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not imgPoints.size) or (not isinstance(imgPoints, list | npNdArray)):
            raise CalibrationParamsWrongFormat

        # Rise if the size of the array is 0
        # arr = npArray([]) -> (not arr.size) -> True
        if (not cameraMatrix.size) or (not isinstance(cameraMatrix, npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not distortionCoefficients.size) or (not isinstance(distortionCoefficients, npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not rotationVectors) or (not isinstance(rotationVectors, list)):
            raise CalibrationParamsWrongFormat

        if (not translationVectors) or (not isinstance(translationVectors, list)):
            raise CalibrationParamsWrongFormat

        return {
            "mse": mse,
            "rms": rms,
            "objPoints": objPoints,
            "imgPoints": imgPoints,
            "cameraMatrix": cameraMatrix,
            "distortionCoefficients": distortionCoefficients,
            "rotationVectors": rotationVectors,
            "translationVectors": translationVectors,
        }

    except KeyError as e:
        raise CalibrationParamsWrongFormat(f"Missing key in JSON data: {e}")
