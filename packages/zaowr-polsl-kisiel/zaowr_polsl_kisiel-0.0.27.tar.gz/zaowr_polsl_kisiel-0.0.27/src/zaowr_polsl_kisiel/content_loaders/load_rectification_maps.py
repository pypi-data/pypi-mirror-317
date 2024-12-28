from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Any

from ..custom_exceptions.exceptions import RectificationMapsPathNotProvided, CalibrationParamsWrongFormat

from json import load as jload
from numpy import array as npArray
from numpy import ndarray as npNdArray

# To avoid creating a class at runtime, for type-hinting alone.
if TYPE_CHECKING:
    # Map the `dict` fields here
    class RectificationMaps(TypedDict):
        """
        A dictionary structure defining the rectification maps for stereo image rectification.

        Keys:
            - **map1_left** (np.ndarray): The first rectification map for the left camera.

            - **map2_left** (np.ndarray): The second rectification map for the left camera.

            - **map1_right** (np.ndarray): The first rectification map for the right camera.

            - **map2_right** (np.ndarray): The second rectification map for the right camera.
        """
        map1_left: npNdArray
        map2_left: npNdArray
        map1_right: npNdArray
        map2_right: npNdArray


def load_rectification_maps(rectificationMapsPath: str) -> RectificationMaps:
    """
    Load rectification maps for stereo camera rectification from a specified JSON file.

    :param str rectificationMapsPath: Path to the JSON file containing rectification maps.
    :return: Returns a dictionary containing the rectification maps:
        - **map1_left** (np.ndarray) - First rectification map for the left camera.
        - **map2_left** (np.ndarray) - Second rectification map for the left camera.
        - **map1_right** (np.ndarray) - First rectification map for the right camera.
        - **map2_right** (np.ndarray) - Second rectification map for the right camera.

    :raises RectificationMapsPathNotProvided: If the path is missing or not a string.
    :raises CalibrationParamsWrongFormat: If the file does not contain the correct format or parameters.
    """

    # Check if the provided path is valid
    if not rectificationMapsPath or not isinstance(rectificationMapsPath, str):
        raise RectificationMapsPathNotProvided("Path must be a non-empty string.")

    with open(rectificationMapsPath, "r") as file:
        jsonDump = jload(file)

    try:
        # Load rectification maps from the JSON
        map1_left = npArray(jsonDump["map1_left"])
        map2_left = npArray(jsonDump["map2_left"])
        map1_right = npArray(jsonDump["map1_right"])
        map2_right = npArray(jsonDump["map2_right"])

        # Validate each map
        if (not map1_left.size) or (not isinstance(map1_left, npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not map2_left.size) or (not isinstance(map2_left, npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not map1_right.size) or (not isinstance(map1_right, npNdArray)):
            raise CalibrationParamsWrongFormat

        if (not map2_right.size) or (not isinstance(map2_right, npNdArray)):
            raise CalibrationParamsWrongFormat

        # Return validated rectification maps
        return {
            "map1_left": map1_left,
            "map2_left": map2_left,
            "map1_right": map1_right,
            "map2_right": map2_right,
        }

    except KeyError as e:
        raise CalibrationParamsWrongFormat(f"Missing key in JSON data: {e}")