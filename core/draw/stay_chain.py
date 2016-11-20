# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_stay_chain import Ui_Dialog

class chain_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(chain_show, self).__init__(parent)
        self.setupUi(self)
