# -*- coding: utf-8 -*-

"""
Module implementing Help_info_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_help import Ui_Info_Dialog

class Help_info_show(QDialog, Ui_Info_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Help_info_show, self).__init__(parent)
        self.setupUi(self)
