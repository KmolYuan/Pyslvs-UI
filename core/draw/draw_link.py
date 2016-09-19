# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_draw_link import Ui_Dialog

class New_link(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(New_link, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
