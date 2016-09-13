# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/info/info.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Info_Dialog(object):
    def setupUi(self, Info_Dialog):
        Info_Dialog.setObjectName("Info_Dialog")
        Info_Dialog.setEnabled(True)
        Info_Dialog.resize(400, 300)
        Info_Dialog.setMinimumSize(QtCore.QSize(400, 300))
        Info_Dialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Info_Dialog.setWindowIcon(icon)
        Info_Dialog.setAutoFillBackground(True)
        Info_Dialog.setSizeGripEnabled(False)
        Info_Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Info_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(260, 220, 111, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Info_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/main.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Info_Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 20, 311, 191))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Info_Dialog)
        self.buttonBox.accepted.connect(Info_Dialog.accept)
        self.buttonBox.rejected.connect(Info_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Info_Dialog)

    def retranslateUi(self, Info_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Info_Dialog.setWindowTitle(_translate("Info_Dialog", "About Python Solvespace"))
        self.buttonBox.setWhatsThis(_translate("Info_Dialog", "Click to exit"))
        self.label.setWhatsThis(_translate("Info_Dialog", "Pyslvs Icon!"))
        self.label_2.setWhatsThis(_translate("Info_Dialog", "Version Info"))
        self.label_2.setText(_translate("Info_Dialog", "<html><head/><body><p>Python Solvespace</p><p>Library of Solvspace, within a interface of Python.</p><p>So any python script can using it in 2D or 3D computing problem-solving.</p><p>It use like Solvespace, but maybe not so convenience.</p><p>So Pyslvs will make up for shortcomings of Python Solvespace.</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Info_Dialog = QtWidgets.QDialog()
    ui = Ui_Info_Dialog()
    ui.setupUi(Info_Dialog)
    Info_Dialog.show()
    sys.exit(app.exec_())

