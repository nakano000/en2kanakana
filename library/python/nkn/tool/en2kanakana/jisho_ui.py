# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\en2kanakana\library\python\nkn\tool\en2kanakana\jisho.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\en2kanakana\library\python\nkn\tool\en2kanakana\jisho.ui' applies.
#
# Created: Fri Jun  3 13:44:30 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(458, 472)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.jishoTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.jishoTextEdit.setObjectName("jishoTextEdit")
        self.verticalLayout.addWidget(self.jishoTextEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.saveButton.setText(QtWidgets.QApplication.translate("Form", "保存", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Form", "キャンセル", None, -1))

