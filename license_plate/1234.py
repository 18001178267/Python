import cv2
import numpy as np
from cv2.cv2 import GaussianBlur

img = cv2.imread('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\1.png')

roi = img[:,300:400]  #截取100行到200行，列为300到400列的整块区域
cv2.imshow("image", roi)
cv2.waitKey(0)
