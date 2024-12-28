import os
from json import dump as jdump
from typing import Any
from ..custom_exceptions.exceptions import CalibrationParamsPathNotProvided


def save_calibration(
    calibrationParams: dict[str, list | Any], calibrationParamsPath: str
) -> None:
    """
    Save the provided calibration parameters to specified JSON file

    :param dict[str, list] calibrationParams: Dictionary containing calibration parameters.
    :param str calibrationParamsPath: Path to the JSON file where the parameters will be saved.

    :return: None

    :raises CalibrationParamsPathNotProvided: Raises an error if the path was not provided, or it isn't an instance of a string.
    """

    if (calibrationParamsPath == "") or (not isinstance(calibrationParamsPath, str)):
        raise CalibrationParamsPathNotProvided

    # Ensure the directory exists
    directory = os.path.dirname(calibrationParamsPath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the calibration parameters
    with open(calibrationParamsPath, "w", encoding="utf-8") as file:
        jdump(calibrationParams, file, ensure_ascii=False, indent=4)
