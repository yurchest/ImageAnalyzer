import os

from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QImage
from settings_form import *
from img_class import Img
import cv2
import imutils

class Settings(QWidget):
    out_signal = pyqtSignal(list)
    update_img_signal_max_br = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)
        self.w2 = QtWidgets.QDialog()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self.w2)
        self.read_data()
        self.file_opened = False

        self.w_root.lineEdit.setValidator(QtGui.QDoubleValidator())
        self.w_root.lineEdit_2.setValidator(QtGui.QDoubleValidator())
        # print(self.data)
        self.w2.show()
        # self.w_root.apply_settings_button.clicked.connect(self.write_data)
        # self.w_root.apply_settings_button.clicked.connect(self.read_data)
        self.w_root.choose_kontr_file_button.clicked.connect(self.open_file_show_img)
        self.w_root.choose_kontr_file_button.clicked.connect(self.find_centre_write_lineinfile)
        self.update_img_signal_max_br.connect(lambda:self.write_data(4))

        self.w_root.lineEdit.textChanged.connect(lambda:self.write_data(1))
        self.w_root.lineEdit_2.textChanged.connect(lambda:self.write_data(2))
        self.w_root.radioButton.toggled.connect(lambda:self.write_data(3))

        self.w_root.close_button.clicked.connect(self.close)


    def close(self):
        self.w2.close()
        return

    def find_centre_write_lineinfile(self):
        if self.file_opened:
            max_line = self.Img1.get_line(self.Img1.get_max_line_bright())
            self.index_max_in_max_line = list(max_line).index(max(max_line))
            print(self.index_max_in_max_line)
            self.update_img_signal_max_br.emit(self.index_max_in_max_line)

            with open("cfg/file_line_max.txt", 'w') as f:
                for el in max_line:
                    f.write(str(el) + '\n')
            cv2.imwrite('cfg/kontr_img_tmp.png',self.Img1.img)

    def read_data(self):
        try:
            with open("cfg/sett.txt",'r') as f:
                self.data = f.readlines()
                print(self.data)
                self.set_data()
                self.out_signal.emit(self.data)
        except FileNotFoundError:
            os.mkdir('cfg')
            with open("cfg/sett.txt",'w') as f:
                for line in range(4):
                    f.write('\n')
        try:
            with open("cfg/file_line_max.txt", 'r') as f:
                kont_line = f.readlines()
                # print(self.kont_line[0])
                for i in range(len(kont_line)):
                    kont_line[i] = int(kont_line[i])
                self.index_kont_line_max = kont_line.index(max(kont_line))
                print(self.index_kont_line_max)
        except FileNotFoundError:
            print("Нет файла линии макс контрольного замера")

        try:
            self.img_kont = cv2.imread('cfg/kontr_img_tmp.png')
            self.img_kont = cv2.cvtColor(self.img_kont, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(self.img_kont, cv2.COLOR_GRAY2BGR)
            img = imutils.resize(img, width=350, height=200)
            img = QImage(img, img.shape[1], \
                         img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            pix = QPixmap(img)
            self.w_root.picture_label.setPixmap(pix)

        except:
            print("Нет файла фото контрольного замера")


    def write_data(self, x):
        try:
            with open("cfg/file_line_max.txt", 'r') as f:
                kont_line = f.readlines()
                # print(self.kont_line[0])
                for i in range(len(kont_line)):
                    kont_line[i] = int(kont_line[i])
                self.index_kont_line_max = kont_line.index(max(kont_line))
                print(self.index_kont_line_max)
            with open("cfg/sett.txt", 'r') as f:
                data = f.readlines()
                if x == 1:
                    # if self.w_root.lineEdit.text().strip() != ''
                    data[0] = self.w_root.lineEdit.text().strip() + '\n'
                    if data[3] != '\n' and self.w_root.lineEdit.text().strip() != '':
                        data[3] = str(self.index_kont_line_max / float(data[0].strip().replace(',', '.'))) + '\n'
                elif x == 2:
                    data[1] = self.w_root.lineEdit_2.text().strip() + '\n'
                elif x == 3:
                    data[2] = str(self.w_root.radioButton.isChecked()) + '\n'
                elif x == 4:
                    self.w_root.label.setText(data[3][:6])
                    print(data[0])
                    if data[0] != '\n':
                        data[3] = str(float(self.index_max_in_max_line/float(self.data[0].replace(',', '.')))) + '\n'
                    else:
                        data[3] = str(float(self.index_max_in_max_line / 1)) + '\n'

            with open("cfg/sett.txt", 'w') as f:
                print(data)
                for line in data:
                    f.write(line)
            self.read_data()

        except Exception as error:
            raise
            # self.w_root.label_11.setText("Сначала укажите угловой размер")
            print(error)
            pass

    def set_data(self):
        self.w_root.lineEdit.setText(self.data[0].strip())
        self.w_root.lineEdit_2.setText(self.data[1].strip())
        self.w_root.label.setText(self.data[3][:6])
        if self.data[2].strip() == "True":
            self.w_root.radioButton.setChecked(True)
        else:
            self.w_root.radioButton.setChecked(False)

    def open_file_show_img(self):
        try:
            if self.get_file_name():
                self.Img1 = Img(self.path_img)
                self.file_opened = True
                self.update_image()

        except Exception as err:
            self.file_opened = False
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            error.setText(
                "Не удалось отрыть файл.\n Попробуйте использовать имя файла и путь к нему только на латинице \n\n" + str(
                    err))
            error.setIcon(QMessageBox.Information)
            error.exec()


    def update_image(self):
        if self.file_opened:
            self.w_root.picture_label.setPixmap(self.Img1.get_pixmap_img(350, 200,  show_line=False))
        else:
            self.w_root.statusbar.showMessage("Файл не открыт ", 1500)

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)", options=options)
        if self.path_img:
            return self.path_img

##ЭПР яркость у контрольного * 10^7