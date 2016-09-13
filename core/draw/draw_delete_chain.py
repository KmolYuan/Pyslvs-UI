# -*- coding: utf-8 -*-

"""
Module implementing delete_chain_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_delete_chain import Ui_Dialog

class delete_chain_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(delete_chain_show, self).__init__(parent)
        self.setupUi(self)
