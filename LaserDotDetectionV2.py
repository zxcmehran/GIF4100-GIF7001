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

def getPointCoordinates(img, background, isDebug = False):


    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th1 = cv2.threshold(imgHSV, 240, 255, cv2.THRESH_BINARY)
    mask = background.apply(th1)

    if isDebug:
        cv2.imshow('th', th1)
        cv2.imshow('mask', mask)


    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    cc = len(cnts)

    # Find dominant blob
    maxcntSize=0
    if cc != 0:
        for cnt in cnts:
            if len(cnt) > maxcntSize:
                maxcntSize = len(cnt)
                biggestCnt = cnt


            # Find blob center

        M = cv2.moments(biggestCnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return np.array([[cX, cY]])
        else:
            return np.array([[0, 0]])
    else:
        return np.array([[0, 0]])


def localisation(LStereoMapX, LStereoMapY, RStereoMapX, RStereoMapY, isDebug = False):

    background = cv2.createBackgroundSubtractorMOG2()

    imgDirL = 'scanL2/'
    imgDirR = 'scanR2/'

    pointsL = []
    pointsR = []

    print('Finding Red dot coordinates for 2 cameras... ')
    # Call all saved images
    for i in range(2, 236):
        t = str(i)

        ChessImaR = cv2.imread(imgDirR+'scan-R'+t+'.png')    # Right side
        ChessImaL = cv2.imread(imgDirL+'scan-L'+t+'.png')    # Left side

        ChessImaR = cv2.remap(ChessImaR, RStereoMapX, RStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        ChessImaL = cv2.remap(ChessImaL, LStereoMapX, LStereoMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        centroidsR = getPointCoordinates(ChessImaR, background, False)

        for itemF in centroidsR:
            item = itemF.astype(int)
            cv2.drawMarker(ChessImaR, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            pointsR.append(np.array([[item[0]],[item[1]]],dtype=np.float))

        if isDebug:
            cv2.imshow('Detection', ChessImaR)

            cv2.waitKey(0)

        centroidsL = getPointCoordinates(ChessImaL, background, False)

        for itemF in centroidsL:
            item = itemF.astype(int)
            cv2.drawMarker(ChessImaL, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            pointsL.append(np.array([[item[0]],[item[1]]],dtype=np.float))

        if isDebug:
            cv2.imshow('Detection', ChessImaL)

            cv2.waitKey(0)

    return [pointsL, pointsR]
