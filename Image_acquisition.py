import numpy as np
import cv2

print('Calibration. Press and hold (q) to exit\n')
print('Push (s) to save the image and push (c) skip')
id_image = 0

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

LeftCam = cv2.VideoCapture(1)
RightCam = cv2.VideoCapture(2)

while True:
    retL, frameL = LeftCam.read()
    retR, frameR = RightCam.read()
    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)  # grayscale
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)  # grayscale

    retL2, cornersL = cv2.findChessboardCorners(grayL, (9, 6), None)  # Define the number of chess corners (9,6)
    retR2, cornersR = cv2.findChessboardCorners(grayR, (9, 6), None)

    cv2.imshow("Cam L", grayL)
    cv2.imshow("Cam R", grayR)

    if (retR2 == True) & (retL2 == True):
        corners2R = cv2.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        corners2L = cv2.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)

        cv2.drawChessboardCorners(grayR, (9, 6), corners2R, retR2)
        cv2.drawChessboardCorners(grayL, (9, 6), corners2L, retL2)
        cv2.imshow('VideoR', grayR)
        cv2.imshow('VideoL', grayL)

        if cv2.waitKey(0) & 0xFF == ord('s'):  # Push "s" to save the images and "c" if you don't want to
            str_id_image = str(id_image)
            print('Images ' + str_id_image + ' saved for right and left cameras')
            cv2.imwrite('chessboard-R' + str_id_image + '.png', frameR)  # Save the image in the file where this Programm is located
            cv2.imwrite('chessboard-L' + str_id_image + '.png', frameL)
            id_image += 1
            cv2.destroyWindow('VideoR')
            cv2.destroyWindow('VideoL')
        else:
            print('Images not saved')
            cv2.destroyWindow('VideoR')
            cv2.destroyWindow('VideoL')


    if cv2.waitKey(1) & 0xff == ord('q'):
        break
LeftCam.release()
RightCam.release()
cv2.destroyWindow()