import cv2
import numpy as np
from cv2.cv2 import GaussianBlur

image = cv2.imread('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\soil_2.jpg')
output=image.copy()
#print(image.shape)
#cv2.imshow("image", image)
#hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#cv2.imshow("hsv", hsv_img)

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
#cv2.imshow("gray", gray_img)
gauss=cv2.GaussianBlur(gray_img,(5,5),0)
#cv2.imshow("Gauss", gauss)

ret, thresh = cv2.threshold(gauss, 70, 255, cv2.THRESH_BINARY) # 阈值分割
#cv2.imshow("thresh0",thresh )

#sobel = cv2.Sobel(thresh, cv2.CV_8U, 1, 1, ksize=1) #对原始灰度图进行边缘检测，初步筛选出包含车牌位置的若干个区域
#cv2.imshow("sobel", sobel)


kernel_dilate = np.ones((5,5), np.uint8)
dilate = cv2.dilate(thresh, kernel_dilate, iterations=1)
#cv2.imshow("dilate", dilate)
'''

'''
canny=cv2.Canny(dilate, 200, 300)
cv2.imshow("canny", canny)


kernel_dilate = np.ones((5,5), np.uint8)
dilate = cv2.dilate(canny, kernel_dilate, iterations=2)
#cv2.imshow("dilate2", dilate)

#sobel_2 = cv2.Sobel(erode, cv2.CV_8U, 1, 1, ksize=1) #对原始灰度图进行边缘检测，初步筛选出包含车牌位置的若干个区域
#cv2.imshow("sobel_2", sobel_2)

#kernel_dilate = np.ones((2,2), np.uint8)
#dilate = cv2.dilate(sobel_2, kernel_dilate, iterations=2)
#cv2.imshow("dilate", dilate)
'''
circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT,1,60,param1=50,param2=1,minRadius=1,maxRadius=5)
print(circles)
if circles is not None:
    # 将圆(x, y)坐标和半径转换成int
    circles = np.round(circles[0, :]).astype('int')
    for (x, y, r) in circles:
        # 绘制圆和半径矩形到output
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x-5, y-5), (x+5, y+5), (0, 128, 255), -1)

    cv2.imshow('output', np.hstack([image, output]))
'''
contours, hier = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #只检测外轮廓，即轮廓不分级
#print(contours[0].shape)
a=np.size(contours)
draw_coutours=cv2.drawContours(image,contours,-1,(0,0,255),3)
#cv2.putText(image,a , (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 3)


a = "Total: "+ str(a)
cv2.putText(draw_coutours,a, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 3)
cv2.imshow("Result",draw_coutours)
#cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\' + 'soil_detect.jpg',draw_coutours)

cv2.waitKey(0)