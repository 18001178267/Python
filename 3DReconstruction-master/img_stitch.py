import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape

		image = cv.pyrDown(image, dstsize= (col//2, row // 2))
	return image

if __name__ == '__main__':
    # top, bot, left, right = 100, 100, 0, 500
    top, bot, left, right = 50, 50, 100, 100
    img1 = cv.imread('1.png')
    img2 = cv.imread('2.png')
    srcImg = cv.copyMakeBorder(img1, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    testImg = cv.copyMakeBorder(img2, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    # cv.imshow('1',srcImg)
    # cv.imshow('2',testImg)
    img1gray = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
    img2gray = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    # test = cv.resize(img1gray,(int(img1gray.shape[1]/4),int(img1gray.shape[0]/4)))
    # img1gray= downsample_image(img1gray,2)
    # img2gray= downsample_image(img2gray,2)
    # cv.imshow('1111',test)
    sift = cv.xfeatures2d_SIFT().create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1gray, None)
    kp2, des2 = sift.detectAndCompute(img2gray, None)
    # FLANN parameters
    # FLANN_INDEX_KDTREE = 1
    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)
    # flann = cv.FlannBasedMatcher(index_params, search_params)
    # matches = flann.knnMatch(des1, des2, k=2)
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    good = []
    pts1 = []
    pts2 = []
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.5*n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=0)
    img3 = cv.drawMatchesKnn(img1gray, kp1, img2gray, kp2, matches, None, **draw_params)
    # cv.namedWindow('match',0)
    # cv.resizeWindow('match',800,600)
    # cv.imshow('match',img3)

    rows, cols = srcImg.shape[:2]
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good])
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])
        # M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        M, mask = cv.findHomography(np.float32(pts1),np.float32(pts2), cv.RANSAC, 3.0)
        print(M,mask,sum(mask))
        # print(M,len(good),len(mask))
        # warpImg = cv.warpPerspective(srcImg, np.array(M), (testImg.shape[1], testImg.shape[0]), flags=cv.WARP_INVERSE_MAP)
        warpImg = cv.warpPerspective(srcImg, np.array(M), (testImg.shape[1], testImg.shape[0]))

        cv.imshow('123',warpImg)
        # cv.imshow('2',testImg)
        for col in range(0, cols):
            if srcImg[:, col].any() and warpImg[:, col].any():
                left = col
                break
        for col in range(cols-1, 0, -1):
            if srcImg[:, col].any() and warpImg[:, col].any():
                right = col
                break

        res = np.zeros([rows, cols, 3], np.uint8)
        for row in range(0, rows):
            for col in range(0, cols):
                if not srcImg[row, col].any():
                    res[row, col] = warpImg[row, col]
                elif not warpImg[row, col].any():
                    res[row, col] = srcImg[row, col]
                else:
                    srcImgLen = float(abs(col - left))
                    testImgLen = float(abs(col - right))
                    alpha = srcImgLen / (srcImgLen + testImgLen)
                    res[row, col] = np.clip(srcImg[row, col] * (1-alpha) + warpImg[row, col] * alpha, 0, 255)

        # opencv is bgr, matplotlib is rgb
        res = cv.cvtColor(res, cv.COLOR_BGR2RGB)
        print(res.shape)
        # show the result
        # plt.figure()
        # plt.imshow(res)
        # plt.show()
        cv.namedWindow('result',0)
        cv.resizeWindow('result',800,600)
        cv.imshow('result',res)
        cv.waitKey(0)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matchesMask = None