from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from form import *
import functions
import sys
import os
from PIL import Image


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_window = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.main_window)
        self.main_window.setWindowTitle('IMG Analyzer')

        self.w_root.pushButton.clicked.connect(self.get_file_name_button)

        self.w_root.pushButton_2.clicked.connect(self.button2_clicked)
        self.w_root.pushButton_3.clicked.connect(self.button3_clicked)
        self.w_root.pushButton_4.clicked.connect(self.button4_clicked)





        self.main_window.show()

    def get_file_name_button(self):
        self.get_file_name()
        self.show_image()
        self.draw_line(self.line_with_max_brightness[1])



    def get_file_name(self):
        self.path_img, _ = QFileDialog.getOpenFileName(self.main_window, 'Выберите файл', './',
                                                       'Image Files(*.bmp)')
        self.w_root.label_2.setText(self.path_img)
        self.calculations()

    def show_image(self):
        self.pixmap = QPixmap(self.path_img)
        # self.w_root.label_3.resize(self.pixmap.width(), self.pixmap.height())
        self.pixmap = self.pixmap.scaled(500, 500 ,QtCore.Qt.KeepAspectRatio)
        self.w_root.label_3.setPixmap(self.pixmap)

    def draw_line(self, pos):
        self.pixmap = QPixmap(self.path_img)

        qp = QPainter(self.pixmap)
        pen = QPen(Qt.blue, 2)
        qp.setPen(pen)
        qp.drawLine(self.pixmap.width(), pos, 0, pos)
        qp.end()
        self.pixmap = self.pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        self.w_root.label_3.setPixmap(self.pixmap)


    def button2_clicked(self):
        try:
            functions.write_in_file(self.line_with_max_brightness[2], self.x, self.y)
            self.w_root.label_4.setText('Готово')
            try:
                self.timer.stop()
            except:
                pass
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.delete_label)
            self.timer.start(2000)
        except:
            pass

    def delete_label(self):
        self.w_root.label_4.setText('')


    def button3_clicked(self):
        try:
            functions.show_plt\
                (self.x, self.y)
        except:
            pass

    def button4_clicked(self):

        try:
            self.x = functions.get_x_y(self.line_with_max_brightness[0], self.line_with_max_brightness[1])[0]
            self.y = functions.get_x_y(self.line_with_max_brightness[0], self.line_with_max_brightness[1])[1]
            pixel_ugl_size = float(self.w_root.lineEdit.text())
            self.w_root.label_7.setText(str(pixel_ugl_size))
            for i in range(len(self.x)):
                self.x[i] = float(self.x[i]) / pixel_ugl_size
                print(self.x[i])
            print('YES')
        except:
            self.w_root.label_7.setText('ERROR')
            print('ERR')
            pass

    def calculations(self):
        img = Image.open(self.path_img)
        self.line_with_max_brightness = functions.line_with_max_brightness(img)
        self.xy \
            = functions.get_x_y(self.line_with_max_brightness[0], self.line_with_max_brightness[1])
        self.x = self.xy[0]
        self.y = self.xy[1]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()



## 16.289 количество пикселей в одной угловой секунде (угловой размер пикселя)
## от максимума минус и плюс