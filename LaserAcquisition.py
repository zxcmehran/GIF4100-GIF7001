import cv2
import time

print('Calibration. Press and hold (q) to exit\n')
print('Push (p) to start')
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

        for i in range(79):
            time.sleep(0.5)

            retL, frameL = LeftCam.read()
            retR, frameR = RightCam.read()

            cv2.imshow('PictureR', frameL)
            cv2.imshow('PictureL', frameR)

            str_id_image = str(id_image)
            print('Images ' + str_id_image + ' saved for right and left cameras')
            cv2.imwrite('scanR/scan-R' + str_id_image + '.png', frameR)  # Save the image in the file where this Programm is located
            cv2.imwrite('scanL/scan-L' + str_id_image + '.png', frameL)
            id_image += 1
            cv2.destroyWindow('PictureR')
            cv2.destroyWindow('PictureL')
            time.sleep(0.45)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
LeftCam.release()
RightCam.release()
cv2.destroyAllWindows()
