# -*- coding: utf-8 -*-
from sys import version_info, argv
import csv, platform
from PyQt5.QtWidgets import QDialog
from .Ui_version import Ui_About_Dialog

version_number = "0.3.0"

class version_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(version_show, self).__init__(parent)
        self.setupUi(self)

def show_info():
    commit = show_commit()
    print("[Pyslvs "+version_number+"]")
    if "-g" in argv or "--git" in argv:
        print("Last Commit: "+commit)
    print("OS Type: "+platform.system())
    print("Python Version: {0:d}.{1:d}.{2:d}".format(*version_info[:3]))
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

def show_help():
    show_info()
    print("""==Help message==
Arguments:

* python3 launch_pyslvs.py [FileName] [arg1] [arg2] ...

Open a file directly by put file name behind the launch command.

Information and Debug Function:

-g\t--git\t\tShow git infomations in the initialization.
-v\t--version\tOnly show version infomations and not to start main program.
-h\t--help\t\tShow this help message and not to start main program.

Run launch_test.py can start unit test.
================""")

def show_version():
    print("[Pyslvs "+version_number+"]\nPython Version: {0:d}.{1:d}.{2:d}".format(*version_info[:3]))

def show_commit():
    data = []
    with open('./.git/logs/refs/heads/master', newline="") as stream:
        reader = csv.reader(stream, delimiter='\n', quotechar='|')
        for row in reader: data += ', '.join(row).split(', ')
    n = data[-1][41:81]
    return n
