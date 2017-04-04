# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/panel/run_Drive_shaft.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(410, 213)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Shaft = QtWidgets.QComboBox(Form)
        self.Shaft.setObjectName("Shaft")
        self.horizontalLayout_2.addWidget(self.Shaft)
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Degree_text = QtWidgets.QDoubleSpinBox(Form)
        self.Degree_text.setMaximum(360.0)
        self.Degree_text.setSingleStep(10.0)
        self.Degree_text.setObjectName("Degree_text")
        self.horizontalLayout_2.addWidget(self.Degree_text)
        self.playButton = QtWidgets.QPushButton(Form)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Degree = QtWidgets.QDial(Form)
        self.Degree.setMaximum(36000)
        self.Degree.setSingleStep(100)
        self.Degree.setPageStep(1000)
        self.Degree.setInvertedAppearance(True)
        self.Degree.setWrapping(True)
        self.Degree.setNotchTarget(0.0045)
        self.Degree.setNotchesVisible(True)
        self.Degree.setObjectName("Degree")
        self.horizontalLayout.addWidget(self.Degree)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p>Drive the shaft to the specified angle.</p></body></html>"))
        self.label_2.setText(_translate("Form", " in Angle:"))
        self.Degree_text.setSuffix(_translate("Form", "°"))
        self.playButton.setToolTip(_translate("Form", "A 60-lap mechanism demo"))
        self.playButton.setText(_translate("Form", "Play"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

