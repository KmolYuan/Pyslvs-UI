# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/io/script.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from core.QtModules import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(520, 564)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/script.png"), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(True)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.main_layout = QVBoxLayout(Dialog)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.style_option = QComboBox(Dialog)
        self.style_option.setObjectName("style_option")
        self.horizontalLayout_2.addWidget(self.style_option)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.copy = QPushButton(Dialog)
        self.copy.setContextMenuPolicy(Qt.NoContextMenu)
        self.copy.setAutoDefault(False)
        self.copy.setObjectName("copy")
        self.horizontalLayout_2.addWidget(self.copy)
        self.save = QPushButton(Dialog)
        self.save.setAutoDefault(False)
        self.save.setObjectName("save")
        self.horizontalLayout_2.addWidget(self.save)
        self.main_layout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_box = QDialogButtonBox(Dialog)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Close)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.main_layout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.button_box.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        self.label_2.setText(_translate("Dialog", "Style:"))
        self.copy.setText(_translate("Dialog", "Copy"))
        self.save.setText(_translate("Dialog", "Save as..."))
        self.label_3.setText(_translate("Dialog", "Syntax highlighting powered by Pygments."))
        self.button_box.setWhatsThis(_translate("Dialog", "Click to exit"))


import icons_rc
