# -*- coding: utf-8 -*-

"""
Module implementing version_show.
"""

from PyQt5.QtWidgets import QDialog
from .Ui_version import Ui_About_Dialog
from sys import version_info

version_number = "1.0.0"

class version_show(QDialog, Ui_About_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(version_show, self).__init__(parent)
        self.setupUi(self)

def show_version():
    print("[Pyslvs "+version_number+"]",
        "Python Version: {0:d}.{1:d}.{2:d}".format(*version_info[:3]))
    try:
        try: from PyQt5.QtCore import qVersion
        except: from PyQt4.QtCore import qVersion
        print("Qt Version: {0}".format(qVersion().strip()))
    except: print("No Qt.")
    try:
        try: from PyQt5.QtCore import PYQT_VERSION_STR as pyqtVersion
        except: from PyQt4.QtCore import PYQT_VERSION_STR as pyqtVersion
        print("PyQt Version:", pyqtVersion.strip())
    except: print("No PyQt.")
    try:
        from sip import SIP_VERSION_STR as sipVersion
        print("Sip Version:", sipVersion.strip())
    except: print("No Sip.")
    try:
        try: from PyQt5.Qsci import QSCINTILLA_VERSION_STR as qsciVersion
        except: from PyQt4.Qsci import QSCINTILLA_VERSION_STR as qsciVersion
        print("QScintilla Version:", qsciVersion.strip())
    except: print("No QScintilla.")
    print("-------")
