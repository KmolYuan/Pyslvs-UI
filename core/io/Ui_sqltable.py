# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/io/sqltable.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(625, 636)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FileTable = QtWidgets.QTableWidget(Form)
        self.FileTable.setObjectName("FileTable")
        self.FileTable.setColumnCount(6)
        self.FileTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.FileTable.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.FileTable)
        self.FileDescription_text = QtWidgets.QLabel(Form)
        self.FileDescription_text.setObjectName("FileDescription_text")
        self.verticalLayout.addWidget(self.FileDescription_text)
        self.FileDescription = QtWidgets.QLineEdit(Form)
        self.FileDescription.setObjectName("FileDescription")
        self.verticalLayout.addWidget(self.FileDescription)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.commit_button = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/git.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commit_button.setIcon(icon)
        self.commit_button.setObjectName("commit_button")
        self.horizontalLayout_4.addWidget(self.commit_button)
        self.branch_button = QtWidgets.QPushButton(Form)
        self.branch_button.setIcon(icon)
        self.branch_button.setObjectName("branch_button")
        self.horizontalLayout_4.addWidget(self.branch_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.stash_button = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stash_button.setIcon(icon1)
        self.stash_button.setObjectName("stash_button")
        self.horizontalLayout_4.addWidget(self.stash_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.FileTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.FileTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Date"))
        item = self.FileTable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Description"))
        item = self.FileTable.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Author"))
        item = self.FileTable.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Previous"))
        item = self.FileTable.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Branch"))
        self.FileDescription_text.setText(_translate("Form", "Description:"))
        self.commit_button.setText(_translate("Form", "Commit"))
        self.branch_button.setText(_translate("Form", "Branch"))
        self.stash_button.setText(_translate("Form", "Stash"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

