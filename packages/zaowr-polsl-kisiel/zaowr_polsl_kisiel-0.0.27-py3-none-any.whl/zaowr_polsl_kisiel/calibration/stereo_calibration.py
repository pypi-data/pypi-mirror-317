from typing import Any
import numpy as np
import cv2 as cv
from cv2 import aruco
import glob

from tqdm import tqdm # progress bar
from colorama import Fore, Style, init as colorama_init #, Back
from sys import stdout
from os.path import basename

from ..custom_exceptions.exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, CalibrationParamsWrongFormat, StereoCalibrationParamsPathNotProvided, CharucoCalibrationError

colorama_init(autoreset=True)

def calculate_fov(cameraMatrix: np.ndarray, imageSize: tuple[float, float]):
    """
    Calculate the horizontal and vertical FOV for a given camera.

    :param np.ndarray cameraMatrix: Intrinsic camera matrix (3x3).
    :param tuple[float, float] imageSize: Tuple containing image width and height (width, height).

    :return: tuple[float, float] Horizontal FOV and vertical FOV in degrees.
    """
    fx = cameraMatrix[0, 0]  # Focal length in x-axis
    fy = cameraMatrix[1, 1]  # Focal length in y-axis
    width, height = imageSize

    fov_horizontal = 2 * np.arctan2(width, (2 * fx)) * (180 / np.pi)  # Convert radians to degrees
    fov_vertical = 2 * np.arctan2(height, (2 * fy)) * (180 / np.pi)  # Convert radians to degrees

    return fov_horizontal, fov_vertical

def stereo_calibration(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath_left: str,
    calibImgDirPath_right: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    loadCalibrationParams: bool = False,
    calibrationParamsPath_left: str = "",
    calibrationParamsPath_right: str = "",
    saveStereoCalibrationParams: bool = False,
    stereoCalibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
                                cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
                                30,
                                0.001
                            ),
    stereoCalibrationFlags: Any = cv.CALIB_FIX_INTRINSIC,
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None:
    """
    Perform stereo camera calibration using chessboard or ChArUco images from both left and right cameras.
    This function calculates intrinsic and extrinsic parameters for both cameras and computes the baseline
    and Field of View (FOV) for each camera (horizontal and vertical).

    :param tuple[int, int] chessBoardSize: Tuple of integers representing the number of internal corners in the chessboard pattern (rows, columns).
    :param float squareRealDimensions: Real-world size of each square on the chessboard in millimeters.
    :param str calibImgDirPath_left: Path to the directory containing calibration images for the left camera.
    :param str calibImgDirPath_right: Path to the directory containing calibration images for the right camera.
    :param str globImgExtension: Extension of the calibration images (default is "png").
    :param bool saveCalibrationParams: Whether to save the individual camera calibration parameters (default is False).
    :param bool loadCalibrationParams: Whether to load pre-calibrated parameters for the cameras (default is False).
    :param str calibrationParamsPath_left: Path to the pre-calibrated parameters for the left camera (default is empty).
    :param str calibrationParamsPath_right: Path to the pre-calibrated parameters for the right camera (default is empty).
    :param bool saveStereoCalibrationParams: Whether to save the stereo calibration parameters (default is False).
    :param str stereoCalibrationParamsPath: Path to save the stereo calibration parameters (default is empty).
    :param bool displayFoundCorners: Whether to display the found chessboard or ChArUco corners during calibration (default is False).
    :param bool displayMSE: Whether to display the Mean Squared Error (MSE) during calibration (default is False).
    :param bool improveSubPix: Whether to refine the corner detection to sub-pixel accuracy (default is True).
    :param bool showListOfImagesWithChessboardFound: Whether to display the list of images where the chessboard or ChArUco board was detected (default is False).
    :param tuple[Any, int, float] terminationCriteria: Criteria for corner refinement, in the form of a tuple (type, max_iter, epsilon) (default is set to terminate after 30 iterations or when epsilon is less than 0.001).
    :param Any stereoCalibrationFlags: Flags for stereo calibration (default is to fix intrinsic parameters using cv.CALIB_FIX_INTRINSIC).
    :param bool useCharuco: Whether to use ChArUco boards instead of chessboards for calibration (default is False).
    :param str charucoDictName: Name of the predefined ArUco dictionary for generating ChArUco boards (default is "DICT_6X6_250").
    :param float markerLength: Length of the markers in ChArUco board in millimeters (default is 20.0).
    :param bool displayIds: If True and `useCharuco` is enabled, displays corner IDs alongside detected corners of the chessboard (ids on markers are always shown) (default is False).

    :return: None

    :raises CalibrationImagesNotFound: If calibration images for the left or right camera are not found in the specified directories.
    :raises CalibrationParamsPathNotProvided: If the path to save or load calibration parameters is not provided when required.
    :raises CalibrationParamsWrongFormat: If the calibration parameters are not in the correct format.
    :raises StereoCalibrationParamsPathNotProvided: If the path to save stereo calibration parameters is not provided when required.
    :raises CharucoCalibrationError: If ChArUco board calibration fails due to insufficient markers being detected.
    """
    if chessBoardSize[0] <= 0 or chessBoardSize[1] <= 0:
        raise ValueError("Chessboard dimensions must be greater than zero")

    # e.g. "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
    images_left = glob.glob(calibImgDirPath_left + "/*." + globImgExtension)
    images_right = glob.glob(calibImgDirPath_right + "/*." + globImgExtension)

    if (not images_left) or (len(images_left) == 0):
        raise CalibrationImagesNotFound

    if (not images_right) or (len(images_right) == 0):
        raise CalibrationImagesNotFound

    if not loadCalibrationParams:
        if useCharuco:
            try:
                arucoDict = getattr(aruco, charucoDictName)
                dictionary = aruco.getPredefinedDictionary(arucoDict)
                board = aruco.CharucoBoard(chessBoardSize, squareRealDimensions, markerLength, dictionary)
                # board.setLegacyPattern(True)  # comment this line to create the new template

                # Setup the charuco detector
                charucoParams = aruco.CharucoParameters()
                detectorParams = aruco.DetectorParameters()
                refineParams = aruco.RefineParameters()

                if improveSubPix:
                    charucoParams.tryRefineMarkers = True
                    charucoParams.minMarkers = 0
                    detectorParams.adaptiveThreshConstant = 19
                    detectorParams.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
                    detectorParams.cornerRefinementMinAccuracy = 0.001
                    detectorParams.cornerRefinementMaxIterations = 30
                    detectorParams.cornerRefinementWinSize = 11

                charucoDetector = aruco.CharucoDetector(board, charucoParams, detectorParams, refineParams)
                charucoDetector.setBoard(board)

                objPoints = []  # 3d point in real world space
                imgPoints_left = []  # 2d points in image plane.
                imgPoints_right = []  # 2d points in image plane.
                imgSize = None
                chessboardFound = []
                chessboardSkipped = []

                for i, _ in enumerate(tqdm(
                        images_left,
                        desc=Style.RESET_ALL + "Processing images...",
                        dynamic_ncols=True,
                        bar_format="{l_bar}{bar}{r_bar}",
                        colour="green",
                        file=stdout
                )):
                    baseFileName_left = basename(images_left[i])
                    img_left = cv.imread(images_left[i])
                    grayImg_left = cv.cvtColor(img_left, cv.COLOR_BGR2GRAY)

                    if imgSize is None:
                        imgSize = grayImg_left.shape[::-1]

                    tqdm.write(Fore.GREEN + f"\nProcessing LEFT image from set no.{i + 1} ({baseFileName_left}).", nolock=True, file=stdout)

                    charucoCorners_left, charucoIds_left, arucoCorners_left, arucoIds_left = charucoDetector.detectBoard(grayImg_left)

                    if (
                            (charucoCorners_left is None) or (len(charucoCorners_left) <= 0)
                            or (charucoIds_left is None) or (len(charucoIds_left) <= 0)
                            or (arucoCorners_left is None) or (len(arucoCorners_left) <= 0)
                            or (arucoIds_left is None) or (len(arucoIds_left) <= 4)
                    ):
                        tqdm.write(
                            Fore.RED
                            + f"Skipped image set no.{i + 1} due to insufficient ChArUco markers in LEFT image ({baseFileName_left}).",
                            nolock=True,
                            file=stdout,
                        )
                        chessboardSkipped.append(baseFileName_left)
                        continue

                    tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)

                    baseFileName_right = basename(images_right[i])
                    img_right = cv.imread(images_right[i])
                    grayImg_right = cv.cvtColor(img_right, cv.COLOR_BGR2GRAY)

                    tqdm.write(Fore.GREEN + f"Processing RIGHT image from set no.{i + 1} ({baseFileName_right}).", nolock=True, file=stdout)

                    charucoCorners_right, charucoIds_right, arucoCorners_right, arucoIds_right = charucoDetector.detectBoard(grayImg_right)

                    if (
                            (charucoCorners_right is None) or (len(charucoCorners_right) <= 0)
                            or (charucoIds_right is None) or (len(charucoIds_right) <= 0)
                            or (arucoCorners_right is None) or (len(arucoCorners_right) <= 0)
                            or (arucoIds_right is None) or (len(arucoIds_right) <= 4)
                            # found less than 4 markers
                    ):
                        tqdm.write(Fore.RED + f"Skipped image set no.{i+1} due to insufficient ChArUco markers in RIGHT image ({baseFileName_left}).", nolock=True, file=stdout)
                        chessboardSkipped.append(baseFileName_left)
                        continue

                    tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)
                    # chessboardFound[f"{i}_L"] = baseFileName_left
                    # chessboardFound[f"{i}_R"] = baseFileName_right
                    chessboardFound.append(baseFileName_left)

                    if displayFoundCorners:
                        if displayIds:
                            # LEFT
                            imgWithMarkers_left = aruco.drawDetectedMarkers(img_left, arucoCorners_left, arucoIds_left)

                            # show ids (e.g. id=1) next to the detected corners
                            charucoCornersFiltered_left = [corner for corner, id in zip(charucoCorners_left, charucoIds_left) if id is not None]
                            imgWithMarkers_left = aruco.drawDetectedCornersCharuco(imgWithMarkers_left, np.array(charucoCornersFiltered_left), np.array(charucoIds_left))

                            # RIGHT
                            imgWithMarkers_right = aruco.drawDetectedMarkers(img_right, arucoCorners_right, arucoIds_right)

                            # show ids (e.g. id=1) next to the detected corners
                            charucoCornersFiltered_right = [corner for corner, id in zip(charucoCorners_right, charucoIds_right) if id is not None]
                            imgWithMarkers_right = aruco.drawDetectedCornersCharuco(imgWithMarkers_right, np.array(charucoCornersFiltered_right), np.array(charucoIds_right))

                        else:
                            # LEFT
                            imgWithMarkers_left = aruco.drawDetectedMarkers(img_left, arucoCorners_left, arucoIds_left)
                            # dont show ids (e.g. id=1) next to the detected corners
                            imgWithMarkers_left = aruco.drawDetectedCornersCharuco(imgWithMarkers_left, np.array(charucoCorners_left), None)

                            # RIGHT
                            imgWithMarkers_right = aruco.drawDetectedMarkers(img_right, arucoCorners_right, arucoIds_right)
                            # dont show ids (e.g. id=1) next to the detected corners
                            imgWithMarkers_right = aruco.drawDetectedCornersCharuco(imgWithMarkers_right, np.array(charucoCorners_right), None)

                        cv.imshow("Detected ChArUco Markers in LEFT Image", imgWithMarkers_left)
                        cv.waitKey(500)

                        cv.imshow("Detected ChArUco Markers in RIGHT Image", imgWithMarkers_right)
                        cv.waitKey(500)

                    cv.destroyAllWindows()

                    # LEFT
                    objectPoints_left, imagePoints_left = board.matchImagePoints(charucoCorners_left, charucoIds_left)

                    objPoints.append(objectPoints_left)
                    imgPoints_left.append(imagePoints_left)

                    # RIGHT
                    objectPoints_right, imagePoints_right = board.matchImagePoints(charucoCorners_right, charucoIds_right)

                    # objPoints.append(objectPoints_left)
                    imgPoints_right.append(imagePoints_right)



                if len(objPoints) < 1:
                    raise CharucoCalibrationError

                # for i, (obj, imgL, imgR) in enumerate(zip(objPoints, imgPoints_left, imgPoints_right)):
                #     print(f"Index {i}: objPoints shape: {obj.shape}, imgPoints_left shape: {imgL.shape}, imgPoints_right shape: {imgR.shape}")

                # ensures that only valid sets of object points(objPoints), left image points(imgPoints_left), and right image points(imgPoints_right) are retained for calibration.This is done by filtering out any sets where the number of points in these arrays is inconsistent.
                valid_data = [
                    (obj, imgL, imgR)
                    for obj, imgL, imgR in zip(objPoints, imgPoints_left, imgPoints_right)
                    if obj.shape[0] == imgL.shape[0] == imgR.shape[0]
                ]
                objPoints, imgPoints_left, imgPoints_right = zip(*valid_data)

                print(Fore.GREEN + "\nCalibrating LEFT camera...")
                rms_left, cameraMatrix_left, distortionCoefficients_left, rotationVectors_left, translationVectors_left = cv.calibrateCamera(
                        objPoints,
                        imgPoints_left,
                        imgSize,
                        None,
                        None
                    )

                print(Fore.GREEN + "\nCalibrating RIGHT camera...")
                rms_right, cameraMatrix_right, distortionCoefficients_right, rotationVectors_right, translationVectors_right = cv.calibrateCamera(
                        objPoints,
                        imgPoints_right,
                        imgSize,
                        None,
                        None
                    )

                mse_left = 0
                mse_right = 0
                for i in range(len(objPoints)):
                    imgPoints_left_improved, _ = cv.projectPoints(
                        objPoints[i],
                        rotationVectors_left[i],
                        translationVectors_left[i],
                        cameraMatrix_left,
                        distortionCoefficients_left,
                    )
                    error = cv.norm(imgPoints_left[i], imgPoints_left_improved, cv.NORM_L2) / len(imgPoints_left_improved)
                    mse_left += error

                    imgPoints_right_improved, _ = cv.projectPoints(
                        objPoints[i],
                        rotationVectors_right[i],
                        translationVectors_right[i],
                        cameraMatrix_right,
                        distortionCoefficients_right,
                    )
                    error = cv.norm(imgPoints_right[i], imgPoints_right_improved, cv.NORM_L2) / len(imgPoints_right_improved)
                    mse_right += error


                mse_left = mse_left / len(objPoints)
                mse_right = mse_right / len(objPoints)
                if displayMSE:
                    print(f"\nMean reprojection error left: {mse_left}")
                    print(f"\nMean reprojection error right: {mse_left}")

                if saveCalibrationParams:
                    try:
                        from ..content_loaders import save_calibration

                        print(Fore.GREEN + "\nSaving the calibration parameters of LEFT camera...")

                        calibrationParams_left = {
                            "mse": mse_left,
                            "rms": rms_left,
                            "objPoints": [obj.tolist() for obj in objPoints[0]],
                            "imgPoints": [img.tolist() for img in imgPoints_left[0]],
                            "cameraMatrix": cameraMatrix_left.tolist(),
                            "distortionCoefficients": distortionCoefficients_left.tolist(),
                            "rotationVectors": [rvec.tolist() for rvec in rotationVectors_left],
                            "translationVectors": [tvec.tolist() for tvec in translationVectors_left],
                        }

                        save_calibration(calibrationParams_left, calibrationParamsPath_left)

                        print(Fore.GREEN + "\nSaving the calibration parameters of RIGHT camera...")

                        calibrationParams_right = {
                            "mse": mse_right,
                            "rms": rms_right,
                            "objPoints": [obj.tolist() for obj in objPoints[0]],
                            "imgPoints": [img.tolist() for img in imgPoints_right[0]],
                            "cameraMatrix": cameraMatrix_right.tolist(),
                            "distortionCoefficients": distortionCoefficients_right.tolist(),
                            "rotationVectors": [rvec.tolist() for rvec in rotationVectors_right],
                            "translationVectors": [tvec.tolist() for tvec in translationVectors_right],
                        }

                        save_calibration(calibrationParams_right, calibrationParamsPath_right)

                    except CalibrationParamsPathNotProvided:
                        print(Fore.RED + "\nError occurred while saving the calibration parameters!\n")
                        raise

                    except Exception as e:
                        print(Fore.RED + "\nUnknown error occurred\n")
                        raise

            except AttributeError:
                raise ValueError(f"Invalid ArUco dictionary name: {charucoDictName}")

        else:
            ######################################################################################
            # Calibrate both cameras
            ######################################################################################
            objP = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
            objP[:, :2] = (
                np.mgrid[0 : chessBoardSize[0], 0 : chessBoardSize[1]].T.reshape(-1, 2)
                * squareRealDimensions
            )

            # Arrays to store object points and image points from all the images.
            objPoints = []  # 3d point in real world space
            imgPoints_left = []  # 2d points in image plane.
            imgPoints_right = []  # 2d points in image plane.
            imgSize = None
            chessboardFound = [] # list of images with chessboard detected properly
            chessboardSkipped = []

            for i, _ in enumerate(tqdm(
                    images_left,
                    desc=Style.RESET_ALL + "Processing images...",
                    dynamic_ncols=True,
                    bar_format="{l_bar}{bar}{r_bar}",
                    colour="green",
                    file=stdout
            )):
                baseFileName_left = basename(images_left[i])
                img_left = cv.imread(images_left[i])
                grayImg_left = cv.cvtColor(img_left, cv.COLOR_BGR2GRAY)

                if imgSize is None:
                    imgSize = grayImg_left.shape[::-1]

                tqdm.write(Fore.GREEN + f"\nProcessing LEFT image from set no.{i + 1} ({baseFileName_left}).", nolock=True, file=stdout)

                # Find the chess board corners
                ret_left, corners_left = cv.findChessboardCorners(
                    grayImg_left, (chessBoardSize[0], chessBoardSize[1]), None
                )

                if not ret_left:
                    tqdm.write(Fore.RED + f"Skipped image set no.{i + 1} because corners were not found in LEFT image ({baseFileName_left}).",
                               nolock=True, file=stdout)
                    chessboardSkipped.append(baseFileName_left)
                    continue

                tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)

                baseFileName_right = basename(images_right[i])
                img_right = cv.imread(images_right[i])
                grayImg_right = cv.cvtColor(img_right, cv.COLOR_BGR2GRAY)

                tqdm.write(Fore.GREEN + f"Processing RIGHT image from set no.{i + 1} ({baseFileName_right}).", nolock=True, file=stdout)

                ret_right, corners_right = cv.findChessboardCorners(
                    grayImg_right, (chessBoardSize[0], chessBoardSize[1]), None
                )

                if not ret_right:
                    tqdm.write(Fore.RED + f"Skipped image set no.{i + 1} because corners were not found in RIGHT image ({baseFileName_left}).",
                               nolock=True, file=stdout)
                    chessboardSkipped.append(baseFileName_left)
                    continue

                tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)
                # chessboardFound[f"{i}_L"] = baseFileName_left
                # chessboardFound[f"{i}_R"] = baseFileName_right
                chessboardFound.append(baseFileName_left)

                objPoints.append(objP)

                if improveSubPix:
                    # LEFT
                    corners_left = cv.cornerSubPix(
                        grayImg_left, corners_left, (11, 11), (-1, -1), terminationCriteria
                    )

                    # RIGHT
                    corners_right = cv.cornerSubPix(
                        grayImg_right, corners_right, (11, 11), (-1, -1), terminationCriteria
                    )

                imgPoints_left.append(corners_left)
                imgPoints_right.append(corners_right)

                if displayFoundCorners:
                    # Draw and display the corners
                    # LEFT
                    cv.drawChessboardCorners(
                        img_left, (chessBoardSize[0], chessBoardSize[1]), corners_left, ret_left
                    )
                    cv.imshow("Current LEFT Image", img_left)
                    cv.waitKey(500)

                    # RIGHT
                    cv.drawChessboardCorners(
                        img_right, (chessBoardSize[0], chessBoardSize[1]), corners_right, ret_right
                    )
                    cv.imshow("Current RIGHT Image", img_right)
                    cv.waitKey(500)

            cv.destroyAllWindows()

            # overall RMS re-projection error, camera matrix, distortion coefficients, rotation vectors, translation vectors
            print(Fore.GREEN + "\nCalibrating LEFT camera...")
            rms_left, cameraMatrix_left, distortionCoefficients_left, rotationVectors_left, translationVectors_left = (
                cv.calibrateCamera(objPoints, imgPoints_left, imgSize, None, None)
            )

            print(Fore.GREEN + "\nCalibrating RIGHT camera...")
            rms_right, cameraMatrix_right, distortionCoefficients_right, rotationVectors_right, translationVectors_right = (
                cv.calibrateCamera(objPoints, imgPoints_right, imgSize, None, None)
            )

            mse_left = 0
            mse_right = 0
            for i in range(len(objPoints)):
                imgPoints_left_improved, _ = cv.projectPoints(
                    objPoints[i],
                    rotationVectors_left[i],
                    translationVectors_left[i],
                    cameraMatrix_left,
                    distortionCoefficients_left,
                )
                error = cv.norm(imgPoints_left[i], imgPoints_left_improved, cv.NORM_L2) / len(imgPoints_left_improved)
                mse_left += error

                imgPoints_right_improved, _ = cv.projectPoints(
                    objPoints[i],
                    rotationVectors_right[i],
                    translationVectors_right[i],
                    cameraMatrix_right,
                    distortionCoefficients_right,
                )
                error = cv.norm(imgPoints_right[i], imgPoints_right_improved, cv.NORM_L2) / len(imgPoints_right_improved)
                mse_right += error

            mse_left = mse_left / len(objPoints)
            mse_right = mse_right / len(objPoints)
            if displayMSE:
                print(f"\nMean reprojection error left: {mse_left}")
                print(f"\nMean reprojection error right: {mse_left}")

            if saveCalibrationParams:
                try:
                    from ..content_loaders import save_calibration

                    print(Fore.GREEN + "\nSaving the calibration parameters of LEFT camera...")

                    calibrationParams_left = {
                        "mse": mse_left,
                        "rms": rms_left,
                        "objPoints": [obj.tolist() for obj in objPoints],
                        "imgPoints": [img.tolist() for img in imgPoints_left],
                        "cameraMatrix": cameraMatrix_left.tolist(),
                        "distortionCoefficients": distortionCoefficients_left.tolist(),
                        "rotationVectors": [rvec.tolist() for rvec in rotationVectors_left],
                        "translationVectors": [tvec.tolist() for tvec in translationVectors_left],
                    }

                    save_calibration(calibrationParams_left, calibrationParamsPath_left)

                    print(Fore.GREEN + "\nSaving the calibration parameters of RIGHT camera...")

                    calibrationParams_right = {
                        "mse": mse_right,
                        "rms": rms_right,
                        "objPoints": [obj.tolist() for obj in objPoints],
                        "imgPoints": [img.tolist() for img in imgPoints_right],
                        "cameraMatrix": cameraMatrix_right.tolist(),
                        "distortionCoefficients": distortionCoefficients_right.tolist(),
                        "rotationVectors": [rvec.tolist() for rvec in rotationVectors_right],
                        "translationVectors": [tvec.tolist() for tvec in translationVectors_right],
                    }

                    save_calibration(calibrationParams_right, calibrationParamsPath_right)

                except CalibrationParamsPathNotProvided:
                    print(Fore.RED + "\nError occurred while saving the calibration parameters!\n")
                    raise

                except Exception as e:
                    print(Fore.RED + "\nUnknown error occurred\n")
                    raise

        if showListOfImagesWithChessboardFound:
            print(Fore.GREEN + "\nList of images with chessboard found:\n")
            print(chessboardFound)
            print(Fore.RED + "\nList of images skipped:\n")
            print(chessboardSkipped)

    else:
        try:
            from ..content_loaders import load_calibration

            print(Fore.GREEN + "\nLoading the calibration parameters of LEFT camera...")

            calibrationParams_left = load_calibration(calibrationParamsPath_left)

            # mse_left = calibrationParams_left["mse"]
            # rms_left = calibrationParams_left["rms"]
            objPoints = calibrationParams_left["objPoints"]
            imgPoints_left = calibrationParams_left["imgPoints"]
            cameraMatrix_left = calibrationParams_left["cameraMatrix"]
            distortionCoefficients_left = calibrationParams_left["distortionCoefficients"]
            rotationVectors_left = calibrationParams_left["rotationVectors"]
            translationVectors_left = calibrationParams_left["translationVectors"]

            print(Fore.GREEN + "\nLoading the calibration parameters of RIGHT camera...")

            calibrationParams_right = load_calibration(calibrationParamsPath_right)

            # mse_right = calibrationParams_right["mse"]
            # rms_right = calibrationParams_right["rms"]
            imgPoints_right = calibrationParams_right["imgPoints"]
            cameraMatrix_right = calibrationParams_right["cameraMatrix"]
            distortionCoefficients_right = calibrationParams_right["distortionCoefficients"]
            rotationVectors_right = calibrationParams_right["rotationVectors"]
            translationVectors_right = calibrationParams_right["translationVectors"]

        except CalibrationParamsPathNotProvided:
            print(Fore.RED + "\nError occurred while loading the calibration parameters!\n")
            raise

        except CalibrationParamsWrongFormat:
            print(Fore.RED + "\nCalibration parameters are not in the correct format!\n")
            raise

        except Exception as e:
            print(Fore.RED + "\nUnknown error occurred\n")
            raise


    ######################################################################################
    # Stereo calibration
    ######################################################################################
    image_size = grayImg_left.shape[::-1]  # (width, height)

    print(Fore.GREEN + "\nCalibrating STEREO cameras...")
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(
        objPoints,  # Object points
        imgPoints_left,  # Image points from the left camera
        imgPoints_right,  # Image points from the right camera
        cameraMatrix_left,  # Camera matrix for the left camera
        distortionCoefficients_left,  # Distortion coefficients for the left camera
        cameraMatrix_right,  # Camera matrix for the right camera
        distortionCoefficients_right,  # Distortion coefficients for the right camera
        image_size,  # Image size (assumes both cameras have the same resolution)
        criteria=terminationCriteria,  # Termination criteria
        flags=stereoCalibrationFlags  # Stereo calibration flags
    )

    baseline = np.round((np.linalg.norm(T)) * 0.1, 2) # baseline in cm

    # Field of View for the Left and Right Cameras
    # Calculate FOV using cameraMatrix_left and cameraMatrix_right from single camera calibration
    fov_left = calculate_fov(cameraMatrix_left, image_size)
    fov_right = calculate_fov(cameraMatrix_right, image_size)

    if saveStereoCalibrationParams:
        try:
            from ..content_loaders import save_calibration

            print(Fore.GREEN + "\nSaving the stereo calibration parameters...")

            stereoCalibrationParams = {
                "reprojectionError": ret,
                "fov_left": list(fov_left),  # FOV as list (converted to tuple on load)
                "fov_right": list(fov_right),  # FOV as list (converted to tuple on load)
                "baseline": baseline,
                "cameraMatrix_left": CM1.tolist(),
                "distortionCoefficients_left": dist1.tolist(),
                "cameraMatrix_right": CM2.tolist(),
                "distortionCoefficients_right": dist2.tolist(),
                "rotationMatrix": R.tolist(),
                "translationVector": T.tolist(),
                "essentialMatrix": E.tolist(),
                "fundamentalMatrix": F.tolist(),
            }

            save_calibration(stereoCalibrationParams, stereoCalibrationParamsPath)

        except StereoCalibrationParamsPathNotProvided:
            print(Fore.RED + "\nError occurred while saving the stereo calibration parameters!\n")
            raise

        except Exception as e:
            print(Fore.RED + "\nUnknown error occurred\n")
            raise