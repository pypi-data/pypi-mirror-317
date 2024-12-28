import numpy as np

def calculate_mse_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float:
    """
    Calculate the Mean Squared Error between two disparity maps.

    :param np.ndarray map1: First disparity map.
    :param np.ndarray map2: Second disparity map.

    :return: **Mean Squared Error** between the two disparity maps.
    """
    return float(np.mean((map1 - map2) ** 2))