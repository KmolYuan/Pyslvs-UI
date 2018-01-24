# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/桌面/Pyslvs-PyQt5/core/synthesis/Collections/TriangularIteration_dialog/solutions.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(768, 482)
        Dialog.setMinimumSize(QtCore.QSize(768, 482))
        Dialog.setMaximumSize(QtCore.QSize(768, 482))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/collection-triangular-iteration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_label = QtWidgets.QLabel(Dialog)
        self.main_label.setObjectName("main_label")
        self.verticalLayout_3.addWidget(self.main_label)
        self.graph_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_label.sizePolicy().hasHeightForWidth())
        self.graph_label.setSizePolicy(sizePolicy)
        self.graph_label.setPixmap(QtGui.QPixmap(":/icons/preview/PLAP.png"))
        self.graph_label.setObjectName("graph_label")
        self.verticalLayout_3.addWidget(self.graph_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.point_A_label = QtWidgets.QLabel(Dialog)
        self.point_A_label.setObjectName("point_A_label")
        self.horizontalLayout.addWidget(self.point_A_label)
        self.point_A = QtWidgets.QComboBox(Dialog)
        self.point_A.setObjectName("point_A")
        self.horizontalLayout.addWidget(self.point_A)
        self.point_B_label = QtWidgets.QLabel(Dialog)
        self.point_B_label.setObjectName("point_B_label")
        self.horizontalLayout.addWidget(self.point_B_label)
        self.point_B = QtWidgets.QComboBox(Dialog)
        self.point_B.setObjectName("point_B")
        self.horizontalLayout.addWidget(self.point_B)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.point_A_label.setText(_translate("Dialog", "A Point:"))
        self.point_B_label.setText(_translate("Dialog", "B Point:"))

import icons_rc
import preview_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

