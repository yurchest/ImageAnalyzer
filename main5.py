import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QButtonGroup, QVBoxLayout
from form import *
import sys
from img_class import Img
import numpy as np
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_window = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.main_window)
        self.main_window.setWindowTitle('IMG Analyzer')
        self.init_plot_widget()

        self.pushButtonGroup = QButtonGroup(self)
        self.w_root.choose_file_button.clicked.connect(self.open_file_show_img_plt)
        self.pushButtonGroup.addButton(self.w_root.find_centre_button)
        self.pushButtonGroup.addButton(self.w_root.line_up_button)
        self.pushButtonGroup.addButton(self.w_root.line_down_button)
        self.pushButtonGroup.addButton(self.w_root.set_uglsize_button)
        self.pushButtonGroup.addButton(self.w_root.write_file_button)
        self.pushButtonGroup.buttonClicked.connect(self.button_clicked)
        self.pushButtonGroup.buttonClicked.connect(self.update_image)
        self.pushButtonGroup.buttonClicked.connect(self.update_plot)



        self.main_window.show()

        self.file_opened = False
        self.pixel_ugl_size = 1
        self.w_root.label_7.setText(str(self.pixel_ugl_size))

    def open_file_show_img_plt(self):
        try:
            path = self.get_file_name()
            self.Img1 = Img(path)
            self.w_root.label_2.setText(path)
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText(
                "Не удалось отрыть файл.\n Попробуйте использовать имя файла и путь к нему только на латинице \n\n" + str(
                    err))
            error.setIcon(QMessageBox.Information)
            error.exec()
        try:
            self.update_image()
            self.file_opened = True
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText(
                "Не удалось вывести изображение.\n\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()

        try:
            self.update_plot()
        except Exception as err:
            raise
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText(
                "Не удалось обновить график.\n\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()

    def button_clicked(self, button):
        if self.file_opened:
            if button == self.w_root.line_up_button:
                self.Img1.line_up()
            elif button == self.w_root.line_down_button:
                self.Img1.line_down()

            elif button == self.w_root.set_uglsize_button:
                try:
                    self.pixel_ugl_size = float(self.w_root.lineEdit.text())
                    self.w_root.label_7.setText(str(self.pixel_ugl_size))
                except Exception as err:
                    self.w_root.label_7.setText('ERROR')
                    error = QMessageBox()
                    error.setWindowTitle("Ошибка")
                    error.setText("Ошибка задания углового размера пикселя\n" + str(err))
                    error.setIcon(QMessageBox.Information)
                    error.exec()
                    self.w_root.statusbar.showMessage("Ошибка задания углового размера пикселя", 2000)
            elif button == self.w_root.write_file_button:
                try:
                    self.write_in_file()
                    done = QMessageBox()
                    done.setWindowTitle("Информация")
                    done.setText("Успешно записано в файл       ")
                    done.exec()
                    self.w_root.statusbar.showMessage("Готово ", 1500)
                except Exception as err:
                    self.w_root.label_7.setText('ERROR')
                    error = QMessageBox()
                    error.setWindowTitle("Ошибка")
                    error.setText("Ошибка записи в файл\n" + str(err))
                    error.setIcon(QMessageBox.Information)
                    error.exec()
                    self.w_root.statusbar.showMessage("Ошибка записи в файл    ........" + str(err), 2000)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)", options=options)
        if path_img:
            return path_img

    def update_image(self):
        self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img())

    def update_plot(self):
        self.ax.clear()
        line = self.Img1.get_line()
        self.ax.plot(np.divide(np.arange(len(line)), self.pixel_ugl_size), line)
        self.canvas.draw()

    def init_plot_widget(self):
        self.canvas = FigureCanvas(plt.figure())
        self.w_root.verticalLayout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()

    def write_in_file(self):
        fp = open('file.txt', 'w')
        y = self.Img1.get_line()
        x = np.divide(np.arange(len(y)), self.pixel_ugl_size)
        fp.write('Date/Time : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
        fp.write('Угловой размер пикселя = ' + str(self.pixel_ugl_size) + '\n\n')
        for i in range(len(y)):
            # fp.write(str(x[i]))
            fp.write(f"%{len(str(max(x))) + 1}.6f%{len(str(max(y))) + 10}.5f\n" % (x[i], y[i]))
            # print(x[i])
        fp.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
