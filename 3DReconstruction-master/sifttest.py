#!/usr/bin/env python3
# -*- coding:utf-8 -*-
u'''
Created on 2020年7月14日
@author: YFZX
'''
__author__ = 'YFZX'
__version__ = '1.0.0'
__company__ = u'773'
__updated__ = '2020-07-20'
import numpy as np
from matplotlib import pyplot as plt
# from imagedt.decorator import time_cost
import cv2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

print('cv version: ', cv2.__version__)

def test_deal(m1):
    # m2=m1.reshape(-1,4)
    m2=m1.T
    # print(m2)
    m3=[]
    for each in m2:
        each_line=list(map(lambda x:float(x),each))
        m3.append(each_line)
    m4=np.array(m3)
    # print(m4)
    #列表解析x,y,z的坐标
    x=[k[0] for k in m4]
    y=[k[1] for k in m4]
    z=[k[2] for k in m4]
    #开始绘图
    fig=plt.figure(dpi=120)
    ax=fig.add_subplot(111,projection='3d')
    #标题
    plt.title('point cloud')
    #利用xyz的值，生成每个点的相应坐标（x,y,z）
    ax.scatter(x,y,z,c='r',marker='.',s=2,linewidth=0,alpha=1,cmap='spectral')
    # ax.axis('scaled')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    #显示
    plt.show()

def deal(p1,s_I,p2,r_I):
    p1_3d = []
    p2_3d = []
    p1_4d = []
    p2_4d = []
    for p in p1:
        p = [p[0],p[1],0]
        p1_3d.append(p)

    for p in p1_3d:
        x = np.dot(s_I,p)
        p1_4d.append(x)

    for p in p2:
        p = [p[0],p[1],1]
        p2_3d.append(p)

    for p in p2_3d:
        x = np.dot(r_I,p)
        p2_4d.append(x)

    p1_4d = np.array(p1_4d)
    p2_4d = np.array(p2_4d)
    p1_4d = p1_4d.reshape(len(p1_4d),-1)
    p2_4d = p2_4d.reshape(len(p2_4d),-1)
    print(p1_4d,'\n',p2_4d)
    # # print(m4)
    #列表解析x,y,z的坐标
    x=[k[0] for k in p2_4d]
    y=[k[1] for k in p2_4d]
    z=[k[2] for k in p2_4d]
    # print(x)
    # for k in p1_4d:
    #     x.append(float(k[0]))
    #     y.append(float(k[1]))
    #     z.append(float(k[2]))
    # print(x)
    #开始绘图
    fig=plt.figure(dpi=120)
    ax=fig.add_subplot(111,projection='3d')
    #标题
    plt.title('point cloud')
    #利用xyz的值，生成每个点的相应坐标（x,y,z）
    ax.scatter(x,y,z,c='b',marker='.',s=2,linewidth=0,alpha=1,cmap='spectral')
    # ax.axis('scaled')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    #显示
    plt.show()

def bgr_rgb(img):
    (r, g, b) = cv2.split(img)
    return cv2.merge([b, g, r])

def orb_detect(image_a, image_b):
    # feature match
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(image_a, None)
    kp2, des2 = orb.detectAndCompute(image_b, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1, des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # Draw first 10 matches.
    img3 = cv2.drawMatches(image_a, kp1, image_b, kp2,
                           matches[:100], None, flags=2)
    return bgr_rgb(img3)

def sift_detect(img1, img2, detector='surf'):
    if detector.startswith('si'):
        print("sift detector......")
        sift = cv2.xfeatures2d_SIFT().create()
    else:
        print("surf detector......")
        sift = cv2.xfeatures2d.SURF_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # img3 = cv2.drawKeypoints(image_a,kp1,image_a,color=(255,0,255)) #画出特征点，并显示为红色圆圈 ；此处输入输出图像作同名处理
    # plt.imshow(bgr_rgb(img3))

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # Apply ratio test
    good = []
    p1 = []
    p2 = []
    for m, n in matches:
        if m.distance < 0.5 * n.distance:
            good.append([m])
            p1.append(kp1[m.queryIdx].pt)
            p2.append(kp2[m.trainIdx].pt)
    p1 = np.array(p1)
    p2 = np.array(p2)
    # print(p1.shape)
    # good = [[m] for m, n in matches if m.distance < 0.5 * n.distance]
    # print(len(good))
    # for _ in range(len(kp1)):
    #     p1.append(kp1[_].pt)
    # for _ in range(len(kp2)):
    #     p2.append(kp2[_].pt)
    # p1 = np.array(p1)
    # p2 = np.array(p2)
    print('有效特征点个数：',len(p1))

    # cv2.drawMatchesKnn expects list of lists as matches.
    match_img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    plt.imshow(bgr_rgb(match_img))

    # Read camera parameters
    K = np.load('./Calibration/camera_params/K.npy')
    Focal = np.load('./Calibration/camera_params/FocalLength.npy')
    pp_x = float("{:.2f}".format(K[0][2]))
    pp_y = float("{:.2f}".format(K[1][2]))
    # E, mask = cv2.findEssentialMat(p1, p2, focal=F, pp=(pp_x,pp_y), method=cv2.RANSAC, prob=0.999, threshold=1.0)
    # F, mask = cv2.findFundamentalMat(p1, p2, cv2.RANSAC)
    # E1 = K.T * F * K

    E, mask = cv2.findEssentialMat(p1, p2, focal=Focal,pp=(pp_x,pp_y), method=cv2.RANSAC, prob=0.999, threshold=1.0)
    # print(E1,'\n',E)
    _, R, T, mask = cv2.recoverPose(E, p1, p2, focal=Focal, pp=(pp_x,pp_y))
    # print(np.linalg.det(R))
    # print(R,T)
    # Trianglepoints
    standard = np.mat(np.eye(3,3,dtype=float))
    standard_zero = np.mat(np.zeros((3,1),dtype= float))
    standard = np.hstack((standard,standard_zero))
    reference = np.mat(np.hstack((R,T)))
    s_I= standard.I
    r_I=reference.I
    # print(p1.shape,standard,reference)
    # print(reference,'\n',r_I,'\n',np.dot(reference,r_I))
    point4d = cv2.triangulatePoints(standard,reference,p1.T,p2.T)
    # print(p1.shape,point4d.shape)
    test_deal(point4d)

    # deal(p1,s_I,p2,r_I)

    # BFMatcher with default params
    return bgr_rgb(match_img)

if __name__ == "__main__":
    # load image
    image_a = cv2.imread('11.png')#绝对路径
    image_b = cv2.imread('22.png')
    # ORB
    # img = orb_detect(image_a, image_b)
    # SIFT or SURF
    img = sift_detect(image_a, image_b)
    # plt.imshow(img)
    plt.show()
