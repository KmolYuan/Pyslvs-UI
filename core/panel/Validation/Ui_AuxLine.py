# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ahshoe\Desktop\Pyslvs-PyQt5\core\panel\Validation\AuxLine.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(428, 175)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMouseTracking(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Point = QtWidgets.QComboBox(Form)
        self.Point.setObjectName("Point")
        self.horizontalLayout.addWidget(self.Point)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.H_line = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.H_line.sizePolicy().hasHeightForWidth())
        self.H_line.setSizePolicy(sizePolicy)
        self.H_line.setChecked(True)
        self.H_line.setObjectName("H_line")
        self.horizontalLayout_3.addWidget(self.H_line)
        self.V_line = QtWidgets.QCheckBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V_line.sizePolicy().hasHeightForWidth())
        self.V_line.setSizePolicy(sizePolicy)
        self.V_line.setChecked(True)
        self.V_line.setObjectName("V_line")
        self.horizontalLayout_3.addWidget(self.V_line)
        self.Max_Limit = QtWidgets.QCheckBox(Form)
        self.Max_Limit.setChecked(True)
        self.Max_Limit.setObjectName("Max_Limit")
        self.horizontalLayout_3.addWidget(self.Max_Limit)
        self.Min_Limit = QtWidgets.QCheckBox(Form)
        self.Min_Limit.setChecked(True)
        self.Min_Limit.setObjectName("Min_Limit")
        self.horizontalLayout_3.addWidget(self.Min_Limit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.Color = QtWidgets.QComboBox(Form)
        self.Color.setObjectName("Color")
        self.horizontalLayout_2.addWidget(self.Color)
        self.Color_l = QtWidgets.QComboBox(Form)
        self.Color_l.setObjectName("Color_l")
        self.horizontalLayout_2.addWidget(self.Color_l)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p>Follow a point to find the moving boundary.</p></body></html>"))
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

