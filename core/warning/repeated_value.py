# -*- coding: utf-8 -*-

"""
Module implementing same_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_repeated_value import Ui_Warning_same_value


class same_show(QDialog, Ui_Warning_same_value):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(same_show, self).__init__(parent)
        self.setupUi(self)
