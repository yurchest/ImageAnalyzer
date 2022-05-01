import imutils
import cv2
from PyQt5.QtGui import QPixmap, QImage

class Img():
    def __init__(self, img_path):
        self.img = cv2.imread(img_path)
        print(type(self.img))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
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

    def get_line(self):
        return self.img[self.line[0][1]]


    def get_pixmap_img(self):
        img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
        cv2.line(img, self.line[0], self.line[1], (119, 201, 200), thickness=3)
        img = imutils.resize(img, width=500, height=500)
        img = QImage(img, img.shape[1], \
                     img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
        pix = QPixmap(img)
        return pix
