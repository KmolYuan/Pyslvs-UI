# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_template import Ui_Dialog

class template_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(template_show, self).__init__(parent)
        self.setupUi(self)
