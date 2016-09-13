# -*- coding: utf-8 -*-

"""
Module implementing color_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_color import Ui_Info_Dialog

class color_show(QDialog, Ui_Info_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(color_show, self).__init__(parent)
        self.setupUi(self)
