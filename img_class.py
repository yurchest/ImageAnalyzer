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
        return  np.argmax(self.img.sum(axis=1))


    def avarage_imgs(self, paths: list):

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




