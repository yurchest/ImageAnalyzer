import os

from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap, QImage
from settings_form import *
from img_class import Img


class Settings(QWidget):
    data_signal = pyqtSignal(list)
    set_mainwindow_active = pyqtSignal(bool)

    def __init__(self):
        QWidget.__init__(self)
        self.w2 = QtWidgets.QDialog()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self.w2)

        self.w2.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.file_opened = False
        self.read_from_cfg_file_set_values()

        self.w_root.lineEdit.setValidator(QtGui.QDoubleValidator())
        self.w_root.lineEdit_2.setValidator(QtGui.QDoubleValidator())

        self.w_root.choose_kontr_file_button.clicked.connect(self.open_file_show_img)
        self.w_root.choose_kontr_file_button.clicked.connect(self.find_centre_write_lineinfile)

        self.w_root.lineEdit.textChanged.connect(self.set_kontr_centr)

        self.w_root.close_button.clicked.connect(self.apply_close)
        self.w_root.close_button_2.clicked.connect(self.close_without_save)

        # self.w2.show()

    def read_from_cfg_file_set_values(self):
        if os.path.isfile("cfg/sett.txt"):
            with open("cfg/sett.txt", 'r') as f:
                data = f.readlines()
                if data[0] != "\n": self.ugl_size_pixel = float(data[0])
                if data[1] != "\n": self.kontr_ugl_length = float(data[1])
                if data[2] != "\n": self.show_kontr_ugl_length = bool(data[2])
                if data[3] != "\n": self.path_img = data[3].strip()
                if data[4] != "\n": self.kontr_centr = float(data[4].strip())
                if data[5] != "\n": self.epr_kontr = float(data[5].strip())

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
                epr_kontr = self.epr_kontr
                kontr_centr = self.kontr_centr
                path = self.path_img
            except:
                epr_kontr = ""
                path = ""
                kontr_centr = ""
            data = [ugl_size_pixel, kontr_ugl_length, show_kontr_ugl_length, path, kontr_centr, epr_kontr]
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
                self.update_image()

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

    def get_file_name(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path_img, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "./",
                                                       "Image Files(*.bmp);;All Files (*)", options=options)
        if self.path_img:
            return self.path_img

    def find_centre_write_lineinfile(self):
        if self.file_opened:
            max_line = self.Img1.get_line(self.Img1.get_max_line_bright())
            self.max_in_line = max(max_line)
            self.kontr_centr = list(max_line).index(max(max_line))
            self.set_kontr_centr()

    def set_kontr_centr(self):
        try:
            if self.file_opened:
                self.calculate_epr()
                self.ugl_size_pixel = float(self.w_root.lineEdit.text().strip().replace(',', '.'))
                self.w_root.label.setText(str(self.kontr_centr / float(self.ugl_size_pixel)))
            else:
                self.w_root.label.setText("Неизвестно")
        except:
            self.w_root.label.setText("Неизвестно")

    def calculate_epr(self):
        self.epr_kontr = self.max_in_line
