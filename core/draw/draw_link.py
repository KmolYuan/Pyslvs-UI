# -*- coding: utf-8 -*-

"""
Module implementing New_link.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_link import Ui_Dialog

class New_link(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(New_link, self).__init__(parent)
        self.setupUi(self)
