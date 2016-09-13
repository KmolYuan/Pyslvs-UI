# -*- coding: utf-8 -*-
import webbrowser
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
_translate = QCoreApplication.translate
from .Ui_script import Ui_Info_Dialog

Environment_variables = '../'

class Script_Dialog(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(Script_Dialog, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_buttonBox_helpRequested(self):
        print("Open http://project.mde.tw/blog/slvs-library-functions.html")
        webbrowser.open("http://project.mde.tw/blog/slvs-library-functions.html")
    
    @pyqtSlot()
    def on_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.script.toPlainText())
        self.copy.setText(_translate("Info_Dialog", "Copied!"))
    
    @pyqtSlot()
    def on_save_clicked(self):
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Python3 Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")+".py"
            with open(fileName, 'w', newline="") as f:
                f.write(self.script.toPlainText())
            print("Successful Save Script: "+fileName)
