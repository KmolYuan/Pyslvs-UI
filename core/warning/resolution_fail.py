# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_resolution_fail import Ui_Warning_resolution_fail

class resolution_fail_show(QDialog, Ui_Warning_resolution_fail):
    def __init__(self, parent=None):
        super(resolution_fail_show, self).__init__(parent)
        self.setupUi(self)
