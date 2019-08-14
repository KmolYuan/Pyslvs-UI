# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/io/script.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from core.QtModules import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(520, 564)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/script.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setAutoFillBackground(True)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.style_option = QtWidgets.QComboBox(Dialog)
        self.style_option.setObjectName("style_option")
        self.horizontalLayout_2.addWidget(self.style_option)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.copy = QtWidgets.QPushButton(Dialog)
        self.copy.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.copy.setAutoDefault(False)
        self.copy.setObjectName("copy")
        self.horizontalLayout_2.addWidget(self.copy)
        self.save_qrcode = QtWidgets.QPushButton(Dialog)
        self.save_qrcode.setAutoDefault(False)
        self.save_qrcode.setObjectName("save_qrcode")
        self.horizontalLayout_2.addWidget(self.save_qrcode)
        self.save_script = QtWidgets.QPushButton(Dialog)
        self.save_script.setAutoDefault(False)
        self.save_script.setObjectName("save_script")
        self.horizontalLayout_2.addWidget(self.save_script)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.main_splitter = QtWidgets.QSplitter(Dialog)
        self.main_splitter.setObjectName("main_splitter")
        self.scroll_area = QtWidgets.QScrollArea(self.main_splitter)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.qrcode_widget = QtWidgets.QWidget()
        self.qrcode_widget.setGeometry(QtCore.QRect(0, 0, 500, 176))
        self.qrcode_widget.setObjectName("qrcode_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.qrcode_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.qrcode_image = QtWidgets.QLabel(self.qrcode_widget)
        self.qrcode_image.setAlignment(QtCore.Qt.AlignCenter)
        self.qrcode_image.setObjectName("qrcode_image")
        self.verticalLayout_2.addWidget(self.qrcode_image)
        self.scroll_area.setWidget(self.qrcode_widget)
        self.verticalLayout.addWidget(self.main_splitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_box.sizePolicy().hasHeightForWidth())
        self.button_box.setSizePolicy(sizePolicy)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.button_box.setObjectName("button_box")
        self.horizontalLayout.addWidget(self.button_box)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.button_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Dialog", "Style:"))
        self.copy.setText(_translate("Dialog", "Copy"))
        self.save_qrcode.setText(_translate("Dialog", "Save QR code"))
        self.save_script.setText(_translate("Dialog", "Save script"))
        self.label_3.setText(_translate("Dialog", "Syntax highlighting powered by Pygments."))
        self.button_box.setWhatsThis(_translate("Dialog", "Click to exit"))
import icons_rc
