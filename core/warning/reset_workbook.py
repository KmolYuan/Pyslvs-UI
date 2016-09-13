# -*- coding: utf-8 -*-

"""
Module implementing reset_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_reset_workbook import Ui_Warning_reset

class reset_show(QDialog, Ui_Warning_reset):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(reset_show, self).__init__(parent)
        self.setupUi(self)
