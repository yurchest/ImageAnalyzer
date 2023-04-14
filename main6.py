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
import warnings
from matplotlib.patches import FancyArrowPatch


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from scipy.signal import find_peaks
from decimal import Decimal
# import numpy.polynomial.polynomial as poly


def find_left_right(y1, y2, point, plus1, plus2):
    left_gran = np.argmax(y1 > point) + plus1 - 1
    right_gran = np.argmax(y2 < point) + plus2
    return left_gran, right_gran


def get_eprs(mean1, mean2):
    return mean1, mean2


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
        try:
            os.mkdir('measurements')
        except Exception as err:
            print(err)
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
        self.pushButtonGroup.addButton(self.w_root.save_graph_button)

        self.w_root.radioButton_5.setChecked(True)
        self.w_root.radioButton.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_3.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_4.toggled.connect(lambda: self.calculate_update_all())
        self.w_root.radioButton_5.toggled.connect(lambda: self.calculate_update_all())

        self.pushButtonGroup.buttonClicked.connect(self.button_clicked)
        self.pushButtonGroup.buttonClicked.connect(lambda: self.calculate_update_all())

        self.w_root.comboBox.currentTextChanged.connect(self.update_plot)

        self.timer = QtCore.QTimer()
        self.pushButtonGroup2.buttonPressed.connect(self.on_press)
        self.pushButtonGroup2.buttonReleased.connect(self.on_release)
        self.timer.timeout.connect(self.while_pressed)

        self.w_root.settings_button.clicked.connect(self.open_settings)
        self.w_root.settings_button_2.clicked.connect(self.save_img)

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
            self.w_root.statusbar.showMessage("Конфигурационный файл не найден ", 2500)

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
                self.w_root.statusbar.showMessage("Готово ", 2500)
            elif button == self.w_root.save_graph_button:
                self.save_graph()

        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 2500)

    def open_file_create_img(self):
        if self.get_file_name():
            self.w_root.statusbar.showMessage("Готово ", 2500)
            self.Img1 = Img(self.path_img)
            self.Img1.set_line(self.Img1.get_max_line_bright())
            if len(self.path_img) == 1:
                self.w_root.label_2.setText(f"Усреднение по 1 изображению")
            else:
                self.w_root.label_2.setText(f"Усреднение по {len(self.path_img)} изображениям")
            self.file_opened = True
        else:
            self.w_root.statusbar.showMessage("Не удалось открыть файл ", 2500)

    def get_file_name(self):
        self.w_root.statusbar.showMessage("Открытие файла ... ")
        self.path_img, _ = QFileDialog.getOpenFileNames(self, "Выберите файл", "./",
                                                        "Image Files(*.bmp);;All Files (*)")
        if self.path_img:
            return self.path_img

    def update_plot(self):
        if self.file_opened:
            if self.w_root.comboBox.currentText() == 'Однопятенный':
                self.ax.clear()
                self.ax.grid(axis="y")
                line = np.array(self.Img1.get_line())
                self.mean = self.find_one_mean(line)
                self.ax.plot(np.divide(np.arange(line.size), self.pixel_ugl_size) - np.divide(self.mean,self.pixel_ugl_size) , line)
                self.ax.plot(np.divide(self.mean, self.pixel_ugl_size) - np.divide(self.mean,self.pixel_ugl_size), line[int(self.mean)], "x", color='purple')
                self.ax.axvline(np.divide(self.mean, self.pixel_ugl_size) - np.divide(self.mean,self.pixel_ugl_size),
                                        ymax=line[int(self.mean)] / self.ax.get_ylim()[1], color='green', ls=':', lw=1)
                self.w_root.label_8.setText("")
                self.canvas.draw()
            else:  
                try:

                    self.ax.clear()
                    self.ax.grid(axis="y")
                    line = np.array(self.Img1.get_line())
                    self.ax.plot(np.divide(np.arange(line.size), self.pixel_ugl_size), line)
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
                        self.left1, self.right1 = find_left_right(line[0:self.peaks[0]],
                                                                  line[self.peaks[0]:self.local_min],
                                                                  line[self.local_min] + 0.15 * line[self.peaks[0]], 0,
                                                                  self.peaks[0])
                        self.left2, self.right2 = find_left_right(line[self.local_min:self.peaks[1]],
                                                                  line[self.peaks[1]:],
                                                                  line[self.local_min] + 0.15 * line[self.peaks[0]],
                                                                  self.local_min, self.peaks[1])
                        self.mean1, self.mean2 = self.find_means(line[self.left1:self.right1], line[self.left2:self.right2],
                                                                 self.left1, self.left2, line)

                        bright1, bright2 = get_eprs(line[int(self.mean1)], line[int(self.mean2)])

                        try:
                            self.epr1 = bright1 / self.bright_kontr * self.epr_kontr
                            self.epr2 = bright2 / self.bright_kontr * self.epr_kontr
                            self.w_root.lineEdit_4.setText(f"{Decimal(str(self.epr1)):.4e}")
                            self.w_root.lineEdit_5.setText(f"{Decimal(str(self.epr2)):.4e}")
                        except Exception as err:
                            self.w_root.statusbar.showMessage(str(err), 2500)

                        # self.ax.plot(sps.norm.pdf(np.arange(len(line)),loc=list(line).index(mean), scale=np.std(line)))
                        # self.ax.plot(list(line).index(mean), np.mean(line), "x")
                        # self.ax.plot(self.right11, line[self.right11], "x")
                        # self.ax.plot(self.left11, line[self.left11], "x")

                        self.ax.plot(np.divide(self.mean1, self.pixel_ugl_size), self.mean1_y, "x", color='purple')
                        self.ax.plot(np.divide(self.mean2, self.pixel_ugl_size), self.mean2_y, "x", color='purple')
                        # self.ax.plot(np.divide(self.left1, self.pixel_ugl_size), line[self.left1], "x", color='black')
                        # self.ax.plot(np.divide(self.left2, self.pixel_ugl_size), line[self.left2], "x", color='black')
                        # self.ax.plot(np.divide(self.right2, self.pixel_ugl_size), line[self.right2], "x", color='black')
                        # self.ax.plot(np.divide(self.right1, self.pixel_ugl_size), line[self.right1], "x", color='black')

                        self.ax.axvline(np.divide(self.mean1, self.pixel_ugl_size),
                                        ymax=self.mean1_y / self.ax.get_ylim()[1], color='green', ls=':', lw=1)
                        self.ax.axvline(np.divide(self.mean2, self.pixel_ugl_size),
                                        ymax=self.mean2_y / self.ax.get_ylim()[1], color='green', ls=':', lw=1)
                        y_arrow  = min(self.mean1_y, self.mean2_y) * 0.8
                        myArrow = FancyArrowPatch((np.divide(self.mean1, self.pixel_ugl_size), y_arrow), (np.divide(self.mean2, self.pixel_ugl_size), y_arrow), arrowstyle='<|-|>', mutation_scale=15, shrinkA=0, shrinkB=0,color='0.5')
                        self.ax.add_artist(myArrow)

                        # self.ax.axhline(y=10, xmin=np.divide(self.mean1,self.pixel_ugl_size)/self.ax.get_xlim()[1],xmax=np.divide(self.mean2,self.pixel_ugl_size)/self.ax.get_xlim()[1] ,color='green', ls=':', lw=1)

                        # self.ax.plot(self.peaks, line[self.peaks], "x")

                        # self.ax.plot(np.divide(self.local_min, self.pixel_ugl_size),
                        #              line[self.local_min], "x")
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
                            bright3, bright4 = get_eprs(
                                line[int(float(self.kontr_centr) - self.kontr_ugl_length * self.pixel_ugl_size / 2)],
                                line[int(float(self.kontr_centr) + self.kontr_ugl_length * self.pixel_ugl_size / 2)])
                            self.epr3 = bright3 / self.bright_kontr * self.epr_kontr
                            self.epr4 = bright4 / self.bright_kontr * self.epr_kontr
                            self.w_root.lineEdit_8.setText(f"{Decimal(str(self.epr3)):.4e}")
                            self.w_root.lineEdit_9.setText(f"{Decimal(str(self.epr4)):.4e}")
                        else:
                            self.w_root.lineEdit_8.setText("")
                            self.w_root.lineEdit_9.setText("")
                    except Exception as err:
                        self.w_root.label_8.setText("Не определен центр контрольного УО")
                        self.w_root.statusbar.showMessage(str(err), 2500)
                    self.canvas.draw()
                except Exception as err:
                    self.w_root.label_8.setText("Ошибка построения графика")
                    self.w_root.statusbar.showMessage(str(err), 2500)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 2500)


    def find_one_mean(self, y1):
        ## 3-й способ:  
        self.mean1_y = np.mean(y1)
        mean1 = np.sum(np.arange(y1.size) * y1) / np.sum(y1)

        return mean1

    def find_means(self, y1, y2, plus1, plus2, line):
        if self.w_root.radioButton_3.isChecked():
            self.mean1_y = np.mean(y1)
            self.mean2_y = np.mean(y2)

            ### 1-й способ: сумма слева == сумма справа ------------------------

            c1 = y1.cumsum()
            c2 = y1[::-1].cumsum()[::-1]
            mean1 = np.argmin(np.abs(c1 - c2)) + plus1
            c1 = y2.cumsum()
            c2 = y2[::-1].cumsum()[::-1]
            mean2 = np.argmin(np.abs(c1 - c2)) + plus2

        elif self.w_root.radioButton.isChecked():
            warnings.simplefilter('ignore', np.RankWarning)
            p = np.polyfit(np.arange(line.size), line, 20)
            yp = np.polyval(p, np.arange(line.size))

            self.ax.plot(np.divide(np.arange(line.size), self.pixel_ugl_size), yp, ls=":", lw=2, color="purple")
            

            peaks = self.find_local_max(yp)
            mean1 = peaks[0]
            mean2 = peaks[1]
            self.mean1_y = yp[mean1]
            self.mean2_y = yp[mean2]

        elif self.w_root.radioButton_4.isChecked():
            mean1, mean2 = self.peaks[0], self.peaks[1]
            self.mean1_y, self.mean2_y = line[mean1], line[mean2]

        elif self.w_root.radioButton_5.isChecked():

            ## 3-й способ:  
            self.mean1_y = np.mean(y1)
            self.mean2_y = np.mean(y2)

            mean1 = np.sum(np.arange(y1.size) * y1) / np.sum(y1) + plus1
            mean2 = np.sum(np.arange(y2.size) * y2) / np.sum(y2) + plus2

        return mean1, mean2

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
            self.update_max_bright()

        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 2500)


    def update_max_bright(self):
        self.max_bright = self.Img1.get_max_bright()
        self.w_root.lineEdit_10.setText(str(self.max_bright))

    def update_image(self):
        if self.file_opened:
            self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img(500, 500))
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 2500)

    def calc_set_length(self):
        if self.w_root.label_8.text() == "Ошибка нахождения контрольных точек":
            self.w_root.lineEdit_7.setText("Error")
        else:
            try:
                self.length = np.absolute(round(((self.mean2 - self.mean1) / self.pixel_ugl_size), 5))
                self.w_root.lineEdit_7.setText(str(self.length))
            except Exception as err:
                self.w_root.statusbar.showMessage(str(err), 2500)
                self.w_root.lineEdit_7.setText("Error")

    def write_in_file(self):

        try:
            date_time = datetime.now().strftime("%m.%d.%Y___%H-%M-%S")
            name_of_file = f"Measure {date_time}.txt"
            fp = open(f"measurements/{name_of_file}", 'w')
            y = self.Img1.get_line()
            
            fp.write('Date/Time : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n\n')
            if self.w_root.comboBox.currentText() == 'Двухпятенный':
                x = np.divide(np.arange(len(y)), self.pixel_ugl_size)
                fp.write('Угловой размер пикселя = ' + str(self.pixel_ugl_size) + '\n')
                fp.write('Угловое расстояние между пятнами = ' + self.w_root.lineEdit_7.text() + " угловых секунд" + '\n')
                fp.write('Максимальная яркость = ' + self.w_root.lineEdit_10.text() + " условных единиц" + '\n\n') ###########
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
                    # fp.write(f"%{len(str(max(x))) + 1}.6f%{len(str(max(y))) + 10}.5f\n" % (x[i], y[i]))
                    # fp.write("{:<12} {:<8}\n".format(x[i], y[i]))
                    fp.write(f"{x[i]:.6f}\t{y[i]:.5f}\n")
            else:
                fp.write(f"Максимальная яркость =  {y[int(self.mean)]}\n\n")
                x = np.divide(np.arange(len(y)), self.pixel_ugl_size) - np.divide(self.mean,self.pixel_ugl_size)
                for i in range(len(y)):
                    fp.write(f"{x[i]:.6f}\t{y[i]:.5f}\n")
            fp.close()  
            done = QMessageBox()
            done.setWindowTitle("Информация")
            done.setText(f"Успешно записано в файл:\n {name_of_file}       ")
            done.exec()
            self.w_root.statusbar.showMessage("Готово ", 2500)
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Ошибка записи в файл\n\n" + str(err))
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
        # self.calculate_update_all()
        self.timer.start(50)

    def while_pressed(self):
        if self.count > 2:
            self.button_clicked(self.current_line_button)
            self.calculate_update_all()
            # self.calculate_update_all(plot=False, setlen=False)
        self.count += 1

    def save_graph(self):
        try:
            date_time = datetime.now().strftime("%m.%d.%Y___%H-%M-%S")
            name_of_file = f"Graph {date_time}.jpg"
            self.canvas.print_figure(f"measurements/{name_of_file}")
            done = QMessageBox()
            done.setWindowTitle("Информация")
            done.setText(f"График успешно сохранен под именем :\n {name_of_file}       ")
            done.exec()
            self.w_root.statusbar.showMessage("Готово ", 2500)
        except Exception as err:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText("Ошибка сохранения графика\n" + str(err))
            error.setIcon(QMessageBox.Information)
            error.exec()
            self.w_root.statusbar.showMessage("Ошибка сохранения графика    ........" + str(err), 2000)

    def save_img(self):
        if self.file_opened:
            try:
                date_time = datetime.now().strftime("%m.%d.%Y___%H-%M-%S")
                name_of_file = f"measurements/Image {date_time}.bmp"
                self.Img1.save_img(name_of_file)
                done = QMessageBox()
                done.setWindowTitle("Информация")
                done.setText(f"Изображение успешно сохранен под именем :\n {name_of_file}       ")
                done.exec()
                self.w_root.statusbar.showMessage("Готово ", 2500)
            except Exception as err:
                error = QMessageBox()
                error.setWindowTitle("Ошибка")
                error.setText("Ошибка сохранения графика\n" + str(err))
                error.setIcon(QMessageBox.Information)
                error.exec()
                self.w_root.statusbar.showMessage("Ошибка сохранения графика    ........" + str(err), 2000)
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 2500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
