# -*- coding: utf-8 -*-
from ..QtModules import *
_translate = QCoreApplication.translate
from .Ui_editFileInfo import Ui_Info_Dialog

class editFileInfo_show(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(editFileInfo_show, self).__init__(parent)
        self.setupUi(self)
    
    def rename(self, name, author, description, lastTime):
        self.setWindowTitle(_translate("Dialog", "About "+name.split('/')[-1]))
        self.fileName.setText(_translate("File Name", "File Name: "+name))
        self.authorName_input.setText(author)
        self.dateName.setText(lastTime)
        self.descriptionText.setPlainText(description)
