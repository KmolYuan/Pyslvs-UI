# -*- coding: utf-8 -*-
from ..QtModules import *
_translate = QCoreApplication.translate
from .Ui_fileInfo import Ui_Info_Dialog

class editFileInfo_show(QDialog, Ui_Info_Dialog):
    def __init__(self, name, author, description, lastTime, results, parent=None):
        super(editFileInfo_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("About {}".format(name))
        self.fileName.setText("File Name: {}".format(name))
        self.authorName_input.setText(author)
        self.dateName.setText(lastTime)
        self.descriptionText.setPlainText(description)
        if results: self.Results.setText('\n'.join(["{} ({} gen)".format(result['Algorithm'], result['maxGen']) for result in results]))

class fileInfo_show(editFileInfo_show):
    def __init__(self, name, author, description, lastTime, results, errorInfo, parent=None):
        super(fileInfo_show, self).__init__(name, author, description, lastTime, results, parent)
        self.setWindowTitle("About {} (Edit mode)".format(name))
        self.authorName_input.setReadOnly(True)
        self.descriptionText.setReadOnly(True)
        if errorInfo:
            self.ErrorTables.setText('\n'.join(["Some part are missing:"]+['+{}'.format(e) for e in errorInfo]))
            self.ErrorTables.setStyleSheet("color: rgb(255, 0, 0);")
