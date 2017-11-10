# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/synthesis/NumberAndTypeSynthesis/Permutations.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(399, 489)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/NumberAndTypeSynthesis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ReloadMechanism = QtWidgets.QPushButton(Form)
        self.ReloadMechanism.setObjectName("ReloadMechanism")
        self.verticalLayout.addWidget(self.ReloadMechanism)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Expression_joint = QtWidgets.QLineEdit(Form)
        self.Expression_joint.setObjectName("Expression_joint")
        self.verticalLayout.addWidget(self.Expression_joint)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.Expression_link = QtWidgets.QLineEdit(Form)
        self.Expression_link.setObjectName("Expression_link")
        self.verticalLayout.addWidget(self.Expression_link)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.NL_input = QtWidgets.QSpinBox(Form)
        self.NL_input.setObjectName("NL_input")
        self.gridLayout.addWidget(self.NL_input, 1, 0, 1, 1)
        self.NJ_input = QtWidgets.QSpinBox(Form)
        self.NJ_input.setMaximum(18)
        self.NJ_input.setObjectName("NJ_input")
        self.gridLayout.addWidget(self.NJ_input, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.DOF_input = QtWidgets.QSpinBox(Form)
        self.DOF_input.setEnabled(False)
        self.DOF_input.setObjectName("DOF_input")
        self.gridLayout.addWidget(self.DOF_input, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.Combine_number = QtWidgets.QPushButton(Form)
        self.Combine_number.setAutoDefault(True)
        self.Combine_number.setObjectName("Combine_number")
        self.verticalLayout_2.addWidget(self.Combine_number)
        self.Expression_number = QtWidgets.QListWidget(Form)
        self.Expression_number.setObjectName("Expression_number")
        self.verticalLayout_2.addWidget(self.Expression_number)
        self.Combine_type = QtWidgets.QPushButton(Form)
        self.Combine_type.setAutoDefault(True)
        self.Combine_type.setObjectName("Combine_type")
        self.verticalLayout_2.addWidget(self.Combine_type)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ReloadMechanism.setText(_translate("Form", "Reload from workbook"))
        self.label.setText(_translate("Form", "Mainly for joint:"))
        self.label_2.setText(_translate("Form", "Mainly for link:"))
        self.label_4.setText(_translate("Form", "Number of joints:"))
        self.label_3.setText(_translate("Form", "Number of links:"))
        self.NL_input.setToolTip(_translate("Form", "≥3"))
        self.NJ_input.setToolTip(_translate("Form", "8~18"))
        self.label_5.setText(_translate("Form", "Degree of freedom:"))
        self.Combine_number.setText(_translate("Form", "Number Combine"))
        self.Combine_type.setText(_translate("Form", "Type Combine"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

