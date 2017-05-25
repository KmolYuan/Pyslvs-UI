# -*- coding: utf-8 -*-
from sys import version_info
import platform, argparse
from ..QtModules import *
from .Ui_info import Ui_About_Dialog

VERSION = ('0.7.0', 'stable')
from PyQt5.QtCore import qVersion
from PyQt5.QtCore import PYQT_VERSION_STR as pyqtVersion
from sip import SIP_VERSION_STR as sipVersion
from PyQt5.Qsci import QSCINTILLA_VERSION_STR as qsciVersion
INFO = ["Pyslvs {}({})".format(VERSION[0], VERSION[1]),
    "OS Type: {} {} [{}]".format(platform.system(), platform.release(), platform.machine()),
    "Python Version: {v.major}.{v.minor}.{v.micro}({v.releaselevel})".format(v=version_info),
    "Python Compiler: {}".format(platform.python_compiler()),
    "Qt Version: {}".format(qVersion().strip()),
    "PyQt Version: {}".format(pyqtVersion.strip()),
    "Sip Version: {}".format(sipVersion.strip()),
    "QScintilla Version: {}".format(qsciVersion.strip())]

parser = argparse.ArgumentParser(
    description="Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.",
    epilog="Power by Python IDE Eric-6, PyQt-5, dxfwrite.")
parser.add_argument('-v', '--version', action='version', help="show version infomations and exit", version='{}({})'.format(VERSION[0], VERSION[1]))
parser.add_argument('r', metavar='File Path', default=False, nargs='?', type=str, help="read workbook from the file path")
parser.add_argument('-i', metavar='Start Path', default=False, nargs='?', type=str, help="start Pyslvs in the specified path")
parser.add_argument('-w', action='store_true', help="show rebuild warning of canvas")
parser.add_argument('-f', '--fusion', action='store_true', help="run Pyslvs in Fusion style")
parser.add_argument('--file-data', action='store_true', help="display the file data in command-line when opening")
parser.add_argument('-d', '--debug-mode', action='store_true', help="don't connect to GUI console when opening")
args = parser.parse_args()

def show_info():
    print('\n'.join(INFO))
    print('-'*7)
    return args

class Pyslvs_Splash(QSplashScreen):
    def __init__(self, parent=None):
        super(Pyslvs_Splash, self).__init__(parent, QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}({})".format(VERSION[0], VERSION[1]), (Qt.AlignBottom|Qt.AlignRight))

## Turn simple string to html format.
def html(script): return '<html><head/><body>{}</body></html>'.format(script)
def title(name, *others): return '<h2>{}</h2>'.format(name)+('<h3>{}</h3>'.format('</h3><h3>'.join(others)) if others else '')
def content(*text): return '<p>{}</p>'.format('</p><p>'.join(text))
def orderList(*List): return '<ul><li>{}</li></ul>'.format('</li><li>'.join(List))

class version_show(QDialog, Ui_About_Dialog):
    def __init__(self, parent=None):
        super(version_show, self).__init__(parent)
        self.setupUi(self)
        self.Title.setText(html(title("Pyslvs", "Version {}({})".format(VERSION[0], VERSION[1]))))
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
            "If you want to know about more, you can reference by our website.")))
        self.Versions.setText(html(orderList(*INFO)))
        self.Arguments.setText(html(content(
            "Startup arguments are as follows:")+orderList(
            "The loaded file when startup: {}".format(args.r),
            "Start Path: {}".format(args.i),
            "Enable solving warning: {}".format(args.w),
            "Fusion style: {}".format(args.fusion),
            "Show file data in console: {}".format(args.file_data),
            "Debug mode: {}".format(args.debug_mode))+content(
            "Using the \"-h\" argument to view help."
            )))
