import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QButtonGroup, QVBoxLayout
from PyQt5.QtCore import QTimer
from form import *
from settings import Settings
import sys
from img_class import Img
import numpy as np
from datetime import datetime
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from scipy.signal import find_peaks


class App(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_window = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.main_window)
        self.main_window.setWindowTitle('IMG Analyzer')

        self.set_form = Settings()
        self.set_form.data_signal.connect(self.set_incoming_data)
        self.set_form.set_mainwindow_active.connect(lambda: self.main_window.setEnabled(True))
        self.set_form.set_mainwindow_active.connect(self.calculate_update_all)
        self.pixel_ugl_size = 1
        self.set_incoming_data()

        self.init_plot()

        self.file_opened = False

        self.pushButtonGroup = QButtonGroup(self)
        self.pushButtonGroup2 = QButtonGroup(self)
        self.w_root.choose_file_button.clicked.connect(self.open_file_create_img)
        self.w_root.choose_file_button.clicked.connect(lambda: self.calculate_update_all())
        self.pushButtonGroup.addButton(self.w_root.find_centre_button)
        self.pushButtonGroup2.addButton(self.w_root.line_up_button)
        self.pushButtonGroup2.addButton(self.w_root.line_down_button)
        self.pushButtonGroup.addButton(self.w_root.write_file_button)

        self.pushButtonGroup.buttonClicked.connect(self.button_clicked)
        self.pushButtonGroup.buttonClicked.connect(lambda: self.calculate_update_all())

        self.timer = QtCore.QTimer()
        self.pushButtonGroup2.buttonPressed.connect(self.on_press)
        self.pushButtonGroup2.buttonReleased.connect(self.on_release)
        self.timer.timeout.connect(self.while_pressed)

        self.w_root.settings_button.clicked.connect(self.open_settings)

        self.main_window.show()

    def set_incoming_data(self, data=None):
        if os.path.isfile("cfg/sett.txt"):
            with open("cfg/sett.txt", 'r') as f:
                data = f.readlines()
                if data[0] != "\n": self.pixel_ugl_size = float(data[0].strip())
                if data[1] != "\n": self.kontr_ugl_length = float(data[1].strip())
                if data[2] != "\n": self.show_kontr_ugl_length = data[2].strip()
                if data[4] != "\n": self.kontr_centr = float(data[4].strip())
                if data[5] != "\n": self.epr_kontr = float(data[5].strip())

            self.w_root.lineEdit.setText(data[0].strip().replace('.', ','))
            if data[5] != "\n": self.w_root.lineEdit_2.setText(str(data[5].strip().replace('.', ',') + ' * 10**7'))
            # self.w_root.lineEdit_2.setText(data[1].strip().replace('.', ','))
            # self.w_root.radioButton.setChecked(bool(data[2].strip()))
        else:
            self.w_root.statusbar.showMessage("Конфигурационный файл не найден ", 1500)

    def open_settings(self):
        self.main_window.setEnabled(False)
        self.set_form.w2.exec_()

    def button_clicked(self, button):
        if self.file_opened:
            if button == self.w_root.line_up_button:
                self.Img1.line_up()
            elif button == self.w_root.line_down_button:
                self.Img1.line_down()
            elif button == self.w_root.write_file_button:
                self.write_in_file()
            elif button == self.w_root.find_centre_button:
                self.w_root.statusbar.showMessage("Обработка ... ")
                self.Img1.set_line(self.Img1.get_max_line_bright())
                self.w_root.statusbar.showMessage("Готово ", 1500)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def open_file_create_img(self):
        if self.get_file_name():
            self.Img1 = Img(self.path_img)
            self.w_root.label_2.setText(self.path_img)
            self.file_opened = True
        else:
            self.w_root.statusbar.showMessage("Не удалось открыть файл ", 1500)

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)", options=options)
        if self.path_img:
            return self.path_img

    def update_plot(self):
        if self.file_opened:
            try:

                self.ax.clear()
                self.ax.grid(axis="y")
                line = np.array(self.Img1.get_line())
                self.ax.plot(np.divide(np.arange(len(line)), self.pixel_ugl_size), line)
                self.w_root.label_8.setText("")

                try:
                    self.find_local_max(line)
                    self.find_local_min(line[int(self.peaks[0]):int(self.peaks[-1])])
                    self.local_min = int(np.mean(self.lows))
                    self.left1, self.right1 = self.find_left_right(line[0:self.peaks[0]],
                                                                   line[self.peaks[0]:self.local_min],
                                                                   line[self.local_min] + 0.2 * line[self.peaks[0]], 0,
                                                                   self.peaks[0])
                    self.left2, self.right2 = self.find_left_right(line[self.local_min:self.peaks[1]],
                                                                   line[self.peaks[1]:],
                                                                   line[self.local_min] + 0.2 * line[self.peaks[0]],
                                                                   self.local_min, self.peaks[1])
                    self.mean1, self.mean2 = self.find_means(line[self.left1:self.right1], line[self.left2:self.right2],
                                                             self.left1, self.left2)
                    epr1, epr2 = self.get_eprs(line[int(self.mean1)], line[int(self.mean2)])

                    self.w_root.lineEdit_4.setText(str(epr1) + " * 10**7")
                    self.w_root.lineEdit_5.setText(str(epr2) + " * 10**7")

                    # self.ax.plot(sps.norm.pdf(np.arange(len(line)),loc=list(line).index(mean), scale=np.std(line)))
                    # self.ax.plot(list(line).index(mean), np.mean(line), "x")
                    # self.ax.plot(self.right11, line[self.right11], "x")
                    # self.ax.plot(self.left11, line[self.left11], "x")
                    self.ax.plot(np.divide(self.mean1, self.pixel_ugl_size), self.mean1_y, "x", color='purple')
                    self.ax.plot(np.divide(self.mean2, self.pixel_ugl_size), self.mean2_y, "x", color='purple')
                    self.ax.plot(np.divide(self.left1, self.pixel_ugl_size), line[self.left1], "x", color='black')
                    self.ax.plot(np.divide(self.left2, self.pixel_ugl_size), line[self.left2], "x", color='black')
                    self.ax.plot(np.divide(self.right2, self.pixel_ugl_size), line[self.right2], "x", color='black')
                    self.ax.plot(np.divide(self.right1, self.pixel_ugl_size), line[self.right1], "x", color='black')

                    self.ax.axvline(np.divide(self.mean1, self.pixel_ugl_size),
                                    ymax=self.mean1_y / self.ax.get_ylim()[1], color='green', ls=':', lw=1)
                    self.ax.axvline(np.divide(self.mean2, self.pixel_ugl_size),
                                    ymax=self.mean2_y / self.ax.get_ylim()[1], color='green', ls=':', lw=1)
                    # self.ax.axhline(y=10, xmin=np.divide(self.mean1,self.pixel_ugl_size)/self.ax.get_xlim()[1],xmax=np.divide(self.mean2,self.pixel_ugl_size)/self.ax.get_xlim()[1] ,color='green', ls=':', lw=1)

                    # self.ax.plot(self.peaks, line[self.peaks], "x")
                    self.ax.plot(np.divide(self.local_min, self.pixel_ugl_size),
                                 line[self.local_min], "x")
                except Exception as err:
                    self.w_root.label_8.setText("Ошибка нахождения контрольных точек")
                    self.w_root.lineEdit_7.setText("Error")
                    self.w_root.statusbar.showMessage(str(err), 1500)
                try:
                    if self.show_kontr_ugl_length == "True":
                        self.ax.axvline(float(self.kontr_centr / self.pixel_ugl_size) - self.kontr_ugl_length / 2,
                                        color='red', ls=':', lw=1)
                        self.ax.axvline(float(self.kontr_centr / self.pixel_ugl_size) + self.kontr_ugl_length / 2,
                                        color='red', ls=':', lw=1)
                        epr3, epr4 = self.get_eprs(
                            line[int(float(self.kontr_centr) - self.kontr_ugl_length * self.pixel_ugl_size / 2)],
                            line[int(float(self.kontr_centr) + self.kontr_ugl_length * self.pixel_ugl_size / 2)])
                        self.w_root.lineEdit_8.setText(str(epr3) + " * 10**7")
                        self.w_root.lineEdit_9.setText(str(epr4) + " * 10**7")
                    else:
                        self.w_root.lineEdit_8.setText("")
                        self.w_root.lineEdit_9.setText("")
                except Exception as err:
                    self.w_root.label_8.setText("Не определен центр контрольного УО")
                    self.w_root.statusbar.showMessage(str(err), 1500)
                self.canvas.draw()
            except Exception as err:
                self.w_root.label_8.setText("Ошибка построения графика")
                self.w_root.statusbar.showMessage(str(err), 1500)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def find_means(self, y1, y2, plus1, plus2):

        self.mean1_y = np.mean(y1)
        self.mean2_y = np.mean(y2)

        left_sum = 0
        right_sum = np.sum(y1)

        for i in range(y1.size):
            left_sum += y1[i]
            right_sum -= y1[i]
            if (right_sum - left_sum) < 500:
                mean1 = i + plus1
                break

        left_sum = 0
        right_sum = np.sum(y2)

        for i in range(y2.size):
            left_sum += y2[i]
            right_sum -= y2[i]
            if (right_sum - left_sum) < 500:
                mean2 = i + plus2
                break

        return mean1, mean2

    def find_left_right(self, y1, y2, point, plus1, plus2):
        for i in range(y1.size):
            if (y1[i] >= point) and (y1[i - 1] <= point):
                left_gran = i + plus1
                break
        for i in range(y2.size):
            if (y2[i] <= point) and (y2[i - 1] >= point):
                right_gran = i - 1 + plus2
        return left_gran, right_gran

    def find_local_max(self, y):
        self.peaks, _ = find_peaks(y, height=50, distance=50, prominence=10, width=40)

    def find_local_min(self, y):
        y1 = np.multiply(y, -1)
        self.lows, _ = find_peaks(y1, height=-60, distance=10, prominence=10, width=5)
        self.lows = self.lows + self.peaks[0]

    def init_plot(self):
        self.canvas = FigureCanvas(plt.figure())
        self.w_root.verticalLayout.addWidget(self.canvas)
        self.ax = self.canvas.figure.subplots()
        self.ax.set_ylabel("Интенсивность")
        self.ax.set_xlabel("угл. сек.")

        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel("Уровень")

    def calculate_update_all(self, img=True, plot=True, setlen=True):
        if self.file_opened:
            if img: self.update_image()
            if plot: self.update_plot()
            if setlen: self.calc_set_length()
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def update_image(self):
        if self.file_opened:
            self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img(500, 500))
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def calc_set_length(self):
        if self.w_root.label_8.text():
            self.w_root.lineEdit_7.setText("Error")
        else:
            try:
                self.length = round(((self.mean2 - self.mean1) / self.pixel_ugl_size), 5)
                self.w_root.lineEdit_7.setText(str(self.length) + " угл. сек.")
            except Exception as err:
                self.w_root.statusbar.showMessage(str(err), 1500)
                self.w_root.lineEdit_7.setText("Error")

    def write_in_file(self):
        try:
            fp = open('file.txt', 'w')
            y = self.Img1.get_line()
            x = np.divide(np.arange(len(y)), self.pixel_ugl_size)
            fp.write('Date/Time : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
            fp.write('Угловой размер пикселя = ' + str(self.pixel_ugl_size) + '\n')
            fp.write('Расстояние между пятнами = ' + str(self.length) + " угловых секунд" + '\n\n')
            for i in range(len(y)):
                # fp.write(str(x[i]))
                fp.write(f"%{len(str(max(x))) + 1}.6f%{len(str(max(y))) + 10}.5f\n" % (x[i], y[i]))
                # print(x[i])
            fp.close()
            done = QMessageBox()
            done.setWindowTitle("Информация")
            done.setText("Успешно записано в файл       ")
            done.exec()
            self.w_root.statusbar.showMessage("Готово ", 1500)
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Ошибка записи в файл\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()
            self.w_root.statusbar.showMessage("Ошибка записи в файл    ........" + str(err), 2000)

    def on_release(self):
        self.calculate_update_all()
        self.timer.stop()
        self.count = 0

    def on_press(self, button):
        self.count = 0
        self.current_line_button = button
        self.button_clicked(button)
        self.calculate_update_all()
        self.timer.start(50)

    def while_pressed(self):
        if self.count > 2:
            self.button_clicked(self.current_line_button)
            self.calculate_update_all()
            # self.calculate_update_all(plot=False, setlen=False)
        self.count += 1

    def get_eprs(self, mean1, mean2):
        return mean1, mean2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
