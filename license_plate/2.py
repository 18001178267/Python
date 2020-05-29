import cv2
import numpy as np
image = cv2.imread('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\1.png')
cv2.imshow("image", image)
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )

lower = np.array([110, 100, 150])
upper = np.array([125, 200, 255])
mask = cv2.inRange(hsv_img, lowerb=lower, upperb=upper)
cv2.imshow("mask", mask)
kernel = np.ones((5,5), np.uint8)
mask2 = cv2.dilate(mask, kernel, iterations=10)
cv2.imshow("mask2", mask2)

final=cv2.add(gray,gray,mask=mask2)
cv2.imshow("final", final)

contours, hierarchy = cv2.findContours(final,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)    # 输出为三个参数
cv2.drawContours(gray,contours,-1,(0,0,255),3)

cv2.imshow("img", gray)

cv2.waitKey()