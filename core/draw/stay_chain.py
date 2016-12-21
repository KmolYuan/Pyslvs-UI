# -*- coding: utf-8 -*-
from .modules import *

class chain_show(QDialog, chain_Dialog):
    def __init__(self, parent=None):
        super(chain_show, self).__init__(parent)
        self.setupUi(self)
