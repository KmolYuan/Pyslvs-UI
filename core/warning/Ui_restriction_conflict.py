# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/warning/restriction_conflict.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Restriction_Conflict(object):
    def setupUi(self, Restriction_Conflict):
        Restriction_Conflict.setObjectName("Restriction_Conflict")
        Restriction_Conflict.resize(411, 211)
        Restriction_Conflict.setMinimumSize(QtCore.QSize(411, 211))
        Restriction_Conflict.setMaximumSize(QtCore.QSize(411, 211))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Restriction_Conflict.setWindowIcon(icon)
        Restriction_Conflict.setSizeGripEnabled(False)
        Restriction_Conflict.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Restriction_Conflict)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Restriction_Conflict)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Restriction_Conflict)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Restriction_Conflict)
        self.buttonBox.accepted.connect(Restriction_Conflict.accept)
        self.buttonBox.rejected.connect(Restriction_Conflict.reject)
        QtCore.QMetaObject.connectSlotsByName(Restriction_Conflict)

    def retranslateUi(self, Restriction_Conflict):
        _translate = QtCore.QCoreApplication.translate
        Restriction_Conflict.setWindowTitle(_translate("Restriction_Conflict", "Warning - Restriction Conflict"))
        self.label.setText(_translate("Restriction_Conflict", "<html><head/><body><p><span style=\" font-size:14pt;\">Some problem in your select.</span></p><p><span style=\" font-size:14pt;\">Please check whether it is logical or not.</span></p><p><span style=\" font-size:14pt;\">And choose another requre entity.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Restriction_Conflict = QtWidgets.QDialog()
    ui = Ui_Restriction_Conflict()
    ui.setupUi(Restriction_Conflict)
    Restriction_Conflict.show()
    sys.exit(app.exec_())

