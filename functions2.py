from PyQt5.QtGui import QPixmap, QImage
import cv2
import imutils
import numpy as np
from main4 import App
import os
from ctypes import *


def init_image(img_path):
    img = cv2.imread(img_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.Canny(img, 21, 12)

    # kernel = np.ones((5, 5), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)

    img = imutils.resize(img, width=500, height=500)
    cv2.imshow('aboba', img)


class Img(App):
    def __init__(self, img_path):
        path = os.path.join(os.getcwd(), 'func.so')
        self.cpp_functions = CDLL(path)
        self.img = cv2.imread(img_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        print(self.img.shape)
        self.line = [[0, self.img.shape[0] // 2], [self.img.shape[1], self.img.shape[0] // 2]]

    def get_pixmap_update_img(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        cv2.line(img, self.line[0], self.line[1], (119, 201, 200), thickness=3)
        img = imutils.resize(img, width=500, height=500)

        img = QImage(img, img.shape[1], \
                     img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap(img)
        return pix
        cv2.imshow('aboba', img)

    def get_max_line_bright(self):

        pass

    def get_current_line(self):
        index_max = self.cpp_functions.index_max_in_array(self.img[self.line[0][1]], len(self.img[self.line[0][1]]))
        x = self.cpp_functions.get_x(self.img[self.line[0][1]], index_max,len(self.img[self.line[0][1]]))
        print(x)
        return (x, self.img[self.line[0][1]])

    def line_up(self):
        if self.line[0][1] > 0:
            self.line[0][1] -= 1
            self.line[1][1] -= 1


    def line_down(self):
        if self.line[0][1] < self.img.shape[0]:
            self.line[0][1] += 1
            self.line[1][1] += 1
