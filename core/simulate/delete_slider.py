# -*- coding: utf-8 -*-

"""
Module implementing delete_slider_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_delete_slider import Ui_Dialog


class delete_slider_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(delete_slider_show, self).__init__(parent)
        self.setupUi(self)
