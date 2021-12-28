from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
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

        self.main_window.show()

    def get_file_name_button(self):
        self.get_file_name()
        self.show_image()

    def get_file_name(self):
        self.path_img, _ = QFileDialog.getOpenFileName(self.main_window, 'Выберите файл', './',
                                                       'Image Files(*.bmp)')
        self.w_root.label_2.setText(self.path_img)

    def show_image(self):
        self.pixmap = QPixmap(self.path_img)
        self.pixmap = self.pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
        self.w_root.label_3.setPixmap(self.pixmap)

    def button2_clicked(self):
        try:
            self.calculations()
            functions.write_in_file(self.line_with_max_brightness[2], self.xy[0], self.xy[1])
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
            self.calculations()
            functions.show_plt(self.xy[0], self.xy[1])
        except:
            pass

    def calculations(self):
        img = Image.open(self.path_img)
        self.line_with_max_brightness = functions.line_with_max_brightness(img)
        self.xy = functions.get_x_y(self.line_with_max_brightness[0], self.line_with_max_brightness[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
