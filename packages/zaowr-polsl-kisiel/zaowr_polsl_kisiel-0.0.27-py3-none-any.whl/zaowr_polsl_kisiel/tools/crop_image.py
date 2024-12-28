import numpy as np

def crop_image(
        img: np.ndarray,
        cropPercentage: float = 0.75
) -> np.ndarray:
    """
    Crop the image to retain only the center part (specified by percentage).

    :param np.ndarray img: The input image to be cropped.
    :param float cropPercentage: The percentage of the image to retain (default is 75%).

    :return: Cropped image as a numpy array.
    """
    # Get the dimensions of the image
    height, width = img.shape[:2]

    # Calculate the cropping bounds
    cropHeight = int(height * cropPercentage)
    cropWidth = int(width * cropPercentage)

    # Calculate starting indices for cropping
    startX = (width - cropWidth) // 2
    startY = (height - cropHeight) // 2

    # Crop the image
    cropped = img[startY : startY + cropHeight, startX : startX + cropWidth]

    return cropped