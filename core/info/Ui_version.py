# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/info/version.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About_Dialog(object):
    def setupUi(self, About_Dialog):
        About_Dialog.setObjectName("About_Dialog")
        About_Dialog.setEnabled(True)
        About_Dialog.resize(400, 300)
        About_Dialog.setMinimumSize(QtCore.QSize(400, 300))
        About_Dialog.setMaximumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About_Dialog.setWindowIcon(icon)
        About_Dialog.setAutoFillBackground(True)
        About_Dialog.setSizeGripEnabled(False)
        About_Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(About_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(260, 220, 111, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(About_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/main.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(About_Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 20, 311, 191))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(About_Dialog)
        self.buttonBox.accepted.connect(About_Dialog.accept)
        self.buttonBox.rejected.connect(About_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(About_Dialog)

    def retranslateUi(self, About_Dialog):
        _translate = QtCore.QCoreApplication.translate
        About_Dialog.setWindowTitle(_translate("About_Dialog", "About Pyslvs"))
        self.buttonBox.setWhatsThis(_translate("About_Dialog", "Click to exit"))
        self.label.setWhatsThis(_translate("About_Dialog", "Pyslvs Icon!"))
        self.label_2.setWhatsThis(_translate("About_Dialog", "Version Info"))
        self.label_2.setText(_translate("About_Dialog", "<html><head/><body><p>Pyslvs version</p><p>Pyslvs is a Open Source support tools to help user solving 2D linkage problem.</p><p>It can use in Mechanical Design and Simulation.</p><p>This program using Python 3 with Python Solvespace.</p><p>If you want to know about more, you can refer to our website.</p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    About_Dialog = QtWidgets.QDialog()
    ui = Ui_About_Dialog()
    ui.setupUi(About_Dialog)
    About_Dialog.show()
    sys.exit(app.exec_())

