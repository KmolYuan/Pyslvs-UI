# -*- coding: utf-8 -*-
from .__init__ import *

class delete_point_show(QDialog, delete_point_Dialog):
    def __init__(self, parent=None):
        super(delete_point_show, self).__init__(parent)
        self.setupUi(self)
