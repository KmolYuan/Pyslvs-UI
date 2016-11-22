# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
_translate = QCoreApplication.translate
from .Ui_fileInfo import Ui_Info_Dialog

class fileInfo_show(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(fileInfo_show, self).__init__(parent)
        self.setupUi(self)
    
    def rename(self, name, author, description, lastTime):
        self.setWindowTitle(_translate("Dialog", "About "+name))
        self.fileName.setText(_translate("File Name", "File Name: "+name))
        self.authorName.setText(_translate("Author", "Author: "+author+' '+lastTime))
        self.descriptionText.setHtml(description)
