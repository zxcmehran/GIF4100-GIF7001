from matplotlib import cm
import Calibration
import LaserDotDetection
import cv2
import numpy as np
import matplotlib.pyplot as plt


rejected = 0

a = Calibration.calibration(False)

b = LaserDotDetection.localisation(a[0], a[1], a[2], a[3], False)

points_L = np.array(b[0])  # cv2.UMat(b[0])
points_R = np.array(b[1])  # cv2.UMat(b[1])
stereoL = a[4]  # cv2.UMat(a[5])
stereoR = a[5]  # cv2.UMat(a[4])
R = a[6]
T = a[7]

Point_3d = []
for i in range(2, len(points_L)):
    if (points_R[i][0] != 0 and points_R[i][1] != 0) or (points_L[i][0] != 0 and points_L[i][1] != 0):
        D_points = cv2.triangulatePoints(stereoL, stereoR, points_L[i], points_R[i])
        homo = D_points[3, 0]
        Point_3d.append([D_points[0, 0]/homo, D_points[1, 0]/homo, D_points[2, 0]/homo])
    else:
        rejected += 1

print("Points rejected: ", rejected)
print("Press (q) to quit")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
point_numpy = np.array(Point_3d)
ax.plot_trisurf(point_numpy[:, 0], point_numpy[:, 1], point_numpy[:, 2], cmap=cm.copper.reversed(), linewidth=0.1)
plt.show()

if cv2.waitKey(1) & 0xff == ord('q'):
    cv2.destroyAllWindows()
