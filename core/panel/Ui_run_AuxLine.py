# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/panel/run_AuxLine.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(684, 75)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 75))
        Form.setMouseTracking(False)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Point = QtWidgets.QComboBox(self.groupBox)
        self.Point.setObjectName("Point")
        self.horizontalLayout.addWidget(self.Point)
        self.H_line = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.H_line.sizePolicy().hasHeightForWidth())
        self.H_line.setSizePolicy(sizePolicy)
        self.H_line.setChecked(True)
        self.H_line.setObjectName("H_line")
        self.horizontalLayout.addWidget(self.H_line)
        self.V_line = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V_line.sizePolicy().hasHeightForWidth())
        self.V_line.setSizePolicy(sizePolicy)
        self.V_line.setChecked(True)
        self.V_line.setObjectName("V_line")
        self.horizontalLayout.addWidget(self.V_line)
        self.Max_Limit = QtWidgets.QCheckBox(self.groupBox)
        self.Max_Limit.setChecked(True)
        self.Max_Limit.setObjectName("Max_Limit")
        self.horizontalLayout.addWidget(self.Max_Limit)
        self.Min_Limit = QtWidgets.QCheckBox(self.groupBox)
        self.Min_Limit.setChecked(True)
        self.Min_Limit.setObjectName("Min_Limit")
        self.horizontalLayout.addWidget(self.Min_Limit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Color = QtWidgets.QComboBox(self.groupBox)
        self.Color.setObjectName("Color")
        self.horizontalLayout.addWidget(self.Color)
        self.Color_l = QtWidgets.QComboBox(self.groupBox)
        self.Color_l.setObjectName("Color_l")
        self.horizontalLayout.addWidget(self.Color_l)
        self.horizontalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Auxiliary Line"))
        self.H_line.setText(_translate("Form", "Horizontal"))
        self.V_line.setText(_translate("Form", "Vertical"))
        self.Max_Limit.setText(_translate("Form", "Max Limit"))
        self.Min_Limit.setText(_translate("Form", "Min Limit"))
        self.label.setText(_translate("Form", "Color:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

