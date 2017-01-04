# -*- coding: utf-8 -*-

"""
Module implementing Path_Solving_listbox_show.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from .Ui_run_Path_Solving_listbox import Ui_Form


class Path_Solving_listbox_show(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Path_Solving_listbox_show, self).__init__(parent)
        self.setupUi(self)
