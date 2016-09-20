# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_draw_delete_point import Ui_Dialog

class delete_point_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(delete_point_show, self).__init__(parent)
        self.setupUi(self)
