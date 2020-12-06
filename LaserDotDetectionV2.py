# Detects blobs of the desired color using background subtractor
# Finds the most dominant one
# determines the center coordinates
#
# The calibration is not applied to the images.
# The first two pictures fail to detect the laser.
# This can be fixed by including the first picture from the scene without laser pointer.

import imutils
import numpy as np
import cv2

def getPointCoordinates(img, isDebug = False):

    background = cv2.createBackgroundSubtractorMOG2()

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th1 = cv2.threshold(imgHSV, 240, 255, cv2.THRESH_BINARY)
    mask = background.apply(th1)

    if isDebug:
        cv2.imshow('th', th1)
        cv2.imshow('mask', mask)


    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)

    # Find dominant blob
    maxcntSize=0
    for cnt in cnts:
        if len(cnt) > maxcntSize:
            maxcntSize = len(cnt)
            biggestCnt = cnt

    # Find blob center
    M = cv2.moments(biggestCnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return np.array([[cX, cY]])

    # Not good, gives a lot of points
    # connectivity = 4
    # output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
    #
    # centroids = output[3][1:]
    # return centroids

def localisation(LStereoMapX, LStereoMapY, RStereoMapX, RStereoMapY, isDebug = False):

    imgDirL = 'scanL/'
    imgDirR = 'scanR/'

    pointsL = []
    pointsR = []

    print('Finding Red dot coordinates for 2 cameras... ')
    # Call all saved images
    for i in range(0, 77):
        t = str(i)

        ChessImaR = cv2.imread(imgDirR+'scan-R'+t+'.png')    # Right side
        ChessImaL = cv2.imread(imgDirL+'scan-L'+t+'.png')    # Left side

        ChessImaR = cv2.remap(ChessImaR, RStereoMapX, RStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        ChessImaL = cv2.remap(ChessImaL, LStereoMapX, LStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)


        centroidsR = getPointCoordinates(ChessImaR, True)
        print(t+' Right')

        for itemF in centroidsR:
            item = itemF.astype(int)
            cv2.drawMarker(ChessImaR, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            pointsR.append((item[0],item[1]))

        cv2.imshow('Detection', ChessImaR)

        cv2.waitKey(0)

        centroidsL = getPointCoordinates(ChessImaL)
        print(t + ' Left')

        for itemF in centroidsL:
            item = itemF.astype(int)
            cv2.drawMarker(ChessImaL, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            pointsL.append((item[0],item[1]))

        cv2.imshow('Detection', ChessImaL)

        cv2.waitKey(0)

    return [pointsL, pointsR]
