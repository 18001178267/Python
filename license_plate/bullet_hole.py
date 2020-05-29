import cv2
import numpy as np
from cv2.cv2 import GaussianBlur

image = cv2.imread('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\bullet_hole_5.jpg')
output=image.copy()
#print(image.shape)
cv2.namedWindow('demo', 0)

#cv2.imshow("image", image)

#hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#cv2.imshow("hsv", hsv_img)

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
#cv2.imshow("gray", gray_img)
gauss=cv2.GaussianBlur(gray_img,(9,9),0)
#cv2.imshow("Gauss", gauss)

ret, thresh = cv2.threshold(gauss, 120, 255, cv2.THRESH_BINARY) # 阈值分割
cv2.imshow("thresh0",thresh )

#sobel = cv2.Sobel(thresh, cv2.CV_8U, 1, 1, ksize=1) #对原始灰度图进行边缘检测，初步筛选出包含车牌位置的若干个区域
#cv2.imshow("sobel", sobel)

kernel_erode = np.ones((2,2), np.uint8)
erode = cv2.erode(thresh, kernel_erode,iterations=5)
#cv2.imshow("erode", erode)

canny=cv2.Canny(erode, 200, 300)
cv2.imshow("canny", canny)

#sobel_2 = cv2.Sobel(erode, cv2.CV_8U, 1, 1, ksize=1) #对原始灰度图进行边缘检测，初步筛选出包含车牌位置的若干个区域
#cv2.imshow("sobel_2", sobel_2)

#kernel_dilate = np.ones((2,2), np.uint8)
#dilate = cv2.dilate(sobel_2, kernel_dilate, iterations=2)
#cv2.imshow("dilate", dilate)
'''
circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT,1,60,param1=50,param2=1,minRadius=1,maxRadius=5)
print(circles.shape[1])
a = "Total: "+str(circles.shape[1])
'''

'''
if circles is not None:
    # 将圆(x, y)坐标和半径转换成int
    circles = np.round(circles[0, :]).astype('int')
    for (x, y, r) in circles:
        # 绘制圆和半径矩形到output
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x-5, y-5), (x+5, y+5), (0, 128, 255), -1)

    cv2.imshow('output', np.hstack([image, output]))
'''
contours, hier = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #只检测外轮廓，即轮廓不分级
#print(contours[0].shape)
print(np.size(contours))
draw_coutours=cv2.drawContours(image,contours,-1,(0,0,255),3)
#cv2.putText(image,a , (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 3)
cv2.imshow("Result",draw_coutours)
#cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\' + 'Result2.jpg',draw_coutours)
num=0
for c in contours:
    # find bounding box coordinates
    # 现计算出一个简单的边界框
    x, y, w, h = cv2.boundingRect(c) # 将轮廓信息转换成(x, y)坐标，并加上矩形的高度和宽度
    circle_x= int((x+w)/2)
    circle_y= int((y+h)/2)
    circle_r= int(w/2)
    #print(x,y,w,h)
    if  h >30 or w>30 or float(h/w)>1.3 or float(w/h)>1.3 or  h < 10 or w< 10 :
        continue
    #cv2.imwrite('con'+str(index)+'.jpg', result[y:y+h, x:x+w])
    cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2) # 画出矩形
    num=num+1
    print(num)
    #cv2.circle(output, (circle_x, circle_y),circle_r, (0, 255, 0), 4)             # 画出圆形
    #print(x,y,w,h)
    #target = image[y:y+h, x:x+w]
    #target_gray = cv2.cvtColor(target.copy(), cv2.COLOR_BGR2GRAY) # 灰度图
    #cv2.imshow("target_gray",target_gray)
    #ret, thresh = cv2.threshold(target_gray, 160, 255, cv2.THRESH_BINARY) # 阈值分割
    #contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(new,contours,-1,(0,255,0),3)
a = "Total: "+ str(num)
cv2.putText(output,a, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), 3)
cv2.imshow("Result",output)
#cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\' + 'Result5.jpg',output)

cv2.waitKey(0)