import os

import cv2 as cv
from numpy import ndarray as npNdArray

from ..custom_exceptions.exceptions import ImgToUndistortPathNotProvided, UndistortedImgPathNotProvided


def remove_distortion(
    cameraMatrix: npNdArray,
    distortionCoefficients: npNdArray,
    imgToUndistortPath: str,
    showImgToUndistort: bool = False,
    showUndistortedImg: bool = False,
    saveUndistortedImg: bool = False,
    undistortedImgPath: str = "",
    undistortionMethod: str = "undistort",
) -> None:
    """
    Remove distortion from given image

    :param npNdArray cameraMatrix: Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters.
    :param npNdArray distortionCoefficients: Distortion Coefficients: (`k₁`, `k₂`, `p₁`, `p₂`, `k₃`), which include radial (`kₙ`) and tangential (`pₙ`) distortion values.
    :param str imgToUndistortPath: Path of the image which we want to undistort.
    :param bool showImgToUndistort: Decide if you want to show the original image., defaults to False
    :param bool showUndistortedImg: Decide if you want to show the undistorted image., defaults to False
    :param bool saveUndistortedImg: Decide if you want to save the undistorted image., defaults to False
    :param str undistortedImgPath: Path where we want to save the undistorted image., defaults to ""
    :param str undistortionMethod: Choose the method used for removing distortion (`undistort` or `remapping`)., defaults to "undistort"

    :return: None

    :raises ImgToUndistortPathNotProvided: Raises an error if the path of the image which you want to undistort was not provided, or it isn't an instance of a string.
    :raises UndistortedImgPathNotProvided: Raises an error if the path where the undistorted image should be saved was not provided, or it isn't an instance of a string.
    """

    if (imgToUndistortPath == "") or (not isinstance(imgToUndistortPath, str)) or not imgToUndistortPath:
        raise ImgToUndistortPathNotProvided

    if saveUndistortedImg and (
        (undistortedImgPath == "") or (not isinstance(undistortedImgPath, str)) or not undistortedImgPath
    ):
        raise UndistortedImgPathNotProvided

    # "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/58.png"
    img = cv.imread(imgToUndistortPath)
    if img is None:
        raise ValueError(f"Failed to load image from path: {imgToUndistortPath}")

    if showImgToUndistort:
        cv.imshow("Current Image", img)
        print("\nPress any key to continue...")
        cv.waitKey()

    h, w = img.shape[:2]
    newOptimalCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
        cameraMatrix, distortionCoefficients, (w, h), 0.3, (w, h)
    )

    if undistortionMethod == "undistort":
        dst = cv.undistort(
            img, cameraMatrix, distortionCoefficients, None, newOptimalCameraMatrix
        )

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow("Undistorted image", dst)
            print("\nPress any key to continue...")
            cv.waitKey()

    elif undistortionMethod == "remapping":
        mapx, mapy = cv.initUndistortRectifyMap(
            cameraMatrix,
            distortionCoefficients,
            None,
            newOptimalCameraMatrix,
            (w, h),
            5,
        )
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow("Undistorted image", dst)
            print("\nPress any key to continue...")
            cv.waitKey()

    else:
        raise ValueError(f"Invalid undistortion method: {undistortionMethod}. Use 'undistort' or 'remapping'.")

    if saveUndistortedImg:
        if not os.path.exists(undistortedImgPath):
            os.makedirs(undistortedImgPath, exist_ok=True)

        file_name, file_extension = os.path.splitext(os.path.basename(imgToUndistortPath))

        new_file_name = f"{file_name}_undistorted{file_extension}"

        cv.imwrite(os.path.join(undistortedImgPath, new_file_name), dst)
