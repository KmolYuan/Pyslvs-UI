# -*- coding: utf-8 -*-

"""
Module implementing Info_Dialog.
"""
from PyQt5.QtWidgets import QDialog
from .Ui_info import Ui_Info_Dialog

class Info_show(QDialog, Ui_Info_Dialog):
    def __init__(self, parent=None):
        super(Info_show, self).__init__(parent)
        self.setupUi(self)
