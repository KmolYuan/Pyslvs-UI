# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ahshoe\Desktop\Pyslvs-PyQt5\core\synthesis\Collections\TriangularIteration_dialog\constraints.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(422, 360)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/collection-triangular-iteration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.main_label = QtWidgets.QLabel(Dialog)
        self.main_label.setWordWrap(True)
        self.main_label.setObjectName("main_label")
        self.verticalLayout_6.addWidget(self.main_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Loops_label = QtWidgets.QLabel(Dialog)
        self.Loops_label.setObjectName("Loops_label")
        self.verticalLayout_3.addWidget(self.Loops_label)
        self.Loops_list = QtWidgets.QListWidget(Dialog)
        self.Loops_list.setObjectName("Loops_list")
        self.verticalLayout_3.addWidget(self.Loops_list)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.sorting_label = QtWidgets.QLabel(Dialog)
        self.sorting_label.setObjectName("sorting_label")
        self.verticalLayout_4.addWidget(self.sorting_label)
        self.sorting_list = QtWidgets.QListWidget(Dialog)
        self.sorting_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.sorting_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.sorting_list.setObjectName("sorting_list")
        self.verticalLayout_4.addWidget(self.sorting_list)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_add = QtWidgets.QPushButton(Dialog)
        self.main_add.setMaximumSize(QtCore.QSize(30, 16777215))
        self.main_add.setObjectName("main_add")
        self.verticalLayout_2.addWidget(self.main_add)
        self.sorting_add = QtWidgets.QPushButton(Dialog)
        self.sorting_add.setMaximumSize(QtCore.QSize(30, 16777215))
        self.sorting_add.setObjectName("sorting_add")
        self.verticalLayout_2.addWidget(self.sorting_add)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.main_list = QtWidgets.QListWidget(Dialog)
        self.main_list.setObjectName("main_list")
        self.verticalLayout_5.addWidget(self.main_list)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Constrains"))
        self.main_label.setText(_translate("Dialog", "Four bar loop in this structure can be apply Gruebler\'s Equation to keep the path integrity."))
        self.Loops_label.setText(_translate("Dialog", "Loops:"))
        self.label_2.setText(_translate("Dialog", ">>"))
        self.sorting_label.setText(_translate("Dialog", "Sorting:"))
        self.main_add.setText(_translate("Dialog", ">>"))
        self.sorting_add.setText(_translate("Dialog", "<<"))
        self.label.setText(_translate("Dialog", "Constrains:"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

