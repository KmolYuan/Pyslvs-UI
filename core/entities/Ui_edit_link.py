# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/桌面/Pyslvs-PyQt5/core/entities/edit_link.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(314, 325)
        Dialog.setMinimumSize(QtCore.QSize(314, 325))
        Dialog.setMaximumSize(QtCore.QSize(314, 325))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(True)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QtWidgets.QLabel(Dialog)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.Link = QtWidgets.QComboBox(Dialog)
        self.Link.setObjectName("Link")
        self.verticalLayout.addWidget(self.Link)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.name_edit = QtWidgets.QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.horizontalLayout_2.addWidget(self.name_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.color_label = QtWidgets.QLabel(Dialog)
        self.color_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.color_label.setObjectName("color_label")
        self.verticalLayout.addWidget(self.color_label)
        self.Color = QtWidgets.QComboBox(Dialog)
        self.Color.setObjectName("Color")
        self.verticalLayout.addWidget(self.Color)
        self.point_label = QtWidgets.QLabel(Dialog)
        self.point_label.setObjectName("point_label")
        self.verticalLayout.addWidget(self.point_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.noSelected = QtWidgets.QListWidget(Dialog)
        self.noSelected.setDragEnabled(True)
        self.noSelected.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.noSelected.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.noSelected.setObjectName("noSelected")
        self.horizontalLayout.addWidget(self.noSelected)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.selected = QtWidgets.QListWidget(Dialog)
        self.selected.setDragEnabled(True)
        self.selected.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.selected.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.selected.setObjectName("selected")
        self.horizontalLayout.addWidget(self.selected)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Link"))
        self.name_label.setText(_translate("Dialog", "Name:"))
        self.color_label.setText(_translate("Dialog", "Color:"))
        self.point_label.setText(_translate("Dialog", "Points:"))
        self.label.setText(_translate("Dialog", ">>"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

