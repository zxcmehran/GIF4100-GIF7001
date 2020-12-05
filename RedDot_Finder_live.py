import numpy as np
import cv2
import time


LeftCam = cv2.VideoCapture(1)
backgroundL = cv2.createBackgroundSubtractorMOG2()
RightCam = cv2.VideoCapture(2)
backgroundR = cv2.createBackgroundSubtractorMOG2()


while True:
    retL, frameL = LeftCam.read()
    retR, frameR = RightCam.read()
    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)  # grayscale
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)  # grayscale
    _, thL = cv2.threshold(grayL, 240, 255, cv2.THRESH_BINARY)
    _, thR = cv2.threshold(grayR, 240, 255, cv2.THRESH_BINARY)
    fgmaskL = backgroundL.apply(thL)
    fgmaskR = backgroundR.apply(thR)
    cv2.imshow("Cam Left", grayL)
    cv2.imshow("Mask L", fgmaskL)
    cv2.imshow("Cam Right", grayR)
    cv2.imshow("Mask R", fgmaskR)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
LeftCam.release()
RightCam.release()
cv2.destroyAllWindows()
