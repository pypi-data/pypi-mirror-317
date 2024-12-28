from json import load as jload
from typing import Any

from .load_calibration import load_calibration
from .load_rectification_maps import load_rectification_maps
from .load_stereo_calibration import load_stereo_calibration

from colorama import Fore, Style, init as colorama_init #, Back

colorama_init(autoreset=True)

def are_params_valid(path: str) -> tuple[bool, dict[str, Any] | None]:
    """
    Detects parameter type, validates it, and returns a tuple of validation result and parameters (if valid).

    :param str path: Path to the parameter file.
    :return: (bool, dict) - Validation result and parameters if valid, otherwise None.
    """
    try:
        with open(path, 'r') as file:
            data = jload(file)

        # Detect and validate calibration parameters
        if "cameraMatrix" in data and "distortionCoefficients" in data:
            params = load_calibration(path)
            return True, params

        # Detect and validate rectification maps
        if "map1_left" in data and "map2_left" in data:
            params = load_rectification_maps(path)
            return True, params

        # Detect and validate stereo calibration parameters
        if "cameraMatrix_left" in data and "cameraMatrix_right" in data:
            params = load_stereo_calibration(path)
            return True, params

        # Unrecognized file structure
        return False, None

    except Exception as e:
        # Catch validation errors
        print(Fore.RED + f"\nValidation failed for file '{path}' with error:\n\t{e}\n" + Style.RESET_ALL)
        return False, None