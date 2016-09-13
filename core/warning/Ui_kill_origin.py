# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs/core/warning/kill_origin.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Warning_kill_origin(object):
    def setupUi(self, Warning_kill_origin):
        Warning_kill_origin.setObjectName("Warning_kill_origin")
        Warning_kill_origin.resize(411, 160)
        Warning_kill_origin.setMinimumSize(QtCore.QSize(411, 160))
        Warning_kill_origin.setMaximumSize(QtCore.QSize(411, 160))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Warning_kill_origin.setWindowIcon(icon)
        Warning_kill_origin.setSizeGripEnabled(False)
        Warning_kill_origin.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Warning_kill_origin)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Warning_kill_origin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/delete.png"))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(Warning_kill_origin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning_kill_origin)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Warning_kill_origin)
        self.buttonBox.accepted.connect(Warning_kill_origin.accept)
        QtCore.QMetaObject.connectSlotsByName(Warning_kill_origin)

    def retranslateUi(self, Warning_kill_origin):
        _translate = QtCore.QCoreApplication.translate
        Warning_kill_origin.setWindowTitle(_translate("Warning_kill_origin", "Warning - Kill Origin"))
        self.label.setText(_translate("Warning_kill_origin", "<html><head/><body><p><span style=\" font-size:20pt;\">I just stand HERE...</span></p><p><span style=\" font-size:10pt;\">Origin can\'t delete.</span></p></body></html>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Warning_kill_origin = QtWidgets.QDialog()
    ui = Ui_Warning_kill_origin()
    ui.setupUi(Warning_kill_origin)
    Warning_kill_origin.show()
    sys.exit(app.exec_())

