import Calibration
import LaserDotDetectionV2

a = Calibration.calibration(True)

b = LaserDotDetectionV2.localisation(a[0], a[1], a[2], a[3], True)

print(a)
print(b)
print("number of points in left image : " + len(b[0]))
print("number of points in right image : " + len(b[1]))


