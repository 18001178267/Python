import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #Dshow的作用????????????????????
i = 0
winname="capture"
while (1):
    ret, frame = cap.read()
    cv2.imshow(winname, frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    elif k == ord('s'):
        cv2.imwrite('C:\\Users\\YFZX\\Desktop\\Python_code\\double_eyes\\' + str(i) + '.jpg', frame)
        i += 1
cap.release()
cv2.destroyAllWindows()