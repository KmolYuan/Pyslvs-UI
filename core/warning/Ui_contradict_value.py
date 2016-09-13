# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/contradict_value.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_contradict(object):
    def setupUi(self, contradict):
        contradict.setObjectName("contradict")
        contradict.resize(411, 211)
        contradict.setMinimumSize(QtCore.QSize(411, 211))
        contradict.setMaximumSize(QtCore.QSize(411, 211))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        contradict.setWindowIcon(icon)
        contradict.setSizeGripEnabled(False)
        contradict.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(contradict)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(contradict)
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
        self.buttonBox = QtWidgets.QDialogButtonBox(contradict)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(contradict)
        self.buttonBox.accepted.connect(contradict.accept)
        self.buttonBox.rejected.connect(contradict.reject)
        QtCore.QMetaObject.connectSlotsByName(contradict)

    def retranslateUi(self, contradict):
        _translate = QtCore.QCoreApplication.translate
        contradict.setWindowTitle(_translate("contradict", "Warning - Contradict Value"))
        self.label.setText(_translate("contradict", "<html><head/><body><p><span style=\" font-size:14pt;\">Some Duplicate constraint problem in your select.</span></p><p><span style=\" font-size:14pt;\">Please choose another requre entity.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    contradict = QtWidgets.QDialog()
    ui = Ui_contradict()
    ui.setupUi(contradict)
    contradict.show()
    sys.exit(app.exec_())

