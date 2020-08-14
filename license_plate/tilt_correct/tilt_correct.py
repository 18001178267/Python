import numpy as np
import cv2

## 图片旋转
def rotate_bound(image, angle):
    #获取宽高
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    print(cX,cY)
    # 提取旋转矩阵 sin cos
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    print(M)
    # 计算图像的新边界尺寸
    nW = int((h * sin) + (w * cos))
#     nH = int((h * cos) + (w * sin))
    nH = h

    # 调整旋转矩阵
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    print(M)

    return cv2.warpAffine(image, M, (nW, nH),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # return cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

## 获取图片旋转角度
def get_minAreaRect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    cv2.imshow("gray", gray)

    # thresh = cv2.threshold(gray, 0, 255,
    #     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.threshold(gray, 0, 255,type=cv2.THRESH_OTSU)[1]
    cv2.imshow("th", thresh)
    # print(thresh[18][43])
    coords = np.column_stack(np.where(thresh > 0))      #np.where返回两个array，第一个是高度行，第二个是宽度列
                                                        #np.column_stack作用：列不变，行拼接，输出像素值255（白）的像素坐标
    # print(coords,np.where(thresh > 0))
    a = cv2.minAreaRect(coords)
    print(cv2.minAreaRect(coords))
    print(cv2.boxPoints(a))
    return a

image_path = "54321.png"
image = cv2.imread(image_path)
angle = get_minAreaRect(image)[-1]
rotated = rotate_bound(image, angle)

cv2.putText(rotated, "angle: {:.2f} ".format(angle),
    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# show the output image
print("[INFO] angle: {:.3f}".format(angle),image.shape,rotated.shape)
# cv2.imshow("imput", image)
cv2.imshow("output", rotated)
cv2.waitKey(0)