# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/synthesis/collections/dialogs/targets.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from core.QtModules import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(346, 309)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/configure.png"), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout_4 = QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.main_label = QLabel(Dialog)
        self.main_label.setObjectName("main_label")
        self.verticalLayout_4.addWidget(self.main_label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.other_label = QLabel(Dialog)
        self.other_label.setObjectName("other_label")
        self.verticalLayout_3.addWidget(self.other_label)
        self.other_list = QListWidget(Dialog)
        self.other_list.setObjectName("other_list")
        self.verticalLayout_3.addWidget(self.other_list)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.targets_add = QPushButton(Dialog)
        self.targets_add.setMaximumSize(QSize(30, 16777215))
        self.targets_add.setObjectName("targets_add")
        self.verticalLayout.addWidget(self.targets_add)
        self.other_add = QPushButton(Dialog)
        self.other_add.setMaximumSize(QSize(30, 16777215))
        self.other_add.setObjectName("other_add")
        self.verticalLayout.addWidget(self.other_add)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.targets_label = QLabel(Dialog)
        self.targets_label.setObjectName("targets_label")
        self.verticalLayout_2.addWidget(self.targets_label)
        self.targets_list = QListWidget(Dialog)
        self.targets_list.setObjectName("targets_list")
        self.verticalLayout_2.addWidget(self.targets_list)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_box = QDialogButtonBox(Dialog)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout_2.addWidget(self.button_box)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept)
        self.button_box.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.main_label.setText(_translate("Dialog", "Choose the target point(s) to verify with path(s)."))
        self.other_label.setText(_translate("Dialog", "To be selected:"))
        self.targets_add.setText(_translate("Dialog", ">>"))
        self.other_add.setText(_translate("Dialog", "<<"))
        self.targets_label.setText(_translate("Dialog", "Tragets:"))


import icons_rc
