import cv2
import numpy as np
from cv2.cv2 import GaussianBlur

image = cv2.imread('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\1.png')
#cv2.imshow("image", image)
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY )
#cv2.imshow("gray", gray_img)
gauss=cv2.GaussianBlur(gray_img,(5,5),0)
#cv2.imshow("Gauss", gauss)

#roi_img  = np.zeros(image.shape[0:2],dtype=np.uint8)
#print(type(roi_img))

'''
ret, thresh = cv2.threshold(gray_img, 10, 255, cv2.THRESH_BINARY) # 阈值分割
cv2.imshow("thresh0",gray_img )
'''
sobel = cv2.Sobel(gray_img, cv2.CV_8U, 1, 0, ksize=1) #对原始灰度图进行边缘检测，初步筛选出包含车牌位置的若干个区域
#cv2.imshow("sobel", sobel)

ret, thresh = cv2.threshold(sobel, 30, 255, cv2.THRESH_BINARY) # 二值分割
#cv2.imshow("thresh",thresh )
#print(thresh.shape)

kernel_erode = np.ones((2,2), np.uint8)
erode = cv2.erode(thresh, kernel_erode,iterations=2)
#cv2.imshow("erode", erode)

kernel_dilate = np.ones((10,10), np.uint8)
dilate = cv2.dilate(erode, kernel_dilate, iterations=3)
#cv2.imshow("dilate", dilate)

contours, hier = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
draw_coutours=cv2.drawContours(image,contours,-1,(0,0,255),3)
#cv2.imshow("1",draw_coutours)
for c in contours:
    # find bounding box coordinates
    # 现计算出一个简单的边界框
    x, y, w, h = cv2.boundingRect(c) # 将轮廓信息转换成(x, y)坐标，并加上矩形的高度和宽度
    if w < 2.9*h:
        continue
    #cv2.imwrite('con'+str(index)+'.jpg', result[y:y+h, x:x+w])
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) # 画出矩形
    target = image[y:y+h, x:x+w]
    target_gray = cv2.cvtColor(target.copy(), cv2.COLOR_BGR2GRAY) # 灰度图
    #cv2.imshow("target_gray",target_gray)
    #ret, thresh = cv2.threshold(target_gray, 160, 255, cv2.THRESH_BINARY) # 阈值分割
    #contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(new,contours,-1,(0,255,0),3)
    #cv2.imshow("new",new)

ret2,th2 = cv2.threshold(target_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#ret2,th2 = cv2.threshold(target_gray,100,255,cv2.THRESH_BINARY)

#print(th2.shape)
th2_copy=th2.copy()
cv2.imshow("target",th2_copy)
#cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\target.jpg',th2)

height = th2_copy.shape[0]
width = th2_copy.shape[1]
a = [0 for z in range(0, width)]
for x in range(0,width): #遍历一列
    for y in range(0,height):  #遍历一行
        if  th2_copy[y,x]==255:  #如果改点为bai
            a[x] += 1  #该列的计数器加一计数
            th2_copy[y,x]=0  #记录完后将其变为hei色
    #print (x)

#cv2.imshow("1",th2_copy)
#
for x  in range(0,width):  #遍历每一列
    for y in range((height-a[x]),height):  #从该列应该变黑的最顶部的点开始向最底部涂bai
        th2_copy[y,x]=255   #涂bai
cv2.imshow("touying",th2_copy)


#截取并正确筛选每个车牌字符
index = 0
cut_x=0
cut_length=0
for i in range(0,width):
    if a[i] < 14:
         if cut_length > 13.0:
            #print(cut_length,"goal")
            ROI= target[:,cut_x:(cut_x+cut_length)]
            #print(type(ROI))
            #cv2.imshow("result",ROI)
            #cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\license_plate\\' + 'plate'+str(index)+'.jpg',ROI)
            cut_x=0
            cut_length=0
            index += 1
         else:
            cut_x=0
            cut_length=0
    else :
        cut_length += 1
        if cut_x == 0:
            cut_x = i
        else:
            pass

cv2.waitKey(0)