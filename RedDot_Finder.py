import numpy as np
import cv2
import time

background = cv2.createBackgroundSubtractorMOG2()

for i in range(0, 77):
    t = str(i)
    scanR = cv2.imread('scan-R'+t+'.png')    # Right side
    scanL = cv2.imread('scan-L'+t+'.png')    # Left side

    grayL = cv2.cvtColor(scanR, cv2.COLOR_BGR2GRAY)  # grayscale
    grayR = cv2.cvtColor(scanL, cv2.COLOR_BGR2GRAY)  # grayscale
    _, th1 = cv2.threshold(grayR, 240, 255, cv2.THRESH_BINARY)
    fgmask = background.apply(th1)
    print(t)
    cv2.imshow("Cam L", scanR)
    cv2.imshow("Cam R", fgmask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

