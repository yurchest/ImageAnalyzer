from PyQt5.QtGui import QPixmap, QImage
import cv2
import imutils
import numpy as np
from main4 import App
import os
from ctypes import *
from ctypes import cdll


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
        path = os.path.join(os.getcwd(), 'lib.so')
        self.cpp_functions = CDLL(path, winmode=1)
        self.img = cv2.imread(img_path)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        print(self.img.shape)
        self.line = [[0, self.img.shape[0] // 2], [self.img.shape[1], self.img.shape[0] // 2]]

    def get_pixmap_update_img(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        cv2.line(img, self.line[0], self.line[1], (119, 201, 200), thickness=3)
        img = imutils.resize(img, width=500, height=500)
        # cv2.imshow('aboba', img)
        img = QImage(img, img.shape[1], \
                     img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap(img)

        return pix

    def get_max_line_bright(self):
        max_sum = 0
        for index_line, line in enumerate(self.img):
            array = (c_short * len(line))(*line)
            cur_sum = self.cpp_functions.sum_in_array(byref(array), len(line))
            if cur_sum > max_sum:
                max_sum = cur_sum
                max_sum_index = index_line
        return max_sum_index

    def get_current_line(self):
        # self.cpp_functions.index_max_in_array.restype = c_short
        len_arr = len(self.img[self.line[0][1]])
        self.cpp_functions.index_max_in_array.argtypes = [POINTER(c_short * len_arr), c_int]
        array = (c_short * len_arr)(*self.img[self.line[0][1]])
        index_max = self.cpp_functions.index_max_in_array(byref(array), len_arr)
        x = np.empty(len_arr, dtype=c_short)
        array_x = (c_short * len_arr)(*x)
        self.cpp_functions.get_x(byref(array_x), array, len_arr, index_max)
        self.x = list(array_x)
        return [list(array_x), list(self.img[self.line[0][1]])]

    def line_up(self):
        if self.line[0][1] > 0:
            self.line[0][1] -= 1
            self.line[1][1] -= 1

    def line_down(self):
        if self.line[0][1] < self.img.shape[0]:
            self.line[0][1] += 1
            self.line[1][1] += 1

    def set_line(self, line):
        if (self.line[0][1] < self.img.shape[0] and self.line[0][1] > 0):
            self.line[0][1] = line
            self.line[1][1] = line

    def recalc_x_with_ugl_size(self, ugl_size):
        len_arr = len(self.x)
        array = (c_float * len_arr)(*self.x)
        self.cpp_functions.recalc_x_ugl_size(array, len_arr, c_float(ugl_size))
        return list(array)

# g++ -c -fPIC .\func_cpp.cpp -o foo.o
# g++ -shared -Wl,-soname,libfoo.so -o libfoo.so  foo.o
