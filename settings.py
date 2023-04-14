import os

from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap, QImage
from settings_form import *
from img_class import Img
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class Settings(QWidget):
    data_signal = pyqtSignal(list)
    set_mainwindow_active = pyqtSignal(bool)

    def __init__(self):
        QWidget.__init__(self)
        self.w2 = QtWidgets.QDialog()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self.w2)


        # self.w2.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint & QtCore.Qt.WindowMinimizeButtonHint)
        # self.w2.setWindowFlags(self.windowFlags() & ~QtCore.Qt.MSWindowsFixedSizeDialogHint)
        # self.w2.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.file_opened = False
        self.read_from_cfg_file_set_values()

        self.w_root.lineEdit.setValidator(QtGui.QDoubleValidator())
        self.w_root.lineEdit_2.setValidator(QtGui.QDoubleValidator())

        self.w_root.choose_kontr_file_button.clicked.connect(self.open_file_show_img)
        self.w_root.choose_kontr_file_button.clicked.connect(self.find_centre_write_lineinfile)
        self.w_root.choose_kontr_file_button_2.clicked.connect(self.save_graph)

        self.w_root.lineEdit.textChanged.connect(self.set_kontr_centr)

        self.w_root.close_button.clicked.connect(self.apply_close)
        self.w_root.close_button_2.clicked.connect(self.close_without_save)

        self.w_root.lineEdit.textChanged.connect(self.update_plot)

        self.w2.closeEvent = self.closeEvent

        self.init_plot()

        # self.w2.show()

    def closeEvent(self, event):
        self.set_mainwindow_active.emit(True)
        event.accept()


    def read_from_cfg_file_set_values(self):
        if os.path.isfile("cfg/sett.txt"):
            with open("cfg/sett.txt", 'r') as f:
                data = f.readlines()
                if data[0] != "\n": self.ugl_size_pixel = float(data[0])
                if data[1] != "\n": self.kontr_ugl_length = float(data[1])
                if data[2] != "\n": self.show_kontr_ugl_length = bool(data[2])
                if data[3] != "\n": self.path_img = data[3].strip()
                if data[4] != "\n": self.kontr_centr = float(data[4].strip())
                if data[5] != "\n": self.bright_kontr = float(data[5].strip())

            self.w_root.lineEdit.setText(data[0].strip().replace('.', ','))
            self.w_root.lineEdit_2.setText(data[1].strip().replace('.', ','))
            if data[2] == "False":
                self.w_root.radioButton.setChecked(False)
            elif data[2] == "True":
                self.w_root.radioButton.setChecked(True)
            try:
                self.Img1 = Img(self.path_img)
                self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img(350, 200, show_line=False))
                self.file_opened = True
                self.find_centre_write_lineinfile()
            except:
                pass
        else:
            try:
                os.mkdir('cfg')
            except:
                pass
            self.write_to_cfg_file(['1', '1', 'False', '', '', ''])

    def write_to_cfg_file(self, list):
        with open("cfg/sett.txt", 'w') as f:
            for i in range(len(list)):
                f.write(str(list[i]) + '\n')

    def get_data_to_transfer(self):
        if self.w_root.lineEdit.text().strip() != "" and self.w_root.lineEdit_2.text().strip() != "":
            ugl_size_pixel = float(self.w_root.lineEdit.text().strip().replace(',', '.'))
            kontr_ugl_length = float(self.w_root.lineEdit_2.text().strip().replace(',', '.'))
            show_kontr_ugl_length = self.w_root.radioButton.isChecked()
            self.find_centre_write_lineinfile()
            try:
                bright_kontr = self.bright_kontr
                kontr_centr = self.kontr_centr
                path = self.path_img
            except:
                bright_kontr = ""
                path = ""
                kontr_centr = ""
            data = [ugl_size_pixel, kontr_ugl_length, show_kontr_ugl_length, path, kontr_centr, bright_kontr,
                    self.max_bright]
        else:
            return 0

        return data

    def apply_close(self):
        data_tranfer = self.get_data_to_transfer()
        if (data_tranfer == 0):
            self.set_close_error()
        else:
            self.write_to_cfg_file(data_tranfer)
            self.data_signal.emit(data_tranfer)
            self.set_mainwindow_active.emit(True)

            self.w2.close()

    def close_without_save(self):
        self.set_mainwindow_active.emit(True)
        self.w2.close()

    def set_close_error(self):
        self.w_root.label_12.setText("Задайте корректные значения перед сохранением")
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(lambda: self.w_root.label_12.setText(""))
        self.timer.start()

    def open_file_show_img(self):
        try:
            if self.get_file_name():
                self.Img1 = Img(self.path_img)
                self.file_opened = True
                self.find_centre_write_lineinfile()
                self.update_image()
                self.update_plot()
                self.max_bright = self.Img1.get_max_bright()
                self.w_root.lineEdit_10.setText(str(self.max_bright))

        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText(
                "Не удалось отрыть файл.\n Попробуйте использовать имя файла и путь к нему только на латинице \n\n" + str(
                    err))
            error.setIcon(QMessageBox.Information)
            error.exec()

    def update_image(self):
        if self.file_opened:
            self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img(350, 200, show_line=False))
        else:
            pass

    def init_plot(self):
        self.canvas = FigureCanvas(plt.figure())
        self.w_root.verticalLayout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.ax.set_ylabel("Интенсивность")
        self.ax.set_xlabel("угл. сек.")

        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel("Уровень")

    def update_plot(self):
        if self.file_opened:
            self.ax.clear()
            self.ax.set_ylabel("Интенсивность")
            self.ax.set_xlabel("угл. сек.")
            self.ax.grid(axis="y")
            self.ugl_size_pixel = float(self.w_root.lineEdit.text().strip().replace(',', '.'))
            self.ax.plot(np.divide(np.arange(self.line.size), self.ugl_size_pixel), self.line)
            self.canvas.draw()

    def get_file_name(self):
        self.path_img, _ = QFileDialog.getOpenFileNames(self, "Выберите файл", "./",
                                                        "Image Files(*.bmp);;All Files (*)")
        if self.path_img:
            return self.path_img

    def find_centre_write_lineinfile(self):
        if self.file_opened:
            max_line = self.Img1.get_line(self.Img1.get_max_line_bright())
            self.line = max_line
            self.max_in_line = max(max_line)
            self.kontr_centr = list(max_line).index(max(max_line))
            self.set_kontr_centr()

    def set_kontr_centr(self):
        if self.file_opened:
            self.calculate_epr()
            self.ugl_size_pixel = float(self.w_root.lineEdit.text().strip().replace(',', '.'))
            # self.w_root.label.setText(str(self.kontr_centr / float(self.ugl_size_pixel)))

    def calculate_epr(self):
        self.bright_kontr = self.max_in_line

    def save_graph(self):
        try:
            date_time = datetime.now().strftime("%m.%d.%Y___%H-%M-%S")
            name_of_file = f"Graph Kontr {date_time}.jpg"
            self.canvas.print_figure(f"measurements/{name_of_file}")
            done = QMessageBox()
            done.setWindowTitle("Информация")
            done.setText(f"График успешно сохранен под именем :\n {name_of_file}       ")
            done.exec()
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Ошибка сохранения графика\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()
