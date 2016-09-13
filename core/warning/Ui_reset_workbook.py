# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/reset_workbook.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_reset(object):
    def setupUi(self, Warning_reset):
        Warning_reset.setObjectName("Warning_reset")
        Warning_reset.resize(400, 150)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_reset.setWindowIcon(icon)
        Warning_reset.setSizeGripEnabled(False)
        Warning_reset.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Warning_reset)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Warning_reset)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.OK = QtWidgets.QPushButton(Warning_reset)
        self.OK.setObjectName("OK")
        self.horizontalLayout.addWidget(self.OK)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Warning_reset)
        self.OK.clicked.connect(Warning_reset.accept)
        QtCore.QMetaObject.connectSlotsByName(Warning_reset)

    def retranslateUi(self, Warning_reset):
        _translate = QtCore.QCoreApplication.translate
        Warning_reset.setWindowTitle(_translate("Warning_reset", "Warning - Reset"))
        self.label.setText(_translate("Warning_reset", "<html><head/><body><p><span style=\" font-size:14pt;\">Do you want to Clear ALL Drawings? <br/>The changes can\'t be recovery!</span></p></body></html>"))
        self.OK.setText(_translate("Warning_reset", "OK"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_reset = QtWidgets.QDialog()
    ui = Ui_Warning_reset()
    ui.setupUi(Warning_reset)
    Warning_reset.show()
    sys.exit(app.exec_())

