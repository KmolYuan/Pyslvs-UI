# -*- coding: utf-8 -*-
from .__init__ import *

class delete_chain_show(QDialog, delete_chain_Dialog):
    def __init__(self, parent=None):
        super(delete_chain_show, self).__init__(parent)
        self.setupUi(self)
