# -*- coding: utf-8 -*-
from sys import version_info, argv
import csv, platform
from PyQt5.QtWidgets import QDialog, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from .textConverter import *
from .Ui_info import Ui_About_Dialog

VERSION = "0.5.0(dev)"

def show_version():
    print("[Pyslvs {}]".format(VERSION))
    if '--version' in argv or '-v' in argv: return 0
    show_info()
    if '--help' in argv or '-h' in argv or '-H' in argv:
        show_help()
        return 0
    return 1

def show_info():
    print("OS Type: {}".format(platform.system()))
    print("Python Version: {:d}.{:d}.{:d}".format(*version_info[:3]))
    try:
        from PyQt5.QtCore import qVersion
        print("Qt Version: {}".format(qVersion().strip()))
    except ImportError: print("No Qt5.")
    try:
        from PyQt5.QtCore import PYQT_VERSION_STR as pyqtVersion
        print("PyQt Version: {}".format(pyqtVersion.strip()))
    except ImportError: print("No PyQt5.")
    try:
        from sip import SIP_VERSION_STR as sipVersion
        print("Sip Version: {}".format(sipVersion.strip()))
    except ImportError: print("No Sip.")
    try:
        from PyQt5.Qsci import QSCINTILLA_VERSION_STR as qsciVersion
        print("QScintilla Version: {}".format(qsciVersion.strip()))
    except ImportError: print("No QScintilla.")
    print('-'*7)

def show_help():
    print(help(argumentType(
        "python3 launch_pyslvs.py [FileName] [arg1] [arg2] ...",
        "launch_pyslvs [FileName] [arg1] [arg2] ..."),
        "Open a file directly by put file name after the launch command.",
        "Information and Debug Function:", argumentList(
        ['-v', '--version', "Show version infomations and Exit."],
        ['-h -H', '--help\t', "Show this help message and Exit."],
        ['-w', "Show rebuild warning of canvas."],
        ['-f', '--fusion', "Run Pyslvs in Fusion style."],
        ['-F', '--file-data', "When open a file, show it's data in command line."]),
        present("Python IDE Eric 6", "PyQt 5", "dxfwrite")))

class Pyslvs_Splash(QSplashScreen):
    def __init__(self, parent=None):
        super(Pyslvs_Splash, self).__init__(parent)
        self.setPixmap(QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}".format(VERSION), (Qt.AlignBottom|Qt.AlignRight))

class Help_info_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(Help_info_show, self).__init__(parent)
        self.setupUi(self)
        self.Content.setText(html(title("Pyslvs")+content(
        "Pyslvs just like a ordinary CAD software, but use table to add and edit points.",
        "Within changing points location, finally give the answer to designer.",
        "We have these features:")+orderList(
        "2D Linkages dynamic simulation.",
        "Dimensional Synthesis of Planar Four-bar Linkages.",
        "Output points coordinate to Data Sheet (*.csv) format.",
        "Change canvas appearance.",
        "Draw dynamic simulation path with any point in the machinery.")))

class version_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(version_show, self).__init__(parent)
        self.setupUi(self)
        self.Content.setText(html(title("Pyslvs", "version {}".format(VERSION))+content(
        "Pyslvs is a Open Source support tools to help user solving 2D linkage problem.",
        "It can use in Mechanical Design and Simulation.",
        "This program using Python 3 with Python Solvespace.",
        "If you want to know about more, you can reference by our website.")))
