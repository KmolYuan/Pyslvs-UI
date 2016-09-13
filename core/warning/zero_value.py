# -*- coding: utf-8 -*-

"""
Module implementing zero_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_zero_value import Ui_Warning_no_value

class zero_show(QDialog, Ui_Warning_no_value):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(zero_show, self).__init__(parent)
        self.setupUi(self)
