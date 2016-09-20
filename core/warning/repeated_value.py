# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_repeated_value import Ui_Warning_same_value

class same_show(QDialog, Ui_Warning_same_value):
    def __init__(self, parent=None):
        super(same_show, self).__init__(parent)
        self.setupUi(self)
