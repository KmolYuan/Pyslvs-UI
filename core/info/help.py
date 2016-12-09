# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_help import Ui_Info_Dialog

class Help_info_show(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(Help_info_show, self).__init__(parent)
        self.setupUi(self)
