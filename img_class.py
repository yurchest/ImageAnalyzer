import imutils
import cv2
from PyQt5.QtGui import QPixmap, QImage
import numpy as np

import glob

class Img():
    def __init__(self, img_path):
        self.img = self.avarage_imgs(img_path)
        self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
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
        # img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        img = self.img
        if show_line:
            cv2.line(img, self.line[0], self.line[1], (119, 201, 200), thickness=3)
        img = imutils.resize(img, width=width, height=height)
        img = QImage(img, img.shape[1], \
                     img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
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

    def avarage_imgs(self, paths):
        # print(cv2.cvtColor(cv2.imread(paths[0]), cv2.COLOR_BGR2GRAY))
        # img = np.zeros(cv2.cvtColor(cv2.imread(paths[0]), cv2.COLOR_BGR2GRAY).shape)
        # print(img)
        # for i in range(img.shape[0]):
        #     sum = img[i]
        #
        #     for path in paths:
        #         # print(len(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)[i]))
        #         sum += cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)[i]
        #     img[i] = np.divide(sum, len(paths))
        #     print(np.divide(sum, len(paths)))
        # print(img.shape)

        # sum = np.zeros(cv2.imread(paths[0]).shape)
        # for path in paths:
        #     sum += cv2.imread(path)

        image_data = cv2.zeroes(cv2.imread(paths).shape[0],cv2.imread(paths).shape[1],cv2.CV_32F)
        for path in paths:
            cv2.accumulate(image_data, cv2.imread(path))
        return image_data/len(paths)


