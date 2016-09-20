# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_restriction_conflict import Ui_Restriction_Conflict

class restriction_conflict_show(QDialog, Ui_Restriction_Conflict):
    def __init__(self, parent=None):
        super(restriction_conflict_show, self).__init__(parent)
        self.setupUi(self)
