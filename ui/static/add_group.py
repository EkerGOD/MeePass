# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_group.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(527, 349)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.General_tab = QtWidgets.QWidget()
        self.General_tab.setObjectName("General_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.General_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_horizontalLayout = QtWidgets.QHBoxLayout()
        self.name_horizontalLayout.setObjectName("name_horizontalLayout")
        self.name_label = QtWidgets.QLabel(self.General_tab)
        self.name_label.setMinimumSize(QtCore.QSize(90, 0))
        self.name_label.setMaximumSize(QtCore.QSize(90, 16777215))
        self.name_label.setObjectName("name_label")
        self.name_horizontalLayout.addWidget(self.name_label)
        self.name_lineEdit = QtWidgets.QLineEdit(self.General_tab)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.name_horizontalLayout.addWidget(self.name_lineEdit)
        self.verticalLayout_2.addLayout(self.name_horizontalLayout)
        self.icon_horizontalLayout = QtWidgets.QHBoxLayout()
        self.icon_horizontalLayout.setObjectName("icon_horizontalLayout")
        self.icon_label = QtWidgets.QLabel(self.General_tab)
        self.icon_label.setMinimumSize(QtCore.QSize(90, 0))
        self.icon_label.setMaximumSize(QtCore.QSize(90, 16777215))
        self.icon_label.setObjectName("icon_label")
        self.icon_horizontalLayout.addWidget(self.icon_label)
        self.icon_toolButton = QtWidgets.QToolButton(self.General_tab)
        self.icon_toolButton.setObjectName("icon_toolButton")
        self.icon_horizontalLayout.addWidget(self.icon_toolButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.icon_horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.icon_horizontalLayout)
        self.notes_horizontalLayout = QtWidgets.QHBoxLayout()
        self.notes_horizontalLayout.setObjectName("notes_horizontalLayout")
        self.notes_label = QtWidgets.QLabel(self.General_tab)
        self.notes_label.setMinimumSize(QtCore.QSize(90, 0))
        self.notes_label.setMaximumSize(QtCore.QSize(90, 16777215))
        self.notes_label.setObjectName("notes_label")
        self.notes_horizontalLayout.addWidget(self.notes_label)
        self.notes_textEdit = QtWidgets.QTextEdit(self.General_tab)
        self.notes_textEdit.setObjectName("notes_textEdit")
        self.notes_horizontalLayout.addWidget(self.notes_textEdit)
        self.verticalLayout_2.addLayout(self.notes_horizontalLayout)
        self.expires_horizontalLayout = QtWidgets.QHBoxLayout()
        self.expires_horizontalLayout.setObjectName("expires_horizontalLayout")
        self.expires_checkBox = QtWidgets.QCheckBox(self.General_tab)
        self.expires_checkBox.setMaximumSize(QtCore.QSize(90, 16777215))
        self.expires_checkBox.setObjectName("expires_checkBox")
        self.expires_horizontalLayout.addWidget(self.expires_checkBox)
        self.expires_dateTimeEdit = QtWidgets.QDateTimeEdit(self.General_tab)
        self.expires_dateTimeEdit.setObjectName("expires_dateTimeEdit")
        self.expires_horizontalLayout.addWidget(self.expires_dateTimeEdit)
        self.verticalLayout_2.addLayout(self.expires_horizontalLayout)
        self.tabWidget.addTab(self.General_tab, "")
        self.Properties_tab = QtWidgets.QWidget()
        self.Properties_tab.setObjectName("Properties_tab")
        self.tabWidget.addTab(self.Properties_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.pushButton_horizontalLayout = QtWidgets.QHBoxLayout()
        self.pushButton_horizontalLayout.setObjectName("pushButton_horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.pushButton_horizontalLayout.addItem(spacerItem1)
        self.OK_pushButton = QtWidgets.QPushButton(Form)
        self.OK_pushButton.setObjectName("OK_pushButton")
        self.pushButton_horizontalLayout.addWidget(self.OK_pushButton)
        self.cancel_pushButton = QtWidgets.QPushButton(Form)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.pushButton_horizontalLayout.addWidget(self.cancel_pushButton)
        self.verticalLayout.addLayout(self.pushButton_horizontalLayout)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Add Group"))
        self.name_label.setText(_translate("Form", "Name:"))
        self.icon_label.setText(_translate("Form", "Icon:"))
        self.icon_toolButton.setText(_translate("Form", "..."))
        self.notes_label.setText(_translate("Form", "Notes:"))
        self.expires_checkBox.setText(_translate("Form", "Expires:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General_tab), _translate("Form", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Properties_tab), _translate("Form", "Properties"))
        self.OK_pushButton.setText(_translate("Form", "OK"))
        self.cancel_pushButton.setText(_translate("Form", "Cancel"))
