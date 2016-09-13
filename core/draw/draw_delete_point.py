# -*- coding: utf-8 -*-

"""
Module implementing delete_point_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_draw_delete_point import Ui_Dialog

class delete_point_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(delete_point_show, self).__init__(parent)
        self.setupUi(self)
