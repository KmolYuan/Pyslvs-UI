# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/info/color.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Info_Dialog(object):
    def setupUi(self, Info_Dialog):
        Info_Dialog.setObjectName("Info_Dialog")
        Info_Dialog.setEnabled(True)
        Info_Dialog.resize(400, 452)
        Info_Dialog.setMinimumSize(QtCore.QSize(400, 452))
        Info_Dialog.setMaximumSize(QtCore.QSize(400, 452))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/in3d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Info_Dialog.setWindowIcon(icon)
        Info_Dialog.setAutoFillBackground(True)
        Info_Dialog.setSizeGripEnabled(False)
        Info_Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Info_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 380, 111, 71))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Info_Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 20, 271, 421))
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
        Info_Dialog.setWindowTitle(_translate("Info_Dialog", "Color Settings"))
        self.buttonBox.setWhatsThis(_translate("Info_Dialog", "Click to exit"))
        self.label_2.setWhatsThis(_translate("Info_Dialog", "Version Info"))
        self.label_2.setText(_translate("Info_Dialog", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Color Settings</span></p><p><span style=\" font-size:12pt;\">*D: Dark Side</span></p><p><span style=\" font-size:12pt;\">- R: Red</span></p><p><span style=\" font-size:12pt;\">- G: Green</span></p><p><span style=\" font-size:12pt;\">- B: Blue</span></p><p><span style=\" font-size:12pt;\">- C: Cyan</span></p><p><span style=\" font-size:12pt;\">- M: Magenta</span></p><p><span style=\" font-size:12pt;\">- Y: Yellow</span></p><p><span style=\" font-size:12pt;\">- Gy: Gray</span></p><p><span style=\" font-size:12pt;\">- Og: Orange</span></p><p><span style=\" font-size:12pt;\">- Pk: Pink</span></p><p><span style=\" font-size:12pt;\">- Bk: Black / W: White</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Info_Dialog = QtWidgets.QDialog()
    ui = Ui_Info_Dialog()
    ui.setupUi(Info_Dialog)
    Info_Dialog.show()
    sys.exit(app.exec_())

