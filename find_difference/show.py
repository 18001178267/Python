import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse

imga= cv2.imread('original_img/2_2.jpg',0)
imgb= cv2.imread('original_img/2_1.jpg',0)
cv2.imshow('1_2',imga)
cv2.imshow('1_1',imgb)
cv2.waitKey(0)

