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
        Form.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/NumberAndTypeSynthesis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Representation_text = QtWidgets.QLineEdit(Form)
        self.Representation_text.setReadOnly(True)
        self.Representation_text.setObjectName("Representation_text")
        self.horizontalLayout.addWidget(self.Representation_text)
        self.ReloadMechanism = QtWidgets.QPushButton(Form)
        self.ReloadMechanism.setObjectName("ReloadMechanism")
        self.horizontalLayout.addWidget(self.ReloadMechanism)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Representation_tree = QtWidgets.QTreeWidget(Form)
        self.Representation_tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.Representation_tree.setObjectName("Representation_tree")
        self.verticalLayout.addWidget(self.Representation_tree)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ReloadMechanism.setText(_translate("Form", "Reload"))
        self.Representation_tree.headerItem().setText(0, _translate("Form", "name"))
        self.Representation_tree.headerItem().setText(1, _translate("Form", "value"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

