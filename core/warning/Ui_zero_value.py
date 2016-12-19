# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/warning/zero_value.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_no_value(object):
    def setupUi(self, Warning_no_value):
        Warning_no_value.setObjectName("Warning_no_value")
        Warning_no_value.resize(411, 160)
        Warning_no_value.setMinimumSize(QtCore.QSize(411, 160))
        Warning_no_value.setMaximumSize(QtCore.QSize(411, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_no_value.setWindowIcon(icon)
        Warning_no_value.setSizeGripEnabled(False)
        Warning_no_value.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Warning_no_value)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Warning_no_value)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_no_value)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Warning_no_value)
        self.buttonBox.accepted.connect(Warning_no_value.accept)
        self.buttonBox.rejected.connect(Warning_no_value.reject)
        QtCore.QMetaObject.connectSlotsByName(Warning_no_value)

    def retranslateUi(self, Warning_no_value):
        _translate = QtCore.QCoreApplication.translate
        Warning_no_value.setWindowTitle(_translate("Warning_no_value", "Warning - No Value"))
        self.label.setText(_translate("Warning_no_value", "<html><head/><body><p><span style=\" font-size:14pt;\">Can\'t find any Essential elements.</span></p><p><span style=\" font-size:14pt;\">Please add some requre entities.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_no_value = QtWidgets.QDialog()
    ui = Ui_Warning_no_value()
    ui.setupUi(Warning_no_value)
    Warning_no_value.show()
    sys.exit(app.exec_())

