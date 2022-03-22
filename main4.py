from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from form import *
from functions2 import *
from functions import write_in_file, show_plt
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
        self.w_root.pushButton_2.clicked.connect(self.button2_clicked)
        self.w_root.pushButton_3.clicked.connect(self.button3_clicked)
        self.w_root.pushButton_4.clicked.connect(self.button4_clicked)
        self.w_root.pushButton_7.clicked.connect(self.button7_clicked)
        self.w_root.pushButton_5.clicked.connect(self.button5_clicked)
        self.w_root.pushButton_6.clicked.connect(self.button6_clicked)

        self.file_opened = False

        self.main_window.show()

    def open_file(self):
        try:
            if self.get_file_name():
                self.w_root.label_2.setText(self.path_img)
                self.Img1 = Img(self.path_img)
                self.pixel_ugl_size = 1
                self.update_image()
                self.line = self.Img1.get_current_line()
                # self.x = [i for i in range(len(self.line))]
                self.file_opened = True
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Не удалось отрыть файл.\n Попробуйте использовать путь только на латинице \n\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)", options=options)
        if self.path_img:
            return self.path_img

    def update_image(self):
        self.w_root.label_3.setPixmap(self.Img1.get_pixmap_update_img())

    def button5_clicked(self):
        if self.file_opened:
            self.Img1.line_up()
            self.w_root.statusbar.showMessage("Обработка ... ")
            self.update_image()
            self.line = self.Img1.get_current_line()
            self.w_root.statusbar.showMessage("Готово ", 100)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def button6_clicked(self):
        if self.file_opened:
            self.Img1.line_down()
            self.w_root.statusbar.showMessage("Обработка ... ")
            self.update_image()
            self.line = self.Img1.get_current_line()
            self.w_root.statusbar.showMessage("Готово ", 100)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def button2_clicked(self):
        try:
            if self.file_opened:
                self.w_root.statusbar.showMessage("Обработка ... ")
                self.line[0] = self.Img1.recalc_x_with_ugl_size(self.pixel_ugl_size)
                write_in_file(self.line[0], self.line[1], self.pixel_ugl_size)
                done = QMessageBox()
                done.setWindowTitle("Информация")
                done.setText("Успешно записано в файл       ")
                done.exec()
                self.w_root.statusbar.showMessage("Готово ", 1500)
            else:
                self.w_root.statusbar.showMessage("Файл не открыт ", 1500)
        except Exception as err:
            self.w_root.label_7.setText('ERROR')
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Ошибка записи в файл\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()
            self.w_root.statusbar.showMessage("Ошибка записи в файл    ........" + str(err), 2000)

    def button4_clicked(self):
        if self.file_opened:
            try:
                self.w_root.statusbar.showMessage("Обработка ... ")
                self.pixel_ugl_size = float(self.w_root.lineEdit.text())
                self.line[0] = self.Img1.recalc_x_with_ugl_size(self.pixel_ugl_size)
                self.w_root.label_7.setText(str(self.pixel_ugl_size))
                self.w_root.statusbar.showMessage("Готово ", 1500)
            except Exception as err:
                self.w_root.label_7.setText('ERROR')
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Ошибка задания углового размера пикселя\n" + str(err))
                error.setIcon(QMessageBox.Information)
                error.exec()
                self.w_root.statusbar.showMessage("Ошибка задания углового размера пикселя", 2000)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def button3_clicked(self):
        if self.file_opened:
            try:
                self.w_root.statusbar.showMessage("Обработка ... ")
                self.line[0] = self.Img1.recalc_x_with_ugl_size(self.pixel_ugl_size)
                show_plt \
                    (self.line[0], self.line[1])
                self.w_root.statusbar.showMessage("Готово ", 1500)
            except Exception as err:
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Ошибка построения графика\n" + str(err))
                error.setIcon(QMessageBox.Information)
                error.exec()
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def button7_clicked(self):
        if self.file_opened:
            self.w_root.statusbar.showMessage("Обработка ... ")
            line_with_max_bright = self.Img1.get_max_line_bright()
            print(line_with_max_bright)
            self.Img1.set_line(line_with_max_bright)
            self.update_image()
            self.line = self.Img1.get_current_line()
            self.w_root.statusbar.showMessage("Готово ", 1500)

        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
