# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_zero_value import Ui_Warning_no_value

class zero_show(QDialog, Ui_Warning_no_value):
    def __init__(self, parent=None):
        super(zero_show, self).__init__(parent)
        self.setupUi(self)
