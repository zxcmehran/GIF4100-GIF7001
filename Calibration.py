import numpy as np
import cv2

def calibration(isDebug = False):
    imgDirL = 'calibrationL2/'
    imgDirR = 'calibrationR2/'

    # isDebug = True

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Square dimension
    calibrationsquaredimension = 26

    # Prepare object points
    objp = np.zeros((9*6, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2) * calibrationsquaredimension

    # Arrays to store object points and image points from all images
    objpoints = []   # 3d points in real world space
    imgpointsR = []   # 2d points in image plane
    imgpointsL = []

    # Start calibration from the camera
    print('Reading calibration samples for the 2 cameras... ')
    # Call all saved images
    for i in range(0, 101):   # Number of calibration pics
        t = str(i)
        ChessImaR = cv2.imread(imgDirR+'chessboard-R'+t+'.png', 0)    # Right side
        ChessImaL = cv2.imread(imgDirL+'chessboard-L'+t+'.png', 0)    # Left side
        retR, cornersR = cv2.findChessboardCorners(ChessImaR, (9, 6), None)  # chees corners we are looking for
        retL, cornersL = cv2.findChessboardCorners(ChessImaL, (9, 6), None)  # Left side
        if (True == retR) & (True == retL):
            objpoints.append(objp)
            corners2R = cv2.cornerSubPix(ChessImaR, cornersR, (11, 11), (-1, -1), criteria)
            corners2L = cv2.cornerSubPix(ChessImaL, cornersL, (11, 11), (-1, -1), criteria)
            imgpointsR.append(corners2R)
            imgpointsL.append(corners2L)

    print('Calibrating camera R')
    # Determine the new values for different parameters
    #   Right Side
    retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, ChessImaR.shape[::-1], None, None)
    hR, wR = ChessImaR.shape[:2]
    #newcameramtxR, roiR = cv2.getOptimalNewCameraMatrix(mtxR, distR, (wR, hR), 1, (wR, hR))

    print('Calibrating camera L')
    #   Left Side
    retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, ChessImaL.shape[::-1], None, None)
    hL, wL = ChessImaL.shape[:2]
    #newcameramtxL, roiL = cv2.getOptimalNewCameraMatrix(mtxL, distL, (wL, hL), 1, (wL, hL))

    print('Starting the stereoCalibrate...')

    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC

    retS, MLS, dLS, MRS, dRS, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, mtxL, distL, mtxR, distR,
                                                              ChessImaR.shape[::-1], criteria_stereo, flags)
    print('Starting the stereoRectify...')
    rectify_scale = 0
    RL, RR, PL, PR, Q, roiL, roiR = cv2.stereoRectify(MLS, dLS, MRS, dRS, ChessImaR.shape[::-1], R, T, rectify_scale, (0, 0))

    print('Starting undistortion...')
    # Rectification and Lens distortion correction at the same time
    LStereoMapX, LStereoMapY = cv2.initUndistortRectifyMap(MLS, dLS, RL, PL, ChessImaR.shape[::-1], cv2.CV_16SC2)
    RStereoMapX, RStereoMapY = cv2.initUndistortRectifyMap(MRS, dRS, RR, PR, ChessImaR.shape[::-1], cv2.CV_16SC2)

    # draw an example
    if isDebug:
        left_rectified = cv2.remap(ChessImaL, LStereoMapX, LStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        right_rectified = cv2.remap(ChessImaR, RStereoMapX, RStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        cv2.imshow('left', left_rectified)
        cv2.imshow('right', right_rectified)

        print('Intrinsic cameraL matrix\n', MLS, '\n')
        print('DistorsionL matrix\n', dLS, '\n')
        print('Intrinsic cameraR matrix\n', MRS, '\n')
        print('DistorsionR matrix\n', dRS, '\n')

        print('R\n', R, '\n')  # Rotation matrix
        print('T\n', T, '\n')  # Translation matrix
        print('E\n', E, '\n')  # Essential matrix
        print('F\n', F, '\n')  # Fundamental matrix

        cv2.waitKey(0)

    return [LStereoMapX, LStereoMapY, RStereoMapX, RStereoMapY, PL, PR, R, T]
