import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse

def matchAB(fileA, fileB):
    # 读取图像数据
    imgA = cv2.imread(fileA)
    imgB = cv2.imread(fileB)

    # 转换成灰色
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 获取图片A的大小
    height, width = grayA.shape
    # print(grayA.shape)
    # 取局部图像，寻找匹配位置
    result_window = np.zeros((height, width), dtype=imgA.dtype)
    for start_y in range(0, height-900, 10):
        for start_x in range(0, width-900, 10):
            window = grayA[start_y:start_y+900, start_x:start_x+900]
            match = cv2.matchTemplate(grayB, window, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(match)
            matched_window = grayB[max_loc[1]:max_loc[1]+900, max_loc[0]:max_loc[0]+900]
            result = cv2.absdiff(window, matched_window)                                    # 重点！
            result_window[start_y:start_y+900, start_x:start_x+900] = result
    cv2.namedWindow('aaa',0)
    cv2.resizeWindow('aaa',800,600)
    cv2.imshow('aaa',result_window)
    # 用四边形圈出不同部分
    _, result_window_bin = cv2.threshold(result_window, 118, 255, cv2.THRESH_BINARY)
    # cv2.imshow('1',result_window_bin)
    i_,contours, _ = cv2.findContours(result_window_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #第一个参数是寻找轮廓的图像，但是有什么用呢？
    # cv2.imshow('a',i_)
    imgC = imgA.copy()
    for contour in contours:
        min = np.nanmin(contour, 0)  #    x, y, w, h = cv2.boundingRect(c)
        max = np.nanmax(contour, 0)
        loc1 = (min[0][0], min[0][1])
        loc2 = (max[0][0], max[0][1])
        if int((max[0][0]-min[0][0])<16) or int((max[0][1]-min[0][1])<5):
            continue
        cv2.rectangle(imgC, loc1, loc2, 255, 2)

    plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)), plt.title('A'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)), plt.title('Answer'), plt.xticks([]), plt.yticks([])
    plt.show()
    cv2.waitKey(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_image',
        type=str,
        default='original_img/1111.jpg',
        help='source image'
    )

    parser.add_argument(
        '--target_image',
        type=str,
        default='original_img/2222.jpg',
        help='target image'
    )

    FLAGS, unparsed = parser.parse_known_args()

    matchAB(FLAGS.source_image, FLAGS.target_image)