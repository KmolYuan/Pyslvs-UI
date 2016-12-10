# -*- coding: utf-8 -*-
from .__init__ import *

class chain_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(chain_show, self).__init__(parent)
        self.setupUi(self)
