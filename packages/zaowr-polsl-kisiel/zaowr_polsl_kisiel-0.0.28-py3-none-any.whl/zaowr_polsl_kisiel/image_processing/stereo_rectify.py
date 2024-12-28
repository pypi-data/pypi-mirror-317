import glob
import os
from sys import stdout
from time import perf_counter

import cv2 as cv
import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back
from tqdm import tqdm  # progress bar

from ..custom_exceptions.exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, RectifiedImgPathNotProvided, \
    StereoCalibrationParamsPathNotProvided, MissingParameters, RectificationMapsPathNotProvided, StereoRectificationError

colorama_init(autoreset=True)

# Draw epipolar lines for visualization
def draw_epilines_aligned(
        img_left: np.ndarray,
        img_right: np.ndarray,
        num_lines: int = 15,
        roi_left: tuple = None,
        roi_right: tuple = None,
        line_thickness: int = 2,
        roi_thickness: int = 2
) -> tuple[np.ndarray, np.ndarray]:
    """
    Draw uniformly spaced horizontal epipolar lines and optional ROI boxes on rectified images.

    :param img_left: Left rectified image.
    :param img_right: Right rectified image.
    :param num_lines: Number of horizontal epipolar lines to draw.
    :param roi_left: ROI tuple for the left image (x, y, width, height).
    :param roi_right: ROI tuple for the right image (x, y, width, height).
    :param line_thickness: Thickness of the epipolar lines.
    :param roi_thickness: Thickness of the ROI rectangle lines.
    :return: Tuple of images with horizontal epipolar lines and optional ROIs.
    """
    if img_left[0].shape != img_right[0].shape:
        raise StereoRectificationError("Images must have the same dimensions")

    img_left_with_lines = img_left.copy()
    img_right_with_lines = img_right.copy()

    # Use image dimensions or ROI if available
    height, width = img_left.shape[:2]
    roi_left = roi_left if roi_left else (0, 0, width, height)
    roi_right = roi_right if roi_right else (0, 0, width, height)

    # # Generate y-coordinates for lines within the ROI
    # y_start, y_end = roi_left[1], roi_left[1] + roi_left[3]
    # y_coords = np.linspace(y_start, y_end - 1, num_lines).astype(int)
    #
    # # Draw horizontal epipolar lines
    # for y in y_coords:
    #     color = (0, 0, 255)  # Red for lines
    #     cv.line(img_left_with_lines, (roi_left[0], y), (roi_left[0] + roi_left[2], y), color, line_thickness)
    #     cv.line(img_right_with_lines, (roi_right[0], y), (roi_right[0] + roi_right[2], y), color, line_thickness)

    # Determine vertical range for lines based on ROI or full image height
    y_start, y_end = (roi_left[1], roi_left[1] + roi_left[3]) if roi_left else (0, height)
    y_coords = np.linspace(y_start, y_end - 1, num_lines).astype(int)

    # Draw horizontal epipolar lines across full width
    for y in y_coords:
        color = (0, 0, 255)  # Red for lines
        cv.line(img_left_with_lines, (0, y), (width, y), color, line_thickness)
        cv.line(img_right_with_lines, (0, y), (width, y), color, line_thickness)

    # Draw ROI rectangles
    if roi_left:
        cv.rectangle(img_left_with_lines, (roi_left[0], roi_left[1]),
                     (roi_left[0] + roi_left[2], roi_left[1] + roi_left[3]), (0, 255, 0), roi_thickness)
    if roi_right:
        cv.rectangle(img_right_with_lines, (roi_right[0], roi_right[1]),
                     (roi_right[0] + roi_right[2], roi_right[1] + roi_right[3]), (0, 255, 0), roi_thickness)

    return img_left_with_lines, img_right_with_lines


def stereo_rectify(
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    cameraMatrix_left: np.ndarray = None,
    cameraMatrix_right: np.ndarray = None,
    distortionCoefficients_left: np.ndarray = None,
    distortionCoefficients_right: np.ndarray = None,
    R: np.ndarray = None,
    T: np.ndarray = None,
    F: np.ndarray = None,
    imgPoints_left: np.ndarray = None,
    imgPoints_right: np.ndarray = None,
    whichImage: int = 0,
    saveRectifiedImages: bool = False,
    rectifiedImagesDirPath: str = "./rectifiedImages",
    globImgExtension: str = "png",
    showRectifiedImages: bool = False,
    loadStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    saveRectificationMaps: bool = False,
    loadRectificationMaps: bool = False,
    rectificationMapsPath: str = "",
    testInterpolationMethods: bool = False,
    drawEpipolarLinesParams: tuple[int, int, int] = (15, 2, 2),
):
    """
        Perform stereo rectification on a pair of stereo images and visualize epipolar lines.

        :param str calibImgDirPath_left: Path to the directory containing left camera images for rectification.
        :param str calibImgDirPath_right: Path to the directory containing right camera images for rectification.
        :param np.ndarray cameraMatrix_left: Intrinsic matrix of the left camera (3x3). Required if not loading parameters.
        :param np.ndarray cameraMatrix_right: Intrinsic matrix of the right camera (3x3). Required if not loading parameters.
        :param np.ndarray distortionCoefficients_left: Distortion coefficients of the left camera.
        :param np.ndarray distortionCoefficients_right: Distortion coefficients of the right camera.
        :param np.ndarray R: Rotation matrix (3x3) between the two cameras. Required if not loading parameters.
        :param np.ndarray T: Translation vector (3x1) between the two cameras. Required if not loading parameters.
        :param np.ndarray F: Fundamental matrix (3x3) relating the two images. Required for epipolar line visualization.
        :param np.ndarray imgPoints_left: Image points from the left camera (e.g., corners of the chessboard).
        :param np.ndarray imgPoints_right: Corresponding image points from the right camera.
        :param int whichImage: Index of the image pair to use for rectification and visualization (default is 0).
        :param bool saveRectifiedImages: Whether to save the rectified images to a directory (default is False).
        :param str rectifiedImagesDirPath: Directory to save rectified images if `saveRectifiedImages` is True.
        :param str globImgExtension: File extension of input images (default is "png").
        :param bool showRectifiedImages: Whether to display rectified images with epipolar lines (default is False).
        :param bool loadStereoCalibrationParams: Whether to load stereo calibration parameters from a file.
        :param str stereoCalibrationParamsPath: Path to the stereo calibration parameters file.
        :param bool saveRectificationMaps: Whether to save rectification maps to a file (default is False).
        :param bool loadRectificationMaps: Whether to load rectification maps from a file (default is False).
        :param str rectificationMapsPath: Path to save or load rectification maps.
        :param bool testInterpolationMethods: Whether to test different interpolation methods for rectification.
        :param tuple[int, int, int] drawEpipolarLinesParams: Parameters for drawing epipolar lines (default is (15, 2, 2)).:
            - **number of lines** - Number of lines to draw (default is 15).
            - **line thickness** - Thickness of the lines (default is 2).
            - **roi rect thickness** - Thickness of the region of interest rectangle around the lines (default is 2).

        :raises CalibrationImagesNotFound: If no calibration images are found in the specified directories.
        :raises MissingParameters: If required camera parameters are missing and not loaded from a file.
        :raises RectificationMapsPathNotProvided: If the path for saving/loading rectification maps is not provided.
        :raises StereoCalibrationParamsPathNotProvided: If the path for stereo calibration parameters is not provided.

        :return: None
    """
    images_left = glob.glob(calibImgDirPath_left + "/*." + globImgExtension)
    images_right = glob.glob(calibImgDirPath_right + "/*." + globImgExtension)

    if (not images_left) or (len(images_left) == 0):
        raise CalibrationImagesNotFound

    if (not images_right) or (len(images_right) == 0):
        raise CalibrationImagesNotFound

    grayImg_left = cv.cvtColor(cv.imread(images_left[0]), cv.COLOR_BGR2GRAY)

    # User provided required params and doesn't want to load from file - calculate new rectification maps
    if not loadStereoCalibrationParams:

        if (
                cameraMatrix_left is None or
                cameraMatrix_right is None or
                distortionCoefficients_left is None or
                distortionCoefficients_right is None or
                R is None or
                T is None
        ):
            raise MissingParameters

        try:
            # Stereo Rectification
            R1, R2, P1, P2, Q, roi1, roi2 = cv.stereoRectify(
                cameraMatrix_left, distortionCoefficients_left, cameraMatrix_right, distortionCoefficients_right,
                grayImg_left.shape[::-1], R, T
            )

        except cv.error as e:
            raise StereoRectificationError(f"Error in stereo rectification process: {str(e)}")

        if not loadRectificationMaps:
            # Create rectification maps
            map1_left, map2_left = cv.initUndistortRectifyMap(cameraMatrix_left, distortionCoefficients_left, R1, P1, grayImg_left.shape[::-1], cv.CV_16SC2)

            map1_right, map2_right = cv.initUndistortRectifyMap(cameraMatrix_right, distortionCoefficients_right, R2, P2, grayImg_left.shape[::-1], cv.CV_16SC2)

    # User provided required calibration params and wants to load them from file to calculate rectification maps
    else:
        try:
            from ..content_loaders import load_stereo_calibration

            print(Fore.GREEN + "\nLoading the STEREO calibration parameters...")

            stereoCalibrationParams = load_stereo_calibration(stereoCalibrationParamsPath)

            cameraMatrix_left = stereoCalibrationParams["cameraMatrix_left"]
            cameraMatrix_right = stereoCalibrationParams["cameraMatrix_right"]
            distortionCoefficients_left = stereoCalibrationParams["distortionCoefficients_left"]
            distortionCoefficients_right = stereoCalibrationParams["distortionCoefficients_right"]
            R = stereoCalibrationParams["rotationMatrix"]
            T = stereoCalibrationParams["translationVector"]
            F = stereoCalibrationParams["fundamentalMatrix"]

            # Stereo Rectification
            R1, R2, P1, P2, Q, roi1, roi2 = cv.stereoRectify(
                cameraMatrix_left, distortionCoefficients_left, cameraMatrix_right, distortionCoefficients_right,
                grayImg_left.shape[::-1], R, T
            )

            if not loadRectificationMaps:
                # Create rectification maps
                map1_left, map2_left = cv.initUndistortRectifyMap(cameraMatrix_left, distortionCoefficients_left, R1, P1, grayImg_left.shape[::-1], cv.CV_16SC2)

                map1_right, map2_right = cv.initUndistortRectifyMap(cameraMatrix_right, distortionCoefficients_right, R2, P2, grayImg_left.shape[::-1], cv.CV_16SC2)

        except StereoCalibrationParamsPathNotProvided:
            print(Fore.RED + "Error loading stereo calibration parameters!")
            raise

        except CalibrationParamsPathNotProvided:
            print(Fore.RED + "Error loading calibration parameters!")
            raise

        except Exception as e:
            print(Fore.RED + f"Unknown error occurred\nError: {e}\n")

    # User provided required maps and wants to load them from file
    if loadRectificationMaps:
        try:
            from ..content_loaders import load_rectification_maps

            print(Fore.GREEN + "\nLoading the rectification maps...")

            rectificationMaps = load_rectification_maps(rectificationMapsPath)

            map1_left = rectificationMaps["map1_left"]
            map2_left = rectificationMaps["map2_left"]
            map1_right = rectificationMaps["map1_right"]
            map2_right = rectificationMaps["map2_right"]

        except RectificationMapsPathNotProvided:
            print(Fore.RED + "\nError loading rectification maps!\n")
            raise

    # User wants to save rectification maps
    if saveRectificationMaps:
        if (not rectificationMapsPath) or (len(rectificationMapsPath) == 0):
            raise RectificationMapsPathNotProvided

        try:
            from ..content_loaders import save_calibration

            if (not map1_left) or (not map2_left) or (not map1_right) or (not map2_right):
                raise MissingParameters

            print(Fore.GREEN + "\nSaving the rectification maps...")

            rectificationParams = {
                "map1_left": map1_left,
                "map2_left": map2_left,
                "map1_right": map1_right,
                "map2_right": map2_right,
            }

            save_calibration(rectificationParams, rectificationMapsPath)

        except CalibrationParamsPathNotProvided:
            print(Fore.RED + "\nError occurred while saving the calibration parameters!\n")
            raise

        except Exception as e:
            print(Fore.RED + "\nUnknown error occurred\n")
            raise

    if F is None or imgPoints_left is None or imgPoints_right is None:
        raise MissingParameters("F, imgPoints_left, and imgPoints_right must not be None")

    if testInterpolationMethods:
        interpolationTypes = [cv.INTER_NEAREST, cv.INTER_LINEAR, cv.INTER_CUBIC, cv.INTER_AREA, cv.INTER_LANCZOS4]
        interpolationTypesNames = ["INTER_NEAREST", "INTER_LINEAR", "INTER_CUBIC", "INTER_AREA", "INTER_LANCZOS4"]
        rectifiedImagesDifferentInterpolations = []

        # Load an example pair of images for rectification
        img_left = cv.imread(images_left[whichImage])
        img_right = cv.imread(images_right[whichImage])

        if img_left.shape != img_right.shape:
            raise StereoRectificationError("Images must have the same dimensions")

        for i, interpolationType in enumerate(tqdm(
                    interpolationTypes,
                    desc=Style.RESET_ALL + "Testing interpolation methods...",
                    dynamic_ncols=True,
                    bar_format="{l_bar}{bar}{r_bar}",
                    colour="green",
                    file=stdout
        )):
            tic_1 = perf_counter()
            rectified_left = cv.remap(img_left, map1_left, map2_left, interpolationType)
            tic_2 = perf_counter()
            rectified_right = cv.remap(img_right, map1_right, map2_right, interpolationType)
            toc = perf_counter()

            tqdm.write(Fore.MAGENTA + f"\nInterpolation type {interpolationTypesNames[i]}:\n\tleft_image: {tic_2 - tic_1}\n\tright_image: {toc - tic_2}\n\ttotal: {toc - tic_1}", nolock=True, file=stdout)

            # Draw epilines using the fundamental matrix F
            rectified_left_with_lines, rectified_right_with_lines = draw_epilines_aligned(
                rectified_left,
                rectified_right,
                num_lines=drawEpipolarLinesParams[0],
                roi_left=roi1,
                roi_right=roi2,
                line_thickness=drawEpipolarLinesParams[1],
                roi_thickness=drawEpipolarLinesParams[2]
            )

            # Combine the images side-by-side for visualization
            rectified_pair = np.hstack((rectified_left_with_lines, rectified_right_with_lines))
            # rectified_pair = np.hstack((rectified_left, rectified_right))

            rectifiedImagesDifferentInterpolations.append(rectified_pair)

            if showRectifiedImages:
                cv.imshow(f'Rectified Stereo Image: {interpolationTypesNames[i]}', rectified_pair)
                cv.waitKey(0)
                cv.destroyAllWindows()

    else:
        # Load an example pair of images for rectification
        img_left = cv.imread(images_left[whichImage])
        img_right = cv.imread(images_right[whichImage])

        if img_left.shape != img_right.shape:
            raise StereoRectificationError("Images must have the same dimensions")

        # Apply rectification to both images
        rectified_left = cv.remap(img_left, map1_left, map2_left, cv.INTER_LINEAR)
        rectified_right = cv.remap(img_right, map1_right, map2_right, cv.INTER_LINEAR)

        # Draw epilines using the fundamental matrix F
        rectified_left_with_lines, rectified_right_with_lines = draw_epilines_aligned(
            rectified_left,
            rectified_right,
            num_lines=drawEpipolarLinesParams[0],
            roi_left=roi1,
            roi_right=roi2,
            line_thickness=drawEpipolarLinesParams[1],
            roi_thickness=drawEpipolarLinesParams[2]
        )

        # Combine the images side-by-side for visualization
        rectified_pair = np.hstack((rectified_left_with_lines, rectified_right_with_lines))

        if showRectifiedImages:
            cv.imshow('Rectified Stereo Image', rectified_pair)
            cv.waitKey(0)
            cv.destroyAllWindows()

    # Save the rectified image to a file
    if saveRectifiedImages:
        if (not rectifiedImagesDirPath) or (len(rectifiedImagesDirPath) == 0):
            raise RectifiedImgPathNotProvided

        if not os.path.exists(rectifiedImagesDirPath):
            os.makedirs(rectifiedImagesDirPath)

        print(Fore.GREEN + f"\nSaving rectified images to '{rectifiedImagesDirPath}'...")

        if testInterpolationMethods and (len(rectifiedImagesDifferentInterpolations) > 0):
            for i, rectified_pair in enumerate(rectifiedImagesDifferentInterpolations):
                cv.imwrite(os.path.join(rectifiedImagesDirPath, f"rectified_pair_{interpolationTypesNames[i]}.png"), rectified_pair)

        else:
            cv.imwrite(os.path.join(rectifiedImagesDirPath, "rectified_left.png"), rectified_left)
            cv.imwrite(os.path.join(rectifiedImagesDirPath, "rectified_right.png"), rectified_right)
            cv.imwrite(os.path.join(rectifiedImagesDirPath, "rectified_stereo_pair.png"), rectified_pair)