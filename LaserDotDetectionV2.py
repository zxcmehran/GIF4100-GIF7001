# A simple code that filters the image using color to get a mask
# Detects blobs of the desired color
# Finds the most dominant one
# determines the center coordinates
#
# The calibration is not applied to the images.
# The algorithm does not necessarily find the brightest spot of the laser dot.
# Check image 7-Right. Maybe an adjustment on mask color ranges helps.

import sys
import imutils
import numpy as np
import cv2


imgDirL = 'scanL/'
imgDirR = 'scanR/'
colorForMask = 'red'

isDebug = True
background = cv2.createBackgroundSubtractorMOG2()

def getPointCoordinates(img, color):


    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th1 = cv2.threshold(imgHSV, 240, 255, cv2.THRESH_BINARY)
    mask = background.apply(th1)


    # Filter reflections from door handle


    if isDebug:
        cv2.imshow('not_cleaned_mask', mask)


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


# Implement green or other colors if needed
def getRedMask(imgHSV):
    # Mask 1 H:0-10
    mask0 = cv2.inRange(imgHSV, np.array([0, 50, 50]), np.array([10, 255, 255]))

    # Mask 2 H:170-180
    mask1 = cv2.inRange(imgHSV, np.array([170, 50, 50]), np.array([180, 255, 255]))

    return mask0 + mask1



print('Finding Red dot coordinates for 2 cameras... ')
# Call all saved images
for i in range(0, 77):
    t = str(i)
    ChessImaR = cv2.imread(imgDirR+'scan-R'+t+'.png')    # Right side
    ChessImaL = cv2.imread(imgDirL+'scan-L'+t+'.png')    # Left side

    centroidsR = getPointCoordinates(ChessImaR, colorForMask)
    print(t+' Right')

    for itemF in centroidsR:
        item = itemF.astype(int)
        cv2.drawMarker(ChessImaR, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                       markerSize=40, thickness=2, line_type=cv2.LINE_AA)

    cv2.imshow('Detection', ChessImaR)

    cv2.waitKey(0)

    centroidsL = getPointCoordinates(ChessImaL, colorForMask)
    print(t + ' Left')

    for itemF in centroidsL:
        item = itemF.astype(int)
        cv2.drawMarker(ChessImaL, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                       markerSize=40, thickness=2, line_type=cv2.LINE_AA)

    cv2.imshow('Detection', ChessImaL)

    cv2.waitKey(0)
