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
        Form.resize(418, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/NumberAndTypeSynthesis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Representation_joint = QtWidgets.QLineEdit(Form)
        self.Representation_joint.setReadOnly(True)
        self.Representation_joint.setObjectName("Representation_joint")
        self.verticalLayout.addWidget(self.Representation_joint)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.Representation_link = QtWidgets.QLineEdit(Form)
        self.Representation_link.setReadOnly(True)
        self.Representation_link.setObjectName("Representation_link")
        self.verticalLayout.addWidget(self.Representation_link)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.ReloadMechanism = QtWidgets.QPushButton(Form)
        self.ReloadMechanism.setObjectName("ReloadMechanism")
        self.horizontalLayout.addWidget(self.ReloadMechanism)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.Representation_tree = QtWidgets.QTreeWidget(Form)
        self.Representation_tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Representation_tree.setObjectName("Representation_tree")
        self.verticalLayout_2.addWidget(self.Representation_tree)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Mainly for joint:"))
        self.label_2.setText(_translate("Form", "Mainly for link:"))
        self.ReloadMechanism.setText(_translate("Form", "Reload"))
        self.Representation_tree.headerItem().setText(0, _translate("Form", "Attributes"))
        self.Representation_tree.headerItem().setText(1, _translate("Form", "Value"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

