import Calibration
import LaserDotDetectionV2
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a = Calibration.calibration(False)

print(a)

b = LaserDotDetectionV2.localisation(a[0], a[1], a[2], a[3], False)
#for i in range(0, len(b[0])):
#    point = []
points_L = np.array(b[0])#cv2.UMat(b[0])
points_R = np.array(b[1])#cv2.UMat(b[1])
stereoL = a[4]#cv2.UMat(a[5])
stereoR = a[5]#cv2.UMat(a[4])
R = a[6]
T = a[7]
#mouvement_matrix = np.array([[R[0,0],R[0,1],R[0,2],T[0,0]],[R[1,0],R[1,1],R[1,2],T[1,0]],[R[2,0],R[2,1],R[2,2],T[2,0]]])
#empty_matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])
#stereoR = np.matmul(stereoR, mouvement_matrix)
#stereoL = np.matmul(stereoL, empty_matrix)
Point_3d = []
for i in range(0, len(points_L)):
    D_points = cv2.triangulatePoints(stereoL,stereoR,points_L[i],points_R[i])
    homo = D_points[3,0]
    Point_3d.append([D_points[0,0]/homo,D_points[1,0]/homo,D_points[2,0]/homo])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
point_numpy = np.array(Point_3d)
ax.scatter(point_numpy[:,0], point_numpy[:,1], point_numpy[:,2])
plt.show()
