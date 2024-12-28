import cv2
from cv2 import aruco
from tqdm import tqdm # progress bar

def find_aruco_dict(imgPath) -> None:
    ARUCO_DICT = {
        "DICT_4X4_50": aruco.DICT_4X4_50,
        "DICT_4X4_100": aruco.DICT_4X4_100,
        "DICT_4X4_250": aruco.DICT_4X4_250,
        "DICT_4X4_1000": aruco.DICT_4X4_1000,
        "DICT_5X5_50": aruco.DICT_5X5_50,
        "DICT_5X5_100": aruco.DICT_5X5_100,
        "DICT_5X5_250": aruco.DICT_5X5_250,
        "DICT_5X5_1000": aruco.DICT_5X5_1000,
        "DICT_6X6_50": aruco.DICT_6X6_50,
        "DICT_6X6_100": aruco.DICT_6X6_100,
        "DICT_6X6_250": aruco.DICT_6X6_250,
        "DICT_6X6_1000": aruco.DICT_6X6_1000,
        "DICT_7X7_50": aruco.DICT_7X7_50,
        "DICT_7X7_100": aruco.DICT_7X7_100,
        "DICT_7X7_250": aruco.DICT_7X7_250,
        "DICT_7X7_1000": aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": aruco.DICT_APRILTAG_36h11
    }
    tqdm.write("[INFO] loading image...", nolock=True)
    image = cv2.imread(imgPath)
    dictsFound = []
    # loop over the types of ArUco dictionaries
    for arucoName, arucoDict in tqdm(ARUCO_DICT.items(), desc="Processing ArUco dictionaries...", dynamic_ncols=True, bar_format="{l_bar}{bar}{r_bar}", colour="green"):
        # load the ArUCo dictionary, grab the ArUCo parameters, and attempt to detect the markers for the current dictionary
        arucoDict = aruco.getPredefinedDictionary(arucoDict)
        arucoParams = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(arucoDict, arucoParams)
        (corners, ids, rejected) = detector.detectMarkers(image)
        # if at least one ArUco marker was detected display the ArUco name to our terminal
        if len(corners) > 0:
            dictsFound.append("[INFO] detected {} markers for '{}'".format(
                len(corners), arucoName))
            # tqdm.write("[INFO] detected {} markers for '{}'".format(len(corners), arucoName), nolock=True)

    for dictFound in dictsFound:
        tqdm.write(dictFound, nolock=True)