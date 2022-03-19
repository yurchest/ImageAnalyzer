from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from form import *
import functions2
import sys
import os


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_window = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.main_window)
        self.main_window.setWindowTitle('IMG Analyzer')

        self.w_root.pushButton.clicked.connect(self.open_file)
        # self.w_root.pushButton_2.clicked.connect(self.button2_clicked)
        # self.w_root.pushButton_3.clicked.connect(self.button3_clicked)
        # self.w_root.pushButton_4.clicked.connect(self.button4_clicked)
        # self.w_root.pushButton_7.clicked.connect(self.button7_clicked)
        # self.w_root.pushButton_5.clicked.connect(self.button5_clicked)
        # self.w_root.pushButton_6.clicked.connect(self.button6_clicked)


        self.main_window.show()

    def open_file(self):
        if self.get_file_name():
            self.w_root.label_2.setText(self.path_img)
            functions2.init_image(self.path_img)


    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                  "Image Files(*.bmp);;All Files (*)", options=options)
        if self.path_img:
            return self.path_img







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
