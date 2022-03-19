import cv2
import numpy as np


def init_image(img_path):
    img = cv2.imread(img_path)

    img = cv2.svtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img, 100, 100)

    kernel = np.ones((5, 5), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)

    cv2.imshow('aboba', img)
    cv2.waitkey(0)
