import cv2
import numpy as np


image = cv2.imread(r'C:\Users\YFZX\Desktop\Python_code\find_difference\original_img\3_2.jpg')
cv2.imshow('1',image)
image= cv2.resize(image,(400,250))
cv2.imwrite(r'C:\Users\YFZX\Desktop\Python_code\find_difference\original_img\3_2.jpg',image)

