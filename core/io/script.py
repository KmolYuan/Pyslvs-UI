# -*- coding: utf-8 -*-
import webbrowser
from ..QtModules import *
_translate = QCoreApplication.translate
from .Ui_script import Ui_Info_Dialog

class Script_Dialog(QDialog, Ui_Info_Dialog):
    def __init__(self, script, Environment_variables, parent=None):
        super(Script_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.Environment_variables = Environment_variables
        self.script.setPlainText(script)
    
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
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', self.Environment_variables, 'Python3 Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")+".py"
            with open(fileName, 'w', newline="") as f:
                f.write(self.script.toPlainText())
            print("Successful Save Script: "+fileName)
