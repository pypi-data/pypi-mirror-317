import numpy as np
from skimage.metrics import structural_similarity as ssim # for structural_similarity comparison

def calculate_ssim_disparity(
        map1: np.ndarray,
        map2: np.ndarray
) -> float:
    """
    Calculate the Structural Similarity Index (SSIM) between two disparity maps.

    :param np.ndarray map1: First disparity map.
    :param np.ndarray map2: Second disparity map.

    :return: **Structural Similarity Index** between the two disparity maps.
    """
    return ssim(map1, map2)