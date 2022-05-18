import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QButtonGroup
# from PyQt5.QtCore import QTimer
from form import *
from settings import Settings
import sys
from img_class import Img
import numpy as np
from datetime import datetime
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from scipy.signal import find_peaks
from decimal import Decimal
import numpy.polynomial.polynomial as poly


from scipy.stats import boxcox
from scipy.special import boxcox1p
from scipy.stats import norm
import scipy.stats


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

        self.w_root.radioButton.setChecked(True)
        self.w_root.radioButton.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_3.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_4.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_5.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_6.toggled.connect(lambda: self.calculate_update_all())

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
                if data[5] != "\n": self.bright_kontr = float(data[5].strip())


            self.w_root.lineEdit.setText(data[0].strip().replace('.', ','))
            self.epr_kontr = 1e7
            self.w_root.lineEdit_2.setText(f"{Decimal(str(self.epr_kontr)):.4e}")

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
            self.Img1.set_line(self.Img1.get_max_line_bright())
            self.w_root.label_2.setText(str(self.path_img))
            self.file_opened = True
        else:
            self.w_root.statusbar.showMessage("Не удалось открыть файл ", 1500)

    def get_file_name(self):
        self.path_img, _ = QFileDialog.getOpenFileNames(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)")
        if self.path_img:
            return self.path_img

    def get_indices(self, lst, el):
        list = []
        for i in range(len(lst)):
            if lst[i] == el:
                list.append(i)
        return list

    def update_plot(self):
        if self.file_opened:
            try:

                self.ax.clear()
                self.ax.grid(axis="y")
                line = np.array(self.Img1.get_line())
                self.ax.plot(np.divide(np.arange(len(line)), self.pixel_ugl_size), line)
                # ## Показывать привидение к нормальному ------------------
                # line_norm = np.multiply(list(boxcox1p(list(line), -0.2)), 8)
                # for i in range(line_norm.size):
                #     if line_norm[i] < 0.4*max(line_norm):
                #         line_norm[i] = 0
                # self.ax.plot(np.divide(np.arange(len(line_norm)), self.pixel_ugl_size), line_norm, ls='-')
                # ## ------------------------------------------------------
                self.w_root.label_8.setText("")

                try:
                    self.find_local_max(line)
                    self.find_local_min(line[int(self.peaks[0]):int(self.peaks[-1])])
                    self.local_min = int(np.mean(self.lows))
                    self.left1, self.right1 = self.find_left_right(line[0:self.peaks[0]],
                                                                   line[self.peaks[0]:self.local_min],
                                                                   line[self.local_min] + 0.15 * line[self.peaks[0]], 0,
                                                                   self.peaks[0])
                    self.left2, self.right2 = self.find_left_right(line[self.local_min:self.peaks[1]],
                                                                   line[self.peaks[1]:],
                                                                   line[self.local_min] + 0.15 * line[self.peaks[0]],
                                                                   self.local_min, self.peaks[1])
                    self.mean1, self.mean2 = self.find_means(line[self.left1:self.right1], line[self.left2:self.right2],
                                                             self.left1, self.left2,line)

                    bright1, bright2 = self.get_eprs(line[int(self.mean1)], line[int(self.mean2)])

                    try:
                        self.epr1 = bright1/self.bright_kontr*self.epr_kontr
                        self.epr2 = bright2/self.bright_kontr*self.epr_kontr
                        self.w_root.lineEdit_4.setText(f"{Decimal(str(self.epr1)):.4e}")
                        self.w_root.lineEdit_5.setText(f"{Decimal(str(self.epr2)):.4e}")
                    except Exception as err:
                        self.w_root.statusbar.showMessage(str(err), 1500)


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
                    self.w_root.lineEdit_4.setText("")
                    self.w_root.lineEdit_5.setText("")
                    self.w_root.statusbar.showMessage(str(err), 1500)
                try:
                    if self.show_kontr_ugl_length == "True":
                        self.ax.axvline(float(self.kontr_centr / self.pixel_ugl_size) - self.kontr_ugl_length / 2,
                                        color='red', ls=':', lw=1)
                        self.ax.axvline(float(self.kontr_centr / self.pixel_ugl_size) + self.kontr_ugl_length / 2,
                                        color='red', ls=':', lw=1)
                        bright3, bright4 = self.get_eprs(
                            line[int(float(self.kontr_centr) - self.kontr_ugl_length * self.pixel_ugl_size / 2)],
                            line[int(float(self.kontr_centr) + self.kontr_ugl_length * self.pixel_ugl_size / 2)])
                        self.epr3 = bright3/self.bright_kontr*self.epr_kontr
                        self.epr4 = bright4/self.bright_kontr*self.epr_kontr
                        self.w_root.lineEdit_8.setText(f"{Decimal(str(self.epr3)):.4e}")
                        self.w_root.lineEdit_9.setText(f"{Decimal(str(self.epr4)):.4e}")
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

    def find_means(self, y1, y2, plus1, plus2, line):
        if self.w_root.radioButton_3.isChecked():
            self.mean1_y = np.mean(y1)
            self.mean2_y = np.mean(y2)
            ### 1-й способ: сумма слева == сумма справа ------------------------
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
        elif self.w_root.radioButton.isChecked():

            # p = np.polyfit(np.arange(line.size), line, 50)
            p = poly.polyfit(np.arange(line.size), line, 50)
            # yp = np.polyval(p, np.arange(line.size))
            yp = poly.polyval(np.arange(line.size), p)
            self.ax.plot(np.divide(np.arange(line.size), self.pixel_ugl_size), yp, ls=":", lw=2, color = "purple")
            peaks = self.find_local_max(yp)
            mean1 = peaks[0]
            mean2 = peaks[1]
            self.mean1_y = yp[mean1]
            self.mean2_y = yp[mean2]

            # from scipy.optimize import curve_fit


            # pars1, cov = curve_fit(f=self.Gauss, xdata=np.arange(y1.size), ydata=y1, p0=[100, 20, 20], bounds=(-np.inf, np.inf))
            # pars2, cov = curve_fit(f=self.Gauss, xdata=np.arange(y2.size), ydata=y2, p0=[100, 20, 20], bounds=(-np.inf, np.inf))
            # print(pars1)
            # print(pars2)
            # # self.ax.clear()
            # fit_y1 = self.Gauss(np.arange(y1.size), pars1[0], pars1[1], pars1[2])
            # fit_y2 = self.Gauss(np.arange(y2.size), pars2[0], pars2[1], pars2[2])
            # self.ax.plot(np.divide(np.arange(y1.size) + plus1, self.pixel_ugl_size),fit_y1, ls=":", lw=2, color="purple")
            # self.ax.plot(np.divide(np.arange(y2.size) + plus2, self.pixel_ugl_size),fit_y2, ls=":", lw=2, color="purple")
            #
            # mean1 = pars1[1] + plus1
            # mean2 = pars2[1] + plus2
            #
            # self.mean1_y = np.max(fit_y1)
            # self.mean2_y = np.max(fit_y2)

            # pars3, cov = curve_fit(f=self.sin_func, xdata=np.arange(line.size), ydata=line, p0=[100, 100, 100, 100, 100, 100],
            #                        bounds=(-np.inf, np.inf))
            # print(pars3)
            # fit_y = self.sin_func(np.arange(line.size), pars3[0], pars3[1], pars3[2], pars3[3], pars3[4], pars3[5])
            # self.ax.plot(np.divide(np.arange(line.size), self.pixel_ugl_size), fit_y, ls=":", lw=2,
            #              color="purple")
        elif self.w_root.radioButton_4.isChecked():
            mean1, mean2 = self.peaks[0], self.peaks[1]
            self.mean1_y, self.mean2_y = line[mean1], line[mean2]

        elif self.w_root.radioButton_5.isChecked():

            ## 3-й способ:
            self.mean1_y = np.mean(y1)
            self.mean2_y = np.mean(y2)
            summ =0
            for i in range(y1.size):
                summ += i*y1[i]
            mean1 = summ/np.sum(y1) + plus1

            summ =0
            for i in range(y2.size):
                summ += i*y2[i]
            mean2 = summ/np.sum(y2) + plus2

        elif self.w_root.radioButton_6.isChecked():
            self.mean1_y = np.mean(y1)
            self.mean2_y = np.mean(y2)
            # 2-й способ: поиск среднего из координат
            p = []
            for el in y1:
                p += self.get_indices(list(y1), el)
            mean1 = np.mean(p) + plus1

            p = []
            for el in y2:
                p += self.get_indices(list(y1), el)
            mean2 = np.mean(p) + plus2


        return mean1, mean2

    def Gauss(self,x, a, b,c):
        return a*np.exp(-np.power(x - b, 2)/(2*np.power(c, 2)))

    def sin_func(self,x, a, b, c, d,e ,f):
            return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f

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
        peaks, _ = find_peaks(y, height=50, distance=50, prominence=10, width=40)
        self.peaks = peaks
        return peaks

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
        if self.w_root.label_8.text() == "Ошибка нахождения контрольных точек":
            self.w_root.lineEdit_7.setText("Error")
        else:
            try:
                self.length = np.absolute(round(((self.mean2 - self.mean1) / self.pixel_ugl_size), 5))
                self.w_root.lineEdit_7.setText(str(self.length))
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
            fp.write('Угловое расстояние между пятнами = ' + str(self.length) + " угловых секунд" + '\n\n')
            fp.write('-----------------------------------------------\n')
            fp.write('Измерения ЭПР: \n')
            try:
                fp.write('Левое пятно = ' + f"{Decimal(str(self.epr1)):.4e}" + '  м^2\n')
                fp.write('Правое пятно = ' + f"{Decimal(str(self.epr2)):.4e}" + '  м^2\n\n\n')
            except:
                fp.write('Левое пятно = ' + f"Неизвестно" + '  м^2\n')
                fp.write('Правое пятно = ' + f"Неизвестно" + '  м^2\n\n\n')
            for i in range(len(y)):
                # fp.write(str(x[i]))
                fp.write(f"%{len(str(max(x))) + 1}.6f%{len(str(max(y))) + 10}.5f\n" % (x[i], y[i]))
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
