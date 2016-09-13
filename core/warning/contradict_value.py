# -*- coding: utf-8 -*-

"""
Module implementing contradict_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_contradict_value import Ui_contradict


class contradict_show(QDialog, Ui_contradict):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(contradict_show, self).__init__(parent)
        self.setupUi(self)
