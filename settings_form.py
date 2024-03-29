# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1079, 656)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(270, 20, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("    border-radius: 10px;\n"
"border: 2px solid gray;")
        self.lineEdit.setText("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 90, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("    border-radius: 10px;\n"
"border: 2px solid gray;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setClearButtonEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 80, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.picture_label = QtWidgets.QLabel(Dialog)
        self.picture_label.setGeometry(QtCore.QRect(60, 250, 351, 271))
        self.picture_label.setStyleSheet("border: 1px solid gray;\n"
"    border-radius: 10px;")
        self.picture_label.setText("")
        self.picture_label.setObjectName("picture_label")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(60, 190, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.choose_kontr_file_button = QtWidgets.QPushButton(Dialog)
        self.choose_kontr_file_button.setGeometry(QtCore.QRect(200, 200, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.choose_kontr_file_button.setFont(font)
        self.choose_kontr_file_button.setStyleSheet("#choose_kontr_file_button{   \n"
" background-color: rgb(140,140,140);\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    font: bold 12px;\n"
"    min-width: 5em;\n"
"    padding: 6px;\n"
"}\n"
"    \n"
"#choose_kontr_file_button:hover {\n"
"    background-color: rgb(160,160,160);\n"
"}\n"
"\n"
"\n"
"#choose_kontr_file_button:pressed {\n"
"    background-color:  rgb(180,180,180);\n"
"}")
        self.choose_kontr_file_button.setObjectName("choose_kontr_file_button")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(210, 110, 121, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(20, 170, 1031, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(340, 130, 41, 31))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radioButton.setFont(font)
        self.radioButton.setStyleSheet("QRadioButton::indicator { width: 20px; height: 20px;};")
        self.radioButton.setText("")
        self.radioButton.setIconSize(QtCore.QSize(30, 30))
        self.radioButton.setCheckable(True)
        self.radioButton.setAutoExclusive(True)
        self.radioButton.setObjectName("radioButton")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(30, 60, 1011, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(420, 70, 121, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.close_button = QtWidgets.QPushButton(Dialog)
        self.close_button.setGeometry(QtCore.QRect(750, 590, 182, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.close_button.setFont(font)
        self.close_button.setStyleSheet("#close_button{   \n"
" background-color: rgb(140,140,140);\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"    \n"
"#close_button:hover {\n"
"    background-color: rgb(160,160,160);\n"
"}\n"
"\n"
"\n"
"#close_button:pressed {\n"
"    background-color:  rgb(180,180,180);\n"
"}")
        self.close_button.setObjectName("close_button")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(620, 250, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("\n"
"color: rgb(255, 0, 0);")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(350, 190, 461, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.close_button_2 = QtWidgets.QPushButton(Dialog)
        self.close_button_2.setGeometry(QtCore.QRect(950, 590, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.close_button_2.setFont(font)
        self.close_button_2.setStyleSheet("#close_button_2{   \n"
" background-color: rgb(140,140,140);\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    font: bold 14px;\n"
"    padding: 6px;\n"
"}\n"
"    \n"
"#close_button_2:hover {\n"
"    background-color: rgb(160,160,160);\n"
"}\n"
"\n"
"\n"
"#close_button_2:pressed {\n"
"    background-color:  rgb(180,180,180);\n"
"}")
        self.close_button_2.setObjectName("close_button_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(460, 200, 471, 371))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setGeometry(QtCore.QRect(40, 530, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.lineEdit_10 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_10.setGeometry(QtCore.QRect(260, 540, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_10.setAutoFillBackground(False)
        self.lineEdit_10.setStyleSheet("    border-radius: 10px;\n"
"border: 2px solid gray;")
        self.lineEdit_10.setText("")
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setReadOnly(True)
        self.lineEdit_10.setClearButtonEnabled(False)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.choose_kontr_file_button_2 = QtWidgets.QPushButton(Dialog)
        self.choose_kontr_file_button_2.setGeometry(QtCore.QRect(930, 540, 141, 31))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.choose_kontr_file_button_2.setFont(font)
        self.choose_kontr_file_button_2.setStyleSheet("#choose_kontr_file_button_2{   \n"
" background-color: rgb(140,140,140);\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    font: bold 12px;\n"
"    min-width: 5em;\n"
"    padding: 6px;\n"
"}\n"
"    \n"
"#choose_kontr_file_button_2:hover {\n"
"    background-color: rgb(160,160,160);\n"
"}\n"
"\n"
"\n"
"#choose_kontr_file_button_2:pressed {\n"
"    background-color:  rgb(180,180,180);\n"
"}")
        self.choose_kontr_file_button_2.setObjectName("choose_kontr_file_button_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Параметры"))
        self.label_5.setText(_translate("Dialog", "Угловой размер пикселя:"))
        self.label_6.setText(_translate("Dialog", "Контрольное угловое расстояние:"))
        self.label_7.setText(_translate("Dialog", "Контрольный УО"))
        self.choose_kontr_file_button.setText(_translate("Dialog", " Выбрать файл"))
        self.label_8.setText(_translate("Dialog", "Показывать :"))
        self.label_9.setText(_translate("Dialog", "угл. сек"))
        self.close_button.setText(_translate("Dialog", "Применить"))
        self.close_button_2.setText(_translate("Dialog", "Отмена"))
        self.label_20.setText(_translate("Dialog", "Максимальная яркость:"))
        self.choose_kontr_file_button_2.setText(_translate("Dialog", "Сохранить график"))
