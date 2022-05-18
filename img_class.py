# -*- encoding: utf-8 -*-
import imutils
import cv2
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PIL import Image

import glob


class Img():
    def __init__(self, img_path):
        self.img = self.avarage_imgs(img_path)
        # self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        self.line = [[0, self.img.shape[0] // 2], [self.img.shape[1], self.img.shape[0] // 2]]


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

    def get_line(self, index=0):
        if index == 0:
            index = self.line[0][1]
        return self.img[index]


    def get_pixmap_img(self,width,height,show_line=True):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        # img = self.img
        # cv2.imshow('Gray image', img)
        if show_line:
            cv2.line(img, self.line[0], self.line[1], (119, 201, 200), thickness=3)
        img = imutils.resize(img, width=width, height=height)
        img = QImage(img, img.shape[1], \
                     img.shape[0],img.shape[1]*3, QImage.Format_RGB888 )
        pix = QPixmap(img)
        return pix

    def get_max_line_bright(self):
        max_sum = 0
        for index_line, line in enumerate(self.img):
            cur_sum = np.sum(line)
            if cur_sum > max_sum:
                max_sum = cur_sum
                index = index_line
        return index

    def avarage_imgs(self, paths: list):

        # number_of_lines, len_of_line = cv2.imread(paths[0]).shape[0], cv2.imread(paths[0]).shape[1]
        # print(number_of_lines, len_of_line)
        # result_img = np.zeros((number_of_lines, len_of_line), dtype=np.uint8)

        # for i in range(number_of_lines):
        #     sum_line = [0.0]*len_of_line
        #     for path in paths:
        #         cur_img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
        #         sum_line += (cur_img[i] // len(paths))
        #     result_img[i] = sum_line
        

        imgs = []
        for path in paths:
            f = open(path, "rb")
            chunk = f.read()
            chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
            img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
            print(path)
            imgs.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        result_img = np.mean(np.array(imgs), axis=0).astype(np.uint8)
        return result_img




