# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_delete_slider import Ui_Dialog

class delete_slider_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(delete_slider_show, self).__init__(parent)
        self.setupUi(self)
