# -*- coding: utf-8 -*-

"""
Module implementing rod_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_set_rod import Ui_Dialog


class rod_show(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(rod_show, self).__init__(parent)
        self.setupUi(self)
