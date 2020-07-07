# USAGE
# python image_diff.py --first original_img/2_1.jpg  --second original_img/2_2.jpg
# python image_diff.py --first original_img/modified_01.png  --second original_img/original_01.png

# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
	help="first input image")
ap.add_argument("-s", "--second", required=True,
	help="second")
args = vars(ap.parse_args())

# load the two input images
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# show the output images
cv2.namedWindow('Original', 0)
cv2.resizeWindow('Original', 800, 600)
cv2.imshow("Original", imageA)
cv2.namedWindow('Modified', 0)
cv2.resizeWindow('Modified', 800, 600)
cv2.imshow("Modified", imageB)
cv2.namedWindow('Diff', 0)
cv2.resizeWindow('Diff', 800, 600)
cv2.imshow("Diff", diff)
cv2.namedWindow('Thresh', 0)
cv2.resizeWindow('Thresh', 800, 600)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)