# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/repeated_value.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_same_value(object):
    def setupUi(self, Warning_same_value):
        Warning_same_value.setObjectName("Warning_same_value")
        Warning_same_value.resize(411, 170)
        Warning_same_value.setMinimumSize(QtCore.QSize(411, 170))
        Warning_same_value.setMaximumSize(QtCore.QSize(411, 170))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_same_value.setWindowIcon(icon)
        Warning_same_value.setSizeGripEnabled(False)
        Warning_same_value.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Warning_same_value)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Warning_same_value)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_same_value)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Warning_same_value)
        self.buttonBox.accepted.connect(Warning_same_value.accept)
        QtCore.QMetaObject.connectSlotsByName(Warning_same_value)

    def retranslateUi(self, Warning_same_value):
        _translate = QtCore.QCoreApplication.translate
        Warning_same_value.setWindowTitle(_translate("Warning_same_value", "Warning - Same Value"))
        self.label.setText(_translate("Warning_same_value", "<html><head/><body><p><span style=\" font-size:14pt;\">Can\'t use two same Essential elements.</span></p><p><span style=\" font-size:14pt;\">Please choose another requre entity.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_same_value = QtWidgets.QDialog()
    ui = Ui_Warning_same_value()
    ui.setupUi(Warning_same_value)
    Warning_same_value.show()
    sys.exit(app.exec_())

