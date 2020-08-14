'''
Created by Omar Padierna "Para11ax" on Jan 1 2019

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

'''


import cv2
import numpy as np 
import glob
from tqdm import tqdm
import PIL.ExifTags
import PIL.Image

#============================================
# Camera calibration
#============================================

#Define size of chessboard target. 

chessboard_size = (7,5)

#Define arrays to save detected points
obj_points = [] #3D points in real world space 
img_points = [] #2D points in image plane

#Prepare grid and points to display

objp = np.zeros((np.prod(chessboard_size),3),dtype=np.float32)   #(7*5,3)


objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1,2)

#read images

calibration_paths = glob.glob('C:/Users/YFZX/Desktop/Python_code/3DReconstruction-master/Calibration/calibration_images/*')
# calibration_paths = glob.glob('./test_image/*')


#Iterate over images to find intrinsic matrix
for image_path in tqdm(calibration_paths):
	#Load image
	image = cv2.imread(image_path)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	print("Image loaded, Analizying...")
	#find chessboard corners
	ret,corners = cv2.findChessboardCorners(gray_image, chessboard_size, None)
	# cv2.drawChessboardCorners(image,chessboard_size,corners,True)
	# corners = corners.reshape(-1,2)
	# for point in corners:
	# 	cv2.circle(image, tuple(point),10,(0,0,255),10)
	# print(corners)
	if ret == True:
		print("Chessboard detected!")
		print(image_path)
		#define criteria for subpixel accuracy
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		#refine corner location (to subpixel accuracy) based on criteria.
		cv2.cornerSubPix(gray_image, corners, (5,5), (-1,-1), criteria)
		obj_points.append(objp)
		img_points.append(corners)
		# print(obj_points,img_points)
	# image1 = image.copy()
	# for point in corners:
	# 	cv2.circle(image1, tuple(point),10,(0,0,255),10)
	# print(corners)


#Calibrate camera
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,gray_image.shape[::-1], None, None)
#摄像机矩阵（K）、畸变系数（dist）、旋转和平移矢量（rvecs和tvecs）#
print(ret,K,rvecs)
#Save parameters into numpy file
np.save("./camera_params/ret", ret)
np.save("./camera_params/K", K)
np.save("./camera_params/dist", dist)
np.save("./camera_params/rvecs", rvecs)
np.save("./camera_params/tvecs", tvecs)

#Get exif data in order to get focal length.
exif_img = PIL.Image.open(calibration_paths[0])

exif_data = {
	PIL.ExifTags.TAGS[k]:v
	for k, v in exif_img._getexif().items()
	if k in PIL.ExifTags.TAGS}

#Get focal length in tuple form
focal_length_exif = exif_data['FocalLength']

#Get focal length in decimal form
focal_length = focal_length_exif[0]/focal_length_exif[1]
#Save focal length
np.save("./camera_params/FocalLength", focal_length)

#Calculate projection error. 
mean_error = 0
for i in range(len(obj_points)):
	img_points2, _ = cv2.projectPoints(obj_points[i],rvecs[i],tvecs[i], K, dist)  #透视图转成俯视图，3D to 2D
	# print(img_points2,img_points2.shape)
	# print(img_points2,len(img_points2),img_points2.shape)
	error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2)/len(img_points2)
	mean_error += error

total_error = mean_error/len(obj_points)
print (total_error)
