# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\work\PyQt\ReportHandle\src\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1387, 938)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.okBtn = PrimaryPushButton(self.centralwidget)
        self.okBtn.setGeometry(QtCore.QRect(1220, 610, 91, 32))
        self.okBtn.setObjectName("okBtn")
        self.score = LineEdit(self.centralwidget)
        self.score.setGeometry(QtCore.QRect(1200, 520, 128, 33))
        self.score.setObjectName("score")
        self.StrongBodyLabel = StrongBodyLabel(self.centralwidget)
        self.StrongBodyLabel.setGeometry(QtCore.QRect(1150, 530, 41, 19))
        self.StrongBodyLabel.setObjectName("StrongBodyLabel")
        self.stuID = LineEdit(self.centralwidget)
        self.stuID.setGeometry(QtCore.QRect(1200, 440, 128, 33))
        self.stuID.setObjectName("stuID")
        self.StrongBodyLabel_2 = StrongBodyLabel(self.centralwidget)
        self.StrongBodyLabel_2.setGeometry(QtCore.QRect(1150, 440, 41, 19))
        self.StrongBodyLabel_2.setObjectName("StrongBodyLabel_2")
        self.stuName = LineEdit(self.centralwidget)
        self.stuName.setGeometry(QtCore.QRect(1200, 350, 128, 33))
        self.stuName.setObjectName("stuName")
        self.StrongBodyLabel_3 = StrongBodyLabel(self.centralwidget)
        self.StrongBodyLabel_3.setGeometry(QtCore.QRect(1150, 360, 41, 19))
        self.StrongBodyLabel_3.setObjectName("StrongBodyLabel_3")
        self.StrongBodyLabel_4 = StrongBodyLabel(self.centralwidget)
        self.StrongBodyLabel_4.setGeometry(QtCore.QRect(1150, 280, 41, 19))
        self.StrongBodyLabel_4.setObjectName("StrongBodyLabel_4")
        self.labName = LineEdit(self.centralwidget)
        self.labName.setGeometry(QtCore.QRect(1200, 270, 128, 33))
        self.labName.setObjectName("labName")
        self.exportBtn = PrimaryPushButton(self.centralwidget)
        self.exportBtn.setGeometry(QtCore.QRect(1220, 670, 91, 32))
        self.exportBtn.setObjectName("exportBtn")
        self.preDocBtn = PrimaryPushButton(self.centralwidget)
        self.preDocBtn.setGeometry(QtCore.QRect(1220, 730, 91, 32))
        self.preDocBtn.setObjectName("preDocBtn")
        self.nextDocBtn = PrimaryPushButton(self.centralwidget)
        self.nextDocBtn.setGeometry(QtCore.QRect(1220, 790, 91, 32))
        self.nextDocBtn.setObjectName("nextDocBtn")
        self.Comments = TextEdit(self.centralwidget)
        self.Comments.setGeometry(QtCore.QRect(1150, 50, 201, 201))
        self.Comments.setObjectName("Comments")
        self.selModeBox = ComboBox(self.centralwidget)
        self.selModeBox.setGeometry(QtCore.QRect(1150, 10, 201, 32))
        self.selModeBox.setObjectName("selModeBox")
        self.fileList = ListView(self.centralwidget)
        self.fileList.setGeometry(QtCore.QRect(10, 0, 261, 891))
        self.fileList.setObjectName("fileList")
        self.contentWidget = ListWidget(self.centralwidget)
        self.contentWidget.setGeometry(QtCore.QRect(290, 0, 831, 891))
        self.contentWidget.setObjectName("contentWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1387, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.okBtn.setText(_translate("MainWindow", "确认评分"))
        self.StrongBodyLabel.setText(_translate("MainWindow", "评分"))
        self.StrongBodyLabel_2.setText(_translate("MainWindow", "学号"))
        self.StrongBodyLabel_3.setText(_translate("MainWindow", "姓名"))
        self.StrongBodyLabel_4.setText(_translate("MainWindow", "实验"))
        self.exportBtn.setText(_translate("MainWindow", "导出评分"))
        self.preDocBtn.setText(_translate("MainWindow", "上一篇"))
        self.nextDocBtn.setText(_translate("MainWindow", "下一篇"))


from qfluentwidgets import (
    ComboBox,
    LineEdit,
    ListView,
    ListWidget,
    PrimaryPushButton,
    StrongBodyLabel,
    TextEdit,
)
