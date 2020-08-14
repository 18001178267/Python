import cv2
import pyzed.sl as sl
import time
import numpy as np

def load_image_into_numpy_array(image):
    ar = image.get_data()
    ar = ar[:, :, 0:3]
    (im_height, im_width, channels) = image.get_data().shape
    return np.array(ar).reshape((im_height, im_width, 3)).astype(np.uint8)

def test(leftimg,rightimg):
# top, bot, left, right = 100, 100, 0, 500
    top, bot, left, right = 10, 10, 10, 10
    # img1 = cv2.imread('1.jpg')
    # img2 = cv2.imread('2.jpg')
    srcImg = cv2.copyMakeBorder(leftimg, top, bot, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    testImg = cv2.copyMakeBorder(rightimg, top, bot, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    print(srcImg.shape)
    # cv2.imshow('1',srcImg)
    # cv2.imshow('2',testImg)
    img1gray = cv2.cvtColor(srcImg, cv2.COLOR_BGR2GRAY)
    img2gray = cv2.cvtColor(testImg, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d_SIFT().create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1gray, None)
    kp2, des2 = sift.detectAndCompute(img2gray, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    good = []
    pts1 = []
    pts2 = []
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=0)
    img3 = cv2.drawMatchesKnn(img1gray, kp1, img2gray, kp2, matches, None, **draw_params)
    # plt.imshow(img3, ), plt.show()

    rows, cols = srcImg.shape[:2]
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        warpImg = cv2.warpPerspective(testImg, np.array(M), (testImg.shape[1], testImg.shape[0]), flags=cv2.WARP_INVERSE_MAP)

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
        res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        print(res.shape)
        # show the result
        # plt.figure()
        # plt.imshow(res)
        # plt.show()
        # cv2.imshow('result',res)
        # cv2.waitKey(0)
        return res
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matchesMask = None

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

while not exit_signal:
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(left_image_mat, sl.VIEW.LEFT, resolution=image_size)
        zed.retrieve_image(right_image_mat, sl.VIEW.RIGHT, resolution=image_size)
        # print(left_image_mat.get_data())
        left_image = load_image_into_numpy_array(left_image_mat)
        right_image = load_image_into_numpy_array(right_image_mat)
        # print(left_image)
        cv2.imshow("ZED-L", left_image)
        cv2.imshow("ZED-R", right_image)
        # cv2.imshow("ZED-L", left_image_mat.get_data())
        # cv2.imshow("ZED-R", right_image_mat.get_data())

        # final = test(left_image,right_image)
        # cv2.imshow("Fusion", final)

        # print(image_mat,image_mat.get_data(),type(image_mat.get_data()))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit_signal = True
