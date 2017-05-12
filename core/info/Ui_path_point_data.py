# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/mde1a1/src/core/info/path_point_data.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Info_Dialog(object):
    def setupUi(self, Info_Dialog):
        Info_Dialog.setObjectName("Info_Dialog")
        Info_Dialog.setEnabled(True)
        Info_Dialog.resize(428, 485)
        Info_Dialog.setMinimumSize(QtCore.QSize(428, 485))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/bezier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Info_Dialog.setWindowIcon(icon)
        Info_Dialog.setAutoFillBackground(True)
        Info_Dialog.setSizeGripEnabled(True)
        Info_Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Info_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.path_data = QtWidgets.QTableWidget(Info_Dialog)
        self.path_data.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.path_data.setTabKeyNavigation(False)
        self.path_data.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.path_data.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.path_data.setObjectName("path_data")
        self.path_data.setColumnCount(4)
        self.path_data.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.path_data.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.path_data.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.path_data.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.path_data.setHorizontalHeaderItem(3, item)
        self.path_data.horizontalHeader().setDefaultSectionSize(75)
        self.path_data.horizontalHeader().setMinimumSectionSize(75)
        self.verticalLayout.addWidget(self.path_data)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Info_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Info_Dialog)
        self.buttonBox.rejected.connect(Info_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Info_Dialog)

    def retranslateUi(self, Info_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Info_Dialog.setWindowTitle(_translate("Info_Dialog", "Path Result"))
        self.path_data.setSortingEnabled(True)
        item = self.path_data.horizontalHeaderItem(0)
        item.setText(_translate("Info_Dialog", "Shaft"))
        item = self.path_data.horizontalHeaderItem(1)
        item.setText(_translate("Info_Dialog", "Point"))
        item = self.path_data.horizontalHeaderItem(2)
        item.setText(_translate("Info_Dialog", "x"))
        item = self.path_data.horizontalHeaderItem(3)
        item.setText(_translate("Info_Dialog", "y"))
        self.buttonBox.setWhatsThis(_translate("Info_Dialog", "Click to exit"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Info_Dialog = QtWidgets.QDialog()
    ui = Ui_Info_Dialog()
    ui.setupUi(Info_Dialog)
    Info_Dialog.show()
    sys.exit(app.exec_())

