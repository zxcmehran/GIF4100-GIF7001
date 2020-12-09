# 3D Reconstruction using Stereopsis camera 
Semester project of Computer Vision course (GIF4100-GIF7001).

The **main.py** file calls the calibration and laser dot detection functions. Given the calibration and scene scanning image sets, you will need to run this file only.  

Additionally, the files **CalibrationAcquisition.py** and **LaserAcquisition.py** can be used to capture calibration and laser scan image sets respectively.

Image sets contain multiple shots of a checkerboard calibration target, and a set of images having a red laser pointer scanning through the scene. Please note to re-adjust the details in **Calibration.py** file if you are going to use another calibration target. After calibrating the cameras and detecting the laser points, a triangulation is done to reconstruct the scene.
   