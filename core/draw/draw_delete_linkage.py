# -*- coding: utf-8 -*-

"""
Module implementing delete_linkage_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_delete_linkage import Ui_Dialog

class delete_linkage_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(delete_linkage_show, self).__init__(parent)
        self.setupUi(self)
