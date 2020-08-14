import numpy as np
import cv2 as cv
import time
from matplotlib import pyplot as plt
import datetime
import pyzed.sl as sl

def load_image_into_numpy_array(image):
    ar = image.get_data()
    ar = ar[:, :, 0:3]
    (im_height, im_width, channels) = image.get_data().shape
    return np.array(ar).reshape((im_height, im_width, 3)).astype(np.uint8)

def downsample_image(image, reduce_factor):
	for i in range(0,reduce_factor):
		#Check if image is color or grayscale
		if len(image.shape) > 2:
			row,col = image.shape[:2]
		else:
			row,col = image.shape

		image = cv.pyrDown(image, dstsize= (col//2, row // 2))
	return image

def attach_homo(left_image,right_image):
    left_image = np.array(left_image)
    right_image = np.array(right_image)
    # cv.imshow('src',left_image)
    # cv.imshow('warp',right_image)
    top, bot, left, right = 100, 100, 150, 150
    srcImg = cv.copyMakeBorder(left_image, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    testImg = cv.copyMakeBorder(right_image, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    img1gray = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
    img2gray = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)

    img1gray = downsample_image(img1gray,1)
    img2gray = downsample_image(img2gray,1)

    sift = cv.xfeatures2d_SIFT().create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1gray, None)
    kp2, des2 = sift.detectAndCompute(img2gray, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

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
    # print(matches)
    img3 = cv.drawMatchesKnn(img1gray, kp1, img2gray, kp2, matches, None, **draw_params)
    # cv.imshow('drawmatch',img3)
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        print(M)
        np.save("zed_M", M)


def realtime_stitch():
    pass


if __name__ == '__main__':
    width = 704  #1056
    height = 416 #624
    exit_signal = False

    zed = sl.Camera()
    # Create a InitParameters object and set configuration parameters
    input_type = sl.InputType()

    init_params = sl.InitParameters(input_t=input_type)
    init_params.camera_resolution = sl.RESOLUTION.HD720
    init_params.camera_fps = 30
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init_params.coordinate_units = sl.UNIT.METER
    init_params.svo_real_time_mode = False

    # Open the camera
    status = zed.open(init_params)
    print(status)
    time.sleep(1)

    left_image_mat  = sl.Mat()
    right_image_mat = sl.Mat()

    runtime_parameters = sl.RuntimeParameters()
    image_size = sl.Resolution(width, height)

    # 获取一帧图像求解单应性矩阵
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(left_image_mat, sl.VIEW.LEFT, resolution=image_size)
        zed.retrieve_image(right_image_mat, sl.VIEW.RIGHT, resolution=image_size)
        left_image = load_image_into_numpy_array(left_image_mat)
        right_image = load_image_into_numpy_array(right_image_mat)
        # cv.imshow('1',left_image)
        # cv.imshow('2',right_image)
        attach_homo(left_image,right_image)
    print('对齐完毕')

    while not exit_signal:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(left_image_mat, sl.VIEW.LEFT, resolution=image_size)
            zed.retrieve_image(right_image_mat, sl.VIEW.RIGHT, resolution=image_size)
            left_image_1 = load_image_into_numpy_array(left_image_mat)
            right_image_1 = load_image_into_numpy_array(right_image_mat)
            M= np.load("zed_M.npy")
            top, bot, left, right = 100, 100, 150, 150
            srcImg = cv.copyMakeBorder(left_image_1, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
            testImg = cv.copyMakeBorder(right_image_1, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
            # img1gray = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
            # img2gray = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
            rows, cols = srcImg.shape[:2]
            warpImg = cv.warpPerspective(testImg, np.array(M), (testImg.shape[1], testImg.shape[0]), flags=cv.WARP_INVERSE_MAP)

            for col in range(0, cols):
                if srcImg[:, col].any() or warpImg[:, col].any():
                    left = col
                    break
            for col in range(cols-1, 0, -1):
                if srcImg[:, col].any() or warpImg[:, col].any():
                    right = col
                    break
            res = np.zeros([rows, cols, 3], np.uint8)
            for col in range(0, cols):
                    srcImgLen = float(abs(col - left))
                    testImgLen = float(abs(col - right))
                    alpha = srcImgLen / (srcImgLen + testImgLen)
                    res[:, col] = np.clip(srcImg[:, col] * (1-alpha) + warpImg[:, col] * alpha, 0, 255)
            # opencv is bgr, matplotlib is rgb
            # res = cv.cvtColor(res, cv.COLOR_BGR2RGB)
            cv.imshow("ZED-L", left_image_1)
            cv.imshow("ZED-R", right_image_1)
            cv.imshow('res',res)
            if cv.waitKey(10) & 0xFF == ord('q'):
                cv.destroyAllWindows()
                exit_signal = True