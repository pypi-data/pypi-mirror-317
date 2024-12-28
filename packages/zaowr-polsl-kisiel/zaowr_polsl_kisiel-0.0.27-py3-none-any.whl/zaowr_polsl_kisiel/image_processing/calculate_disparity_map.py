import os
from sys import stdout

import cv2 as cv
import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back
from tqdm import tqdm  # progress bar
import matplotlib.pyplot as plt # for plotting

colorama_init(autoreset=True)

def calculate_disparity_map(
    leftImagePath: str,
    rightImagePath: str,
    blockSize: int = 9, # for StereoBM, StereoSGBM & Custom 2
    numDisparities: int = 16, # for StereoBM & StereoSGBM
    minDisparity: int = 0, # for StereoSGBM
    maxDisparity: int = 64, # for Custom 1 & Custom 2
    windowSize: tuple[int, int] = (11, 11), # for Custom 1
    disparityCalculationMethod: str = "bm",
    saveDisparityMap: bool = False,
    saveDisparityMapPath: str = None,
    showDisparityMap: bool = False
) -> np.ndarray:
    """
    Calculate the disparity map using **StereoBM**, **StereoSGBM** or **custom block matching using SSD** as the matching criterion (left to right).

    :param str leftImagePath: Path to the left stereo image (should already be rectified).
    :param str rightImagePath: Path to the right stereo image (should already be rectified).
    :param int blockSize: (**Used by StereoBM, StereoSGBM & Custom Block Matching 2**) Block size to use for block matching. Must be:
        - **an odd number >= 5 for StereoBM**,
        - **an odd number >= 3 for StereoSGBM**,
    :param int numDisparities: (**Used by StereoBM & StereoSGBM**) Maximum disparity range (must be divisible by 16).

    :param int minDisparity: (**Used by StereoSGBM**) Minimum disparity (typically 0 or a small positive value).
    :param int maxDisparity: (**Used by Custom Block Matching 1 & 2**) Maximum disparity range to search.
    :param tuple[int, int] windowSize: (**Used by Custom Block Matching 1**) Tuple specifying the (height, width) of the matching window.

    :param str disparityCalculationMethod: Method to use for disparity calculation provided as a string (bm, sgbm, custom, custom2; custom2 is **NOT** recommended).:
        - **bm**: Use **StereoBM** for disparity calculation,
        - **sgbm**: Use **StereoSGBM** for disparity calculation,
        - **custom**: Use **Custom Block Matching** for disparity calculation,
        - **custom2**: Use **Custom Block Matching 2** for disparity calculation.

    :param bool saveDisparityMap: Whether to save the disparity map.
    :param str saveDisparityMapPath: Path to save the disparity map.
    :param bool showDisparityMap: Whether to show the disparity map.

    :raises ValueError: Raises an error if the provided parameters are invalid.
    :raises FileNotFoundError: Raises an error if one or both input images could not be loaded.
    :raises IOError: Raises an error if the images could not be read.
    :raises RuntimeError: Raises an error if the disparity calculation fails.

    :return: **Disparity map** as a normalized numpy array of type uint8.
    """
    if (
        not os.path.exists(leftImagePath)
        or not os.path.exists(rightImagePath)
        or leftImagePath == ""
        or rightImagePath == ""
    ):
        raise FileNotFoundError(Fore.RED + f"\nOne or both input images could not be loaded:\n"
                                    f"\t{leftImagePath}\n"
                                    f"\t{rightImagePath}\n"
                        )

    if leftImagePath == rightImagePath:
        raise ValueError(Fore.RED + "\nLeft and right images must be different:\n"
                                    f"\t{leftImagePath}\n"
                                    f"\t{rightImagePath}\n"
                         )

    # Validate block size, disparity range and disparity calculation method
    if (blockSize % 2 == 0
        or (blockSize < 5 and disparityCalculationMethod == "bm")
        or (blockSize < 3 and disparityCalculationMethod == "sgbm")
        or (blockSize < 5 and disparityCalculationMethod == "custom2")
    ):
        raise ValueError(Fore.RED + "\nBlock size must be an odd number"
                                    " >= 5 for StereoBM,"
                                    " and >= 3 for StereoSGBM.\n"
                         )

    if numDisparities % 16 != 0:
        raise ValueError(Fore.RED + f"\nDisparity range must be divisible by 16. ({numDisparities} is not divisible)\n")

    if disparityCalculationMethod not in ["bm", "sgbm", "custom", "custom2"]:
        raise ValueError(Fore.RED + f"\nInvalid disparity calculation method ({disparityCalculationMethod}). Supported methods:\n\t- bm,\n\t- sgbm,\n\t- custom,\n\t- custom2.\n")

    # Load the stereo images as grayscale
    base_left = os.path.basename(leftImagePath)
    base_right = os.path.basename(rightImagePath)
    print(Fore.GREEN + f"Loading images {base_left} and {base_right}...")

    img_left = None
    img_right = None
    img_left = cv.imread(leftImagePath, cv.IMREAD_GRAYSCALE)
    img_right = cv.imread(rightImagePath, cv.IMREAD_GRAYSCALE)

    if img_left is None or img_right is None:
        raise IOError(Fore.RED + "\nOne or both input images could not be loaded:\n"
                                f"\t{leftImagePath}\n"
                                f"\t{rightImagePath}\n"
                     )

    disparityMap = None
    calculationMethod = None
    if disparityCalculationMethod == "bm":
        calculationMethod = "StereoBM"
        print(Fore.GREEN + f"Computing disparity map using '{calculationMethod}'...")

        # Create StereoBM object
        stereoBM = cv.StereoBM.create(numDisparities=numDisparities, blockSize=blockSize)

        # Compute disparity map
        disparityMap = stereoBM.compute(img_left, img_right)

    elif disparityCalculationMethod == "sgbm":
        calculationMethod = "StereoSGBM"
        print(Fore.GREEN + f"Computing disparity map using '{calculationMethod}'...")

        # Create StereoSGBM object with initial/default parameters
        stereoSGBM = cv.StereoSGBM.create(
            minDisparity=minDisparity,
            numDisparities=numDisparities,
            blockSize=blockSize,
            P1=(8 * 3 * blockSize ** 2),  # Penalty on the disparity change (smoothing constraint)
            P2=(32 * 3 * blockSize ** 2),  # Stronger penalty for larger changes in disparity
            disp12MaxDiff=2,  # Maximum allowed disparity difference between left and right checks
            preFilterCap=63,  # Truncation value for prefiltered image pixels
            uniquenessRatio=15,  # Margin by which the best (minimum) computed cost function value
            # should "win" over the next best
            speckleWindowSize=100,  # Maximum size of smooth disparity regions to consider noise
            speckleRange=1,  # Maximum disparity variation within smooth disparity regions
        )

        # Compute the disparity map
        disparityMap = stereoSGBM.compute(img_left, img_right)

    elif disparityCalculationMethod == "custom": # SSD
        calculationMethod = "Custom Method (SSD, left to right)"
        print(Fore.GREEN + f"Computing disparity map using '{calculationMethod}'...")

        windowHeight, windowWidth = windowSize
        height, width = img_left.shape
        halfWindowHeight = windowHeight // 2
        halfWindowWidth = windowWidth // 2

        # Initialize the disparity map
        disparityMap = np.zeros((height, width), dtype=np.float32)

        for dy in tqdm(
                range(halfWindowHeight, height - halfWindowHeight),
                desc=Style.RESET_ALL + "Searching for the best SSD match...",
                dynamic_ncols=True,
                bar_format="{l_bar}{bar}{r_bar}",
                colour="green",
                file=stdout
        ):
            # tqdm.write(
            #     Fore.GREEN
            #     + f"Processing disparity map at pixel line {dy} (height: {height})...",
            #     nolock=True,
            #     file=stdout,
            # )
            for dx in range(halfWindowWidth, width - halfWindowWidth):
                # Extract block from the right image
                template = img_right[
                           dy - halfWindowHeight : dy + halfWindowHeight + 1,
                           dx - halfWindowWidth : dx + halfWindowWidth + 1,
                           ]

                # Initialize the best SSD and disparity
                minSsd = float('inf')
                bestDisparity = 0

                # Search over the disparity range
                for offset in range(min(maxDisparity, width - dx - halfWindowWidth)):
                    # Extract block from the left image
                    roi = img_left[
                          dy - halfWindowHeight : dy + halfWindowHeight + 1,
                          dx - halfWindowWidth + offset : dx + halfWindowWidth + offset + 1,
                          ]

                    # Compute SSD
                    ssd = np.sum((template - roi) ** 2)

                    # Update the best match
                    if ssd < minSsd:
                        minSsd = ssd
                        bestDisparity = offset
                        tqdm.write(
                            Fore.GREEN
                            + f"Found new best SSD match at disparity {bestDisparity} (SSD: {minSsd})...",
                            nolock=True,
                            file=stdout,
                        )

                # Store the best disparity
                disparityMap[dy, dx] = bestDisparity

    elif disparityCalculationMethod == "custom2":
        calculationMethod = "Custom Method 2 (SSD, stereo block matching)"
        print(Fore.GREEN + f"Computing disparity map using '{calculationMethod}'...")

        # Initialize disparity map
        height, width = img_left.shape
        disparityMap = np.zeros((height, width), dtype=np.float32)

        halfBlock = blockSize // 2

        # Pad images to handle borders
        padded_left = cv.copyMakeBorder(img_left, halfBlock, halfBlock, halfBlock, halfBlock, cv.BORDER_CONSTANT, value=0)
        padded_right = cv.copyMakeBorder(img_right, halfBlock, halfBlock, halfBlock, halfBlock, cv.BORDER_CONSTANT, value=0)

        # Compute disparity map

        for y in tqdm(
            range(halfBlock, height + halfBlock),
            desc=Style.RESET_ALL + "Searching for the best SSD match...",
            dynamic_ncols=True,
            bar_format="{l_bar}{bar}{r_bar}",
            colour="green",
            file=stdout
        ):
            # tqdm.write(
            #     Fore.GREEN
            #     + f"Processing disparity map at pixel line {y} (height: {height})...",
            #     nolock=True,
            #     file=stdout,
            # )
            for x in range(halfBlock, width + halfBlock):
                # Extract block from left image
                block_left = padded_left[y - halfBlock:y + halfBlock + 1, x - halfBlock:x + halfBlock + 1]

                minSsd = float('inf')
                bestDisparity = 0

                # Search for best match in disparity range
                for d in range(maxDisparity):
                    x_shifted = x - d
                    if x_shifted - halfBlock < 0:
                        continue

                    # Extract block from right image
                    right_block = padded_right[y - halfBlock:y + halfBlock + 1,
                                  x_shifted - halfBlock:x_shifted + halfBlock + 1]

                    # Compute SSD
                    ssd = np.sum((block_left - right_block) ** 2)

                    # Update best match
                    if ssd < minSsd:
                        minSsd = ssd
                        bestDisparity = d
                        tqdm.write(
                            Fore.GREEN
                            + f"Found new best SSD match at disparity {bestDisparity} (SSD: {minSsd})...",
                            nolock=True,
                            file=stdout,
                        )

                # Store best disparity
                disparityMap[y - halfBlock, x - halfBlock] = bestDisparity


    if disparityMap is None:
        raise RuntimeError(Fore.RED + "\nDisparity map calculation failed!\n")

    # Normalize the disparity map for visualization
    disparityMap = cv.normalize(disparityMap, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    disparityMap = np.uint8(disparityMap)  # Convert to 8-bit unsigned integer

    print(Fore.GREEN + f"Disparity map successfully calculated using '{calculationMethod}'")

    if showDisparityMap and not saveDisparityMap:
        cv.imshow(f"Disparity Map '{calculationMethod}'", disparityMap)
        cv.waitKey(0)
        cv.destroyAllWindows()

    if saveDisparityMap:
        if saveDisparityMapPath is None or not isinstance(saveDisparityMapPath, str) or len(saveDisparityMapPath) == 0:
            raise ValueError(Fore.RED + "\n`saveDisparityMapPath` must be a non-empty string!\n")

        try:
            from ..content_loaders import save_disparity_map

            save_disparity_map(disparityMap, saveDisparityMapPath, showDisparityMap)

        except ValueError:
            raise

        except TypeError:
            raise

        except Exception as e:
            raise ValueError(Fore.RED + f"\nUnknown error occurred while saving disparity map: {e}\n")

    return disparityMap


def plot_disparity_map_comparison(
    disparityMapBM: np.ndarray,
    disparityMapSGBM: np.ndarray,
    disparityMapCustom: np.ndarray,
    groundTruth: np.ndarray,
    colorDiffMapBM: np.ndarray = None,
    colorDiffMapSGBM: np.ndarray = None,
    colorDiffMapCustom: np.ndarray = None,
    showComparison: bool = False,
    saveComparison: bool = False,
    savePath: str = None
) -> None:
    """
    Plot the disparity map comparison. Requires disparity maps calculated using BM, SGBM, and custom block matching. Optionally, color difference maps can be provided.

    :param np.ndarray disparityMapBM: Disparity map calculated using BM.
    :param np.ndarray disparityMapSGBM: Disparity map calculated using SGBM.
    :param np.ndarray disparityMapCustom: Disparity map calculated using custom block matching.
    :param np.ndarray groundTruth: The ground truth disparity map.
    :param np.ndarray colorDiffMapBM: Color difference map for the disparity map calculated using BM.
    :param np.ndarray colorDiffMapSGBM: Color difference map for the disparity map calculated using SGBM.
    :param np.ndarray colorDiffMapCustom: Color difference map for the disparity map calculated using custom block matching.
    :param bool showComparison: Whether to show the comparison plot.
    :param bool saveComparison: Whether to save the comparison plot.
    :param str savePath: Path to save the comparison plot.

    :raises ValueError: Raises ValueError if `savePath` is not provided when `saveComparison` is True.

    :return: None
    """
    plt.figure(figsize=(20, 10))

    if (
            colorDiffMapBM is not None
            and colorDiffMapSGBM is not None
            and colorDiffMapCustom is not None
    ):
        colorMaps = True
        plotSize = (2, 4)
    else:
        colorMaps = False
        plotSize = (2, 2)

    plt.subplot(plotSize[0], plotSize[1], 1)
    plt.imshow(disparityMapBM, cmap='gray')
    plt.title('Disparity Map using StereoBM')
    plt.axis('off')

    plt.subplot(plotSize[0], plotSize[1], 2)
    plt.imshow(disparityMapSGBM, cmap='gray')
    plt.title('Disparity Map using StereoSGBM')
    plt.axis('off')

    plt.subplot(plotSize[0], plotSize[1], 3)
    plt.imshow(disparityMapCustom, cmap='gray')
    plt.title('Disparity Map using Custom Block Matching')
    plt.axis('off')

    plt.subplot(plotSize[0], plotSize[1], 4)
    plt.imshow(groundTruth, cmap='gray')
    plt.title('Ground Truth Disparity Map')
    plt.axis('off')

    if colorMaps:
        plt.subplot(plotSize[0], plotSize[1], 5)
        plt.imshow(colorDiffMapBM, cmap='gray')
        plt.title('Color Difference Map (StereoBM vs Ground Truth)')
        plt.axis('off')

        plt.subplot(plotSize[0], plotSize[1], 6)
        plt.imshow(colorDiffMapSGBM, cmap='gray')
        plt.title('Color Difference Map (StereoSGBM vs Ground Truth)')
        plt.axis('off')

        plt.subplot(plotSize[0], plotSize[1], 7)
        plt.imshow(colorDiffMapCustom, cmap='gray')
        plt.title('Color Difference Map (Custom vs Ground Truth)')
        plt.axis('off')

    plt.tight_layout()

    if saveComparison:
        if savePath is None:
            raise ValueError(Fore.RED + "\n`savePath` must be provided if `saveComparison` is set to True\n")

        plt.savefig(savePath, format='png', bbox_inches='tight')
        print(Fore.GREEN + f"Plot successfully saved at {savePath}")

    if showComparison:
        plt.show()

    plt.close()