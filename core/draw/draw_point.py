# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_draw_point import Ui_Dialog

class New_point(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(New_point, self).__init__(parent)
        self.setupUi(self)
