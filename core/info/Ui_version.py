# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ahshoe\Desktop\Pyslvs-PyQt5\core\info\version.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About_Dialog(object):
    def setupUi(self, About_Dialog):
        About_Dialog.setObjectName("About_Dialog")
        About_Dialog.setEnabled(True)
        About_Dialog.resize(400, 354)
        About_Dialog.setMinimumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About_Dialog.setWindowIcon(icon)
        About_Dialog.setAutoFillBackground(True)
        About_Dialog.setSizeGripEnabled(False)
        About_Dialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(About_Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.iconLabel = QtWidgets.QLabel(About_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setText("")
        self.iconLabel.setPixmap(QtGui.QPixmap(":/icons/main.png"))
        self.iconLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.iconLabel.setObjectName("iconLabel")
        self.verticalLayout_2.addWidget(self.iconLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.versionLabel = QtWidgets.QLabel(About_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLabel.sizePolicy().hasHeightForWidth())
        self.versionLabel.setSizePolicy(sizePolicy)
        self.versionLabel.setText("")
        self.versionLabel.setObjectName("versionLabel")
        self.verticalLayout.addWidget(self.versionLabel)
        self.Content = QtWidgets.QLabel(About_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Content.sizePolicy().hasHeightForWidth())
        self.Content.setSizePolicy(sizePolicy)
        self.Content.setText("")
        self.Content.setTextFormat(QtCore.Qt.RichText)
        self.Content.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Content.setWordWrap(True)
        self.Content.setOpenExternalLinks(True)
        self.Content.setObjectName("Content")
        self.verticalLayout.addWidget(self.Content)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(About_Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(About_Dialog)
        self.buttonBox.accepted.connect(About_Dialog.accept)
        self.buttonBox.rejected.connect(About_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(About_Dialog)

    def retranslateUi(self, About_Dialog):
        _translate = QtCore.QCoreApplication.translate
        About_Dialog.setWindowTitle(_translate("About_Dialog", "About Pyslvs"))
        self.iconLabel.setWhatsThis(_translate("About_Dialog", "Pyslvs Icon!"))
        self.Content.setWhatsThis(_translate("About_Dialog", "Version Info"))
        self.buttonBox.setWhatsThis(_translate("About_Dialog", "Click to exit"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    About_Dialog = QtWidgets.QDialog()
    ui = Ui_About_Dialog()
    ui.setupUi(About_Dialog)
    About_Dialog.show()
    sys.exit(app.exec_())

