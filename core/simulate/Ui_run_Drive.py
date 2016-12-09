# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ahshoe\Desktop\Pyslvs-PyQt5\core\simulate\run_Drive.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 82)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 82))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 500))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Shaft = QtWidgets.QComboBox(self.groupBox)
        self.Shaft.setObjectName("Shaft")
        self.horizontalLayout_2.addWidget(self.Shaft)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Degree = QtWidgets.QSlider(self.groupBox)
        self.Degree.setMaximum(36000)
        self.Degree.setSingleStep(1000)
        self.Degree.setPageStep(1000)
        self.Degree.setOrientation(QtCore.Qt.Horizontal)
        self.Degree.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.Degree.setTickInterval(9000)
        self.Degree.setObjectName("Degree")
        self.horizontalLayout_2.addWidget(self.Degree)
        self.Degree_text = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.Degree_text.setMaximum(360.0)
        self.Degree_text.setSingleStep(10.0)
        self.Degree_text.setObjectName("Degree_text")
        self.horizontalLayout_2.addWidget(self.Degree_text)
        self.playButton = QtWidgets.QPushButton(self.groupBox)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Drive Shaft"))
        self.label_2.setText(_translate("Form", "in Angle:"))
        self.Degree_text.setSuffix(_translate("Form", "°"))
        self.playButton.setText(_translate("Form", "Play"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

