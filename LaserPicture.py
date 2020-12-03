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


    cv2.imshow("Cam L", frameL)
    cv2.imshow("Cam R", frameR)

    if cv2.waitKey(1) & 0xFF == ord('p'):

        cv2.imshow('PictureR', frameR)
        cv2.imshow('PictureL', frameL)

        if cv2.waitKey(0) & 0xFF == ord('s'):  # Push "s" to save the images and "c" if you don't want to
            str_id_image = str(id_image)
            print('Images ' + str_id_image + ' saved for right and left cameras')
            cv2.imwrite('scan-R' + str_id_image + '.png', frameR)  # Save the image in the file where this Programm is located
            cv2.imwrite('scan-L' + str_id_image + '.png', frameL)
            id_image += 1
            cv2.destroyWindow('PictureR')
            cv2.destroyWindow('PictureL')
        else:
            print('Images not saved')
            cv2.destroyWindow('PictureR')
            cv2.destroyWindow('PictureL')

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
LeftCam.release()
RightCam.release()
cv2.destroyWindow()