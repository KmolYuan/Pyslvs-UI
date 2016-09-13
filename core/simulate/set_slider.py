# -*- coding: utf-8 -*-

"""
Module implementing slider_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_set_slider import Ui_Dialog

class slider_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
