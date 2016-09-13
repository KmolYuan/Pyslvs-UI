# -*- coding: utf-8 -*-

"""
Module implementing kill_origin_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_kill_origin import Ui_Warning_kill_origin


class kill_origin_show(QDialog, Ui_Warning_kill_origin):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(kill_origin_show, self).__init__(parent)
        self.setupUi(self)
