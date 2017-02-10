# -*- coding: utf-8 -*-
from sys import version_info, argv
import csv, platform
from PyQt5.QtWidgets import QDialog
from .Ui_version import Ui_About_Dialog

version_number = "0.5.0(dev)"

def show_info():
    print("OS Type: {}".format(platform.system()))
    print("Python Version: {0:d}.{1:d}.{2:d}".format(*version_info[:3]))
    try:
        from PyQt5.QtCore import qVersion
        print("Qt Version: {}".format(qVersion().strip()))
    except: print("No Qt5.")
    try:
        from PyQt5.QtCore import PYQT_VERSION_STR as pyqtVersion
        print("PyQt Version: {}".format(pyqtVersion.strip()))
    except: print("No PyQt5.")
    try:
        from sip import SIP_VERSION_STR as sipVersion
        print("Sip Version: {}".format(sipVersion.strip()))
    except: print("No Sip.")
    try:
        from PyQt5.Qsci import QSCINTILLA_VERSION_STR as qsciVersion
        print("QScintilla Version: {}".format(qsciVersion.strip()))
    except: print("No QScintilla.")
    print("-------")

def show_help():
    show_info()
    print("""==Help message==
Arguments:

* python3 launch_pyslvs.py [FileName] [arg1] [arg2] ...

* launch_pyslvs [FileName] [arg1] [arg2] ...

Open a file directly by put file name behind the launch command.

Information and Debug Function:

-v\t--version\tOnly show version infomations and Exit.
-h\t--help\t\tShow this help message and Exit.
-w\t\t\tDon't show Rebuild warning.
--fusion\t\tRun Pyslvs in Fusion style.
--file-data\t\tWhen open a file, show it's data in command line.

Run launch_test.py can start unit test.
================""")

def show_version(): print("[Pyslvs "+version_number+"]\nPython Version: {0:d}.{1:d}.{2:d}".format(*version_info[:3]))

class Help_info_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(Help_info_show, self).__init__(parent)
        self.setupUi(self)
        self.versionLabel.setVisible(False)
        self.Content.setText("""<html><head/><body><h1>
Pyslvs
</h1><p>
Pyslvs just like a ordinary CAD software, but use table format to add and edit, within changing points location, finally give the answer to designer.
</p><p>
We have these functions:
</p><ol><li>
Change canvas appearance.
</li><li>
2D Linkages dynamic simulation.
</li><li>
Draw dynamic simulation path at any point in the machinery.
</li><li>
Output points coordinate to table file format.
</li></ol></p></body></html>""")

class Info_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(Info_show, self).__init__(parent)
        self.setupUi(self)
        self.versionLabel.setVisible(False)
        self.Content.setText("""<html><head/><body><h1>
Python Solvespace
</h1><p>
Library of Solvspace, within a interface of Python.
</p><p>
So any python script can using it in 2D or 3D computing problem-solving.
</p><p>
It use like Solvespace, but maybe not so convenience.
</p><p>
So Pyslvs will make up for shortcomings of Python Solvespace.
</p></body></html>""")

class version_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(version_show, self).__init__(parent)
        self.setupUi(self)
        self.versionLabel.setText("<h1>Pyslvs</h1><h3>version {}</h3>".format(version_number))
        self.Content.setText("""<html><head/><body><p>
Pyslvs is a Open Source support tools to help user solving 2D linkage problem.
</p><p>
It can use in Mechanical Design and Simulation.
</p><p>
This program using Python 3 with Python Solvespace.
</p><p>
If you want to know about more, you can refer to our website.
</p></body></html>""")
