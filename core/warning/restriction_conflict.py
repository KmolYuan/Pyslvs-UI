# -*- coding: utf-8 -*-

"""
Module implementing restriction_conflict_show.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_restriction_conflict import Ui_Restriction_Conflict

class restriction_conflict_show(QDialog, Ui_Restriction_Conflict):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(restriction_conflict_show, self).__init__(parent)
        self.setupUi(self)
