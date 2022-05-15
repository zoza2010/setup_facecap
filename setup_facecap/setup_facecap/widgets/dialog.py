# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\my_dev\setup_facecap\ui\dialog.ui'
#
# Created: Mon May 16 02:03:05 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 109)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.useTweakCheckBox = QtWidgets.QCheckBox(Form)
        self.useTweakCheckBox.setChecked(True)
        self.useTweakCheckBox.setObjectName("useTweakCheckBox")
        self.verticalLayout.addWidget(self.useTweakCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.configsLabel = QtWidgets.QLabel(Form)
        self.configsLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        self.configsLabel.setObjectName("configsLabel")
        self.horizontalLayout.addWidget(self.configsLabel)
        self.configsComboBox = QtWidgets.QComboBox(Form)
        self.configsComboBox.setObjectName("configsComboBox")
        self.horizontalLayout.addWidget(self.configsComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setupPushButton = QtWidgets.QPushButton(Form)
        self.setupPushButton.setObjectName("setupPushButton")
        self.verticalLayout.addWidget(self.setupPushButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.useTweakCheckBox.setText(QtWidgets.QApplication.translate("Form", "use tweak", None, -1))
        self.configsLabel.setText(QtWidgets.QApplication.translate("Form", "configs:", None, -1))
        self.setupPushButton.setText(QtWidgets.QApplication.translate("Form", "setup", None, -1))

