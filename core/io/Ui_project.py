# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/io/project.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from core.QtModules import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(431, 680)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/data.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.file_name_title = QtWidgets.QLabel(Form)
        self.file_name_title.setObjectName("file_name_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.file_name_title)
        self.file_name_label = QtWidgets.QLineEdit(Form)
        self.file_name_label.setReadOnly(True)
        self.file_name_label.setObjectName("file_name_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.file_name_label)
        self.path_title = QtWidgets.QLabel(Form)
        self.path_title.setObjectName("path_title")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.path_title)
        self.path_label = QtWidgets.QLineEdit(Form)
        self.path_label.setReadOnly(True)
        self.path_label.setObjectName("path_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.path_label)
        self.last_modified_title = QtWidgets.QLabel(Form)
        self.last_modified_title.setObjectName("last_modified_title")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.last_modified_title)
        self.last_modified_label = QtWidgets.QLabel(Form)
        self.last_modified_label.setObjectName("last_modified_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.last_modified_label)
        self.file_size_title = QtWidgets.QLabel(Form)
        self.file_size_title.setObjectName("file_size_title")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.file_size_title)
        self.file_size_label = QtWidgets.QLabel(Form)
        self.file_size_label.setObjectName("file_size_label")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.file_size_label)
        self.type_title = QtWidgets.QLabel(Form)
        self.type_title.setObjectName("type_title")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.type_title)
        self.type_label = QtWidgets.QLabel(Form)
        self.type_label.setObjectName("type_label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.type_label)
        self.owner_title = QtWidgets.QLabel(Form)
        self.owner_title.setObjectName("owner_title")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.owner_title)
        self.owner_label = QtWidgets.QLabel(Form)
        self.owner_label.setObjectName("owner_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.owner_label)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.file_name_title.setText(_translate("Form", "File name:"))
        self.path_title.setText(_translate("Form", "Path:"))
        self.last_modified_title.setText(_translate("Form", "Last modified:"))
        self.file_size_title.setText(_translate("Form", "File size:"))
        self.type_title.setText(_translate("Form", "Type:"))
        self.owner_title.setText(_translate("Form", "Owner:"))
import icons_rc
