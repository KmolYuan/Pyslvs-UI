# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ahshoe/Desktop/Pyslvs-PyQt5/core/synthesis/Collections/TriangularIteration.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(390, 553)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/collection-triangular-iteration.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Driver_label = QtWidgets.QLabel(Form)
        self.Driver_label.setObjectName("Driver_label")
        self.verticalLayout_2.addWidget(self.Driver_label)
        self.Driver_list = QtWidgets.QListWidget(Form)
        self.Driver_list.setObjectName("Driver_list")
        self.verticalLayout_2.addWidget(self.Driver_list)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Follower_label = QtWidgets.QLabel(Form)
        self.Follower_label.setObjectName("Follower_label")
        self.verticalLayout_4.addWidget(self.Follower_label)
        self.Follower_list = QtWidgets.QListWidget(Form)
        self.Follower_list.setObjectName("Follower_list")
        self.verticalLayout_4.addWidget(self.Follower_list)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Target_label = QtWidgets.QLabel(Form)
        self.Target_label.setObjectName("Target_label")
        self.verticalLayout_3.addWidget(self.Target_label)
        self.Target_list = QtWidgets.QListWidget(Form)
        self.Target_list.setObjectName("Target_list")
        self.verticalLayout_3.addWidget(self.Target_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.constraint_label = QtWidgets.QLabel(Form)
        self.constraint_label.setObjectName("constraint_label")
        self.verticalLayout_5.addWidget(self.constraint_label)
        self.constraint_list = QtWidgets.QListWidget(Form)
        self.constraint_list.setObjectName("constraint_list")
        self.verticalLayout_5.addWidget(self.constraint_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_6.addWidget(self.line_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Link_Expression_label = QtWidgets.QLabel(Form)
        self.Link_Expression_label.setObjectName("Link_Expression_label")
        self.verticalLayout.addWidget(self.Link_Expression_label)
        self.Link_Expression = QtWidgets.QLineEdit(Form)
        self.Link_Expression.setReadOnly(True)
        self.Link_Expression.setObjectName("Link_Expression")
        self.verticalLayout.addWidget(self.Link_Expression)
        self.Expression_label = QtWidgets.QLabel(Form)
        self.Expression_label.setObjectName("Expression_label")
        self.verticalLayout.addWidget(self.Expression_label)
        self.Expression = QtWidgets.QLineEdit(Form)
        self.Expression.setReadOnly(True)
        self.Expression.setObjectName("Expression")
        self.verticalLayout.addWidget(self.Expression)
        self.verticalLayout_6.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Driver_label.setText(_translate("Form", "Drivers:"))
        self.Follower_label.setText(_translate("Form", "Followers:"))
        self.Target_label.setText(_translate("Form", "Targets:"))
        self.constraint_label.setText(_translate("Form", "Gruebler\'s Equation:"))
        self.Link_Expression_label.setText(_translate("Form", "Link expression:"))
        self.Expression_label.setText(_translate("Form", "Expression:"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

