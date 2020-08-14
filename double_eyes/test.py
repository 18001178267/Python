import numpy as np
import cv2

#SGBM函数参数
window_size = 5
min_disp = 17
num_disp = 65 - min_disp
blockSize = window_size
uniquenessRatio = 1
speckleRange = 3
speckleWindowSize = 3
disp12MaxDiff = 200
P1 = 600
P2 = 2400

#读取左图并转为单通道灰度图
imgL = cv2.imread('1.png')
imgLG = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
#读取右图并转为单通道灰度图
imgR = cv2.imread('2.png')
imgRG = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
print(imgL.shape)
#计算视差
stereo = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=num_disp, blockSize=window_size,
                               uniquenessRatio=uniquenessRatio, speckleRange=speckleRange,
                               speckleWindowSize=speckleWindowSize, disp12MaxDiff=disp12MaxDiff, P1=P1, P2=P2)
# stereo = cv2.StereoSGBM_create(minDisparity=1,numDisparities=384, blockSize=11)
# disp = stereo.compute(imgLG, imgRG).astype(np.float32) / 16.0
disp = stereo.compute(imgLG, imgRG)
print(disp[0])
# cv2.imshow("disp1.jpg", disp)

#转换为单通道图片
disp = cv2.normalize(disp, disp, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
#显示并输出图像
print(disp[0])

cv2.imshow("disp2.jpg", disp)
# cv2.imwrite("disp2.jpg", disp)
#等待
cv2.waitKey()
#退出
cv2.destroyAllWindows()
