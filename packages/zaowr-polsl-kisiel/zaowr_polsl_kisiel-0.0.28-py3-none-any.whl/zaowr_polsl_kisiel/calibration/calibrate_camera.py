from typing import Any
import numpy as np
import cv2 as cv
from cv2 import aruco
import glob

from tqdm import tqdm # progress bar
from colorama import Fore, Style, init as colorama_init #, Back
from sys import stdout
from os.path import basename


from ..custom_exceptions.exceptions import CalibrationImagesNotFound, CalibrationParamsPathNotProvided, CharucoCalibrationError

colorama_init(autoreset=True)

def calibrate_camera(
    chessBoardSize: tuple[int, int],
    squareRealDimensions: float,
    calibImgDirPath: str,
    globImgExtension: str = "png",
    saveCalibrationParams: bool = False,
    calibrationParamsPath: str = "",
    displayFoundCorners: bool = False,
    displayMSE: bool = False,
    improveSubPix: bool = True,
    showListOfImagesWithChessboardFound: bool = False,
    terminationCriteria: tuple[Any, int, float] = (
        cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
        30,
        0.001,
    ),
    useCharuco: bool = False,
    charucoDictName: str = "DICT_6X6_250",
    markerLength: float = 20.0,
    displayIds: bool = False,
) -> None:
    """
    Calibrate the camera using chessboard images or ChArUco board images. Optionally, save the calibration parameters
    or display diagnostic outputs.

    :param tuple[int, int] chessBoardSize: Dimensions of the chessboard used for calibration, given as (WIDTH, HEIGHT).
        For example, a chessboard with 6x9 inner corners should be specified as (6, 9). Refer to OpenCV documentation:
        `https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html`.
        **for ChArUco** - exact number of squares on the board **NOT THE CORNERS ON THE INSIDE (squares - 1)** like in normal chessboard
    :param float squareRealDimensions: The real-world dimension of one side of a square on the chessboard (e.g., if each
        square is 28.67 mm, pass "28.67").
    :param str calibImgDirPath: Directory containing the calibration images.
    :param str globImgExtension: File extension of the calibration images (e.g., "jpg", "png"). Defaults to "png".
    :param bool saveCalibrationParams: If True, save the calibration parameters to a JSON file. Defaults to False.
    :param str calibrationParamsPath: Path to save the calibration parameters, required if saveCalibrationParams is True.
    :param bool displayFoundCorners: If True, displays the calibration images with detected corners. Defaults to False.
    :param bool displayMSE: If True, prints the Mean Square Error (MSE) for each image during calibration. Defaults to False.
    :param bool improveSubPix: If True, refines the detected corners to sub-pixel precision. Defaults to True.
    :param bool showListOfImagesWithChessboardFound: If True, prints the list of images where a chessboard was detected.
        Defaults to False.
    :param tuple[Any, int, float] terminationCriteria: Termination criteria for the corner refinement process. Defaults to
        (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001).
    :param bool useCharuco: If True, uses a ChArUco board for calibration instead of a chessboard. Defaults to False.
    :param str charucoDictName: The name of the ArUco dictionary to use when `useCharuco` is True. Defaults to "DICT_6X6_250".
    :param float markerLength: The length of the ArUco marker side in real-world units. Only applicable if `useCharuco`
        is True. Defaults to 20.0.
    :param bool displayIds: If True and `useCharuco` is enabled, displays corner IDs alongside detected corners of the chessboard (ids on markers are always shown). Defaults to False.

    :return: None

    :raises CalibrationImagesNotFound: If no images are found in the specified directory.
    :raises CharucoCalibrationError: If ChArUco marker detection fails or no valid markers are detected.
    :raises ValueError: If an invalid ArUco dictionary name is provided when `useCharuco` is True.

    Notes:
    - Calibration assumes that all images are taken with the same camera and resolution.
    - This function handles both traditional chessboard calibration and ChArUco board calibration.
    - For best results, use well-lit images with clear chessboard or marker visibility.
    """
    if chessBoardSize[0] <= 0 or chessBoardSize[1] <= 0:
        raise ValueError("Invalid chessBoardSize. Both dimensions must be positive integers.")

    if squareRealDimensions <= 0:
        raise ValueError("Invalid squareRealDimensions. It must be a positive float.")

    # e.g. "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
    images = glob.glob(calibImgDirPath + "/*." + globImgExtension)

    if (images == []) or (len(images) == 0):
        raise CalibrationImagesNotFound

    if useCharuco:
        try:
            arucoDict = getattr(aruco, charucoDictName)
            dictionary = aruco.getPredefinedDictionary(arucoDict)
            board = aruco.CharucoBoard(chessBoardSize, squareRealDimensions, markerLength, dictionary)
            # board.setLegacyPattern(True)  # comment this line to create the new template

            # Set up the charuco detector
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

            objPoints = []  # 3D points in real world space
            imgPoints = []  # 2D points in image plane
            imgSize = None
            chessboardFound = []
            chessboardSkipped = []

            for fileName in tqdm(
                    images,
                    desc=Style.RESET_ALL + "Processing images...",
                    dynamic_ncols=True,
                    bar_format="{l_bar}{bar}{r_bar}",
                    colour="green",
                    file=stdout
            ):

                baseFileName = basename(fileName)
                img = cv.imread(fileName)
                grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

                if imgSize is None:
                    imgSize = grayImg.shape[::-1]

                tqdm.write(Fore.GREEN + f"\nProcessing image '{baseFileName}'.", nolock=True, file=stdout)

                charucoCorners, charucoIds, arucoCorners, arucoIds = charucoDetector.detectBoard(grayImg)

                if (
                        (charucoCorners is None) or (len(charucoCorners) <= 0)
                        or (charucoIds is None) or (len(charucoIds) <= 0)
                        or (arucoCorners is None) or (len(arucoCorners) <= 0)
                        or (arucoIds is None) or (len(arucoIds) <= 4)
                ):
                    tqdm.write(Fore.RED + f"Skipped image '{baseFileName}' due to insufficient ChArUco markers.", nolock=True, file=stdout)
                    chessboardSkipped.append(baseFileName)
                    continue

                tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)
                if displayFoundCorners:
                    if displayIds:
                        imgWithMarkers = aruco.drawDetectedMarkers(img, arucoCorners, arucoIds)

                        # show ids (e.g. id=1) next to the detected corners
                        charucoCorners_filtered = [corner for corner, id in zip(charucoCorners, charucoIds) if id is not None]
                        imgWithMarkers = aruco.drawDetectedCornersCharuco(imgWithMarkers, np.array(charucoCorners_filtered), np.array(charucoIds))

                    else:
                        imgWithMarkers = aruco.drawDetectedMarkers(img, arucoCorners, arucoIds)
                        # dont show ids (e.g. id=1) next to the detected corners
                        imgWithMarkers = aruco.drawDetectedCornersCharuco(imgWithMarkers, np.array(charucoCorners), None)

                    cv.imshow("Detected ChArUco Markers", imgWithMarkers)
                    cv.waitKey(0)

                objectPoints, imagePoints = board.matchImagePoints(charucoCorners, charucoIds)

                chessboardFound.append(baseFileName)
                objPoints.append(objectPoints)
                imgPoints.append(imagePoints)



            if len(objPoints) < 1:
                raise CharucoCalibrationError

            if not objPoints or not imgPoints:
                raise ValueError("No valid chessboard patterns found in the provided images.")

            print(Fore.GREEN + "\nCalibrating camera...")
            rms, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = cv.calibrateCamera(
                    objPoints,
                    imgPoints,
                    imgSize,
                    None,
                    None
                )

            mse = 0
            for i in range(len(objPoints)):
                imgPoints2, _ = cv.projectPoints(
                    objPoints[i],
                    rotationVectors[i],
                    translationVectors[i],
                    cameraMatrix,
                    distortionCoefficients,
                )
                error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
                mse += error

            mse = mse / len(objPoints)
            if displayMSE:
                print(f"\nMean reprojection error: {mse}")

            if saveCalibrationParams:
                try:
                    from ..content_loaders import save_calibration

                    print(Fore.GREEN + "\nSaving the calibration parameters...")

                    calibrationParams = {
                        "mse": mse,
                        "rms": rms,
                        "objPoints": [obj.tolist() for obj in objPoints[0]],
                        "imgPoints": [img.tolist() for img in imgPoints[0]],
                        "cameraMatrix": cameraMatrix.tolist(),
                        "distortionCoefficients": distortionCoefficients.tolist(),
                        "rotationVectors": [rvec.tolist() for rvec in rotationVectors],
                        "translationVectors": [tvec.tolist() for tvec in translationVectors],
                    }

                    save_calibration(calibrationParams, calibrationParamsPath)

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
        # Calibrate camera
        ######################################################################################
        # termination criteria for images
        # terminationCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        # objp = np.zeros((10 * 7, 3), np.float32)
        # objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2) * 28.67
        objP = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
        objP[:, :2] = (
            np.mgrid[0 : chessBoardSize[0], 0 : chessBoardSize[1]].T.reshape(-1, 2)
            * squareRealDimensions
        )

        # Arrays to store object points and image points from all the images.
        objPoints = []  # 3d point in real world space
        imgPoints = []  # 2d points in image plane.
        imgSize = None
        chessboardFound = [] # list of images with chessboard detected properly
        chessboardSkipped = []

        for fileName in tqdm(images, desc=Style.RESET_ALL + "Processing images...", dynamic_ncols=True, bar_format="{l_bar}{bar}{r_bar}", colour="green", file=stdout):

            baseFileName = basename(fileName)
            img = cv.imread(fileName)
            grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            if imgSize is None:
                imgSize = grayImg.shape[::-1]

            tqdm.write(Fore.GREEN + f"\nProcessing image '{baseFileName}'.", nolock=True, file=stdout)

            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(
                grayImg, (chessBoardSize[0], chessBoardSize[1]), None
            )

            if not ret:
                tqdm.write(Fore.RED + f"Skipped image '{baseFileName}' because corners were not found.", nolock=True, file=stdout)
                chessboardSkipped.append(baseFileName)
                continue

            tqdm.write(Fore.GREEN + f"Success!", nolock=True, file=stdout)

            chessboardFound.append(baseFileName)
            objPoints.append(objP)

            if improveSubPix:
                corners = cv.cornerSubPix(
                    grayImg, corners, (11, 11), (-1, -1), terminationCriteria
                )

            imgPoints.append(corners)

            if displayFoundCorners:
                # Draw and display the corners
                cv.drawChessboardCorners(
                    img, (chessBoardSize[0], chessBoardSize[1]), corners, ret
                )
                cv.imshow("Current Image", img)
                cv.waitKey(500)

        if not objPoints or not imgPoints:
            raise ValueError("No valid chessboard patterns found in the provided images.")

        # overall RMS re-projection error, camera matrix, distortion coefficients, rotation vectors, translation vectors
        print(Fore.GREEN + "\nCalibrating camera...")
        rms, cameraMatrix, distortionCoefficients, rotationVectors, translationVectors = (
            cv.calibrateCamera(objPoints, imgPoints, imgSize, None, None)
        )

        mse = 0
        for i in range(len(objPoints)):
            imgPoints2, _ = cv.projectPoints(
                objPoints[i],
                rotationVectors[i],
                translationVectors[i],
                cameraMatrix,
                distortionCoefficients,
            )
            error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2) / len(imgPoints2)
            mse += error

        mse = mse / len(objPoints)
        if displayMSE:
            print(f"\nMean reprojection error: {mse}")

        if saveCalibrationParams:
            try:
                from ..content_loaders import save_calibration

                print(Fore.GREEN + "\nSaving the calibration parameters...")

                calibrationParams = {
                    "mse": mse,
                    "rms": rms,
                    "objPoints": [obj.tolist() for obj in objPoints],
                    "imgPoints": [img.tolist() for img in imgPoints],
                    "cameraMatrix": cameraMatrix.tolist(),
                    "distortionCoefficients": distortionCoefficients.tolist(),
                    "rotationVectors": [rvec.tolist() for rvec in rotationVectors],
                    "translationVectors": [tvec.tolist() for tvec in translationVectors],
                }

                save_calibration(calibrationParams, calibrationParamsPath)

            except CalibrationParamsPathNotProvided:
                print(Fore.RED + "\nError occurred while saving the calibration parameters!\n")
                raise

            except Exception as e:
                print(Fore.RED + "\nUnknown error occurred\n")
                raise

    cv.destroyAllWindows()

    if showListOfImagesWithChessboardFound:
        print(Fore.GREEN + "\nList of images with chessboard found:\n")
        print(chessboardFound)
        print(Fore.RED + "\nList of images skipped:\n")
        print(chessboardSkipped)