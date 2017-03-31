# -*- coding: utf-8 -*-
from sys import version_info
import csv, platform, argparse
from ..QtModules import *
from .Ui_info import Ui_About_Dialog

VERSION = "0.6.2(dev)"

parser = argparse.ArgumentParser(
    description="Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.",
    epilog="Power by Python IDE Eric-6, PyQt-5, dxfwrite.")
parser.add_argument('-v', '--version', action='version', help="show version infomations and exit", version=VERSION)
parser.add_argument('-r', metavar='File Path', default=False, nargs='?', type=str, help="read csv file from the file path")
parser.add_argument('-w', action='store_true', help="show rebuild warning of canvas")
parser.add_argument('-f', '--fusion', action='store_true', help="run Pyslvs in Fusion style")
parser.add_argument('-d', '--file-data', action='store_true', help="display the file data in command-line when opening")
parser.add_argument('-g', '--show-args', action='store_true', help="display the arguments when starting")
args = parser.parse_args()

def show_info():
    print("Pyslvs {}".format(VERSION))
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
    return args

class Pyslvs_Splash(QSplashScreen):
    def __init__(self, parent=None):
        super(Pyslvs_Splash, self).__init__(parent, QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}".format(VERSION), (Qt.AlignBottom|Qt.AlignRight))

## Turn simple string to html format.
def html(script): return '<html><head/><body>{}</body></html>'.format(script)
def title(name, *others): return '<h2>{}</h2>'.format(name)+('<h3>{}</h3>'.format('</h3><h3>'.join(others)) if others else '')
def content(*text): return '<p>{}</p>'.format('</p><p>'.join(text))
def orderList(*List): return '<ol><li>{}</li></ol>'.format('</li><li>'.join(List))

class version_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(version_show, self).__init__(parent)
        self.setupUi(self)
        self.Title.setText(html(title("Pyslvs", "Version {}".format(VERSION))))
        self.Content.setText(html(content(
        "Pyslvs is a Open Source support tools to help user solving 2D linkage problem.",
        "It can use in Mechanical Design and Simulation.",
        "This program using Python 3 with Python Solvespace.",
        "Pyslvs just like a ordinary CAD software, but use table to add and edit points.",
        "Within changing points location, finally give the answer to designer.",
        "We have these features:")+orderList(
        "2D Linkages dynamic simulation.",
        "Dimensional Synthesis of Planar Four-bar Linkages.",
        "Output points coordinate to Data Sheet (*.csv) format.",
        "Change canvas appearance.",
        "Draw dynamic simulation path with any point in the machinery.",
        "Using triangle iterate the mechanism results.")+content(
        "If you want to know about more, you can reference by our website.",
        )))
