# -*- coding: utf-8 -*-

"""
Module implementing resolution_fail_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_resolution_fail import Ui_Warning_resolution_fail

class resolution_fail_show(QDialog, Ui_Warning_resolution_fail):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(resolution_fail_show, self).__init__(parent)
        self.setupUi(self)
