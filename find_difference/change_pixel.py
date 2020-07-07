import cv2
import numpy as np


image = cv2.imread(r'C:\Users\YFZX\Desktop\Python_code\find_difference\original_img\2_1.jpg')
cv2.imshow('1',image)
image= cv2.resize(image,(400,300))
cv2.imwrite(r'C:\Users\YFZX\Desktop\Python_code\find_difference\original_img\2_1.jpg',image)

