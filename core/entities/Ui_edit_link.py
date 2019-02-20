# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/entities/edit_link.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from core.QtModules import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(333, 467)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/link.png"), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.horizontalLayout_4 = QHBoxLayout(Dialog)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QLabel(Dialog)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.name_box = QComboBox(Dialog)
        self.name_box.setObjectName("name_box")
        self.verticalLayout.addWidget(self.name_box)
        self.name_edit = QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout.addWidget(self.name_edit)
        self.color_label = QLabel(Dialog)
        self.color_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.color_label.setObjectName("color_label")
        self.verticalLayout.addWidget(self.color_label)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.color_box = QComboBox(Dialog)
        self.color_box.setObjectName("color_box")
        self.horizontalLayout_2.addWidget(self.color_box)
        self.color_pick_button = QPushButton(Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.color_pick_button.sizePolicy().hasHeightForWidth())
        self.color_pick_button.setSizePolicy(sizePolicy)
        self.color_pick_button.setObjectName("color_pick_button")
        self.horizontalLayout_2.addWidget(self.color_pick_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.points_label = QLabel(Dialog)
        self.points_label.setObjectName("points_label")
        self.verticalLayout.addWidget(self.points_label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.noSelected = QListWidget(Dialog)
        self.noSelected.setDragEnabled(True)
        self.noSelected.setDragDropMode(QAbstractItemView.DragDrop)
        self.noSelected.setDefaultDropAction(Qt.MoveAction)
        self.noSelected.setObjectName("noSelected")
        self.horizontalLayout.addWidget(self.noSelected)
        self.label = QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.selected = QListWidget(Dialog)
        self.selected.setDragEnabled(True)
        self.selected.setDragDropMode(QAbstractItemView.DragDrop)
        self.selected.setDefaultDropAction(Qt.MoveAction)
        self.selected.setObjectName("selected")
        self.horizontalLayout.addWidget(self.selected)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_box = QDialogButtonBox(Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setOrientation(Qt.Vertical)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_2.addWidget(self.button_box)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Link"))
        self.name_label.setText(_translate("Dialog", "Name:"))
        self.color_label.setText(_translate("Dialog", "Emphatic Color:"))
        self.points_label.setText(_translate("Dialog", "Points:"))
        self.label.setText(_translate("Dialog", ">>"))


import icons_rc
