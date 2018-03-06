# -*- coding: utf-8 -*-

"""About informations."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QSplashScreen,
    QPixmap,
    Qt,
    QDialog,
)
from .info import VERSION, INFO, ARGUMENTS
from .Ui_about import Ui_About_Dialog

"""Turn simple string to html format."""
html = lambda s: "<html><head/><body>{}</body></html>".format(s.replace('\n', '<br/>'))
title = lambda name, *s: '<h2>{}</h2>'.format(name)+('<h3>{}</h3>'.format('</h3><h3>'.join(s)) if s else '')
content = lambda *s: '<p>{}</p>'.format('</p><p>'.join(s))
orderList = lambda *s: '<ul><li>{}</li></ul>'.format('</li><li>'.join(s))

class PyslvsSplash(QSplashScreen):
    
    """Qt splash show up when startup."""
    
    def __init__(self, parent=None):
        super(PyslvsSplash, self).__init__(parent, QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}.{}.{}({})".format(*VERSION), (Qt.AlignBottom|Qt.AlignRight))

class PyslvsAbout(QDialog, Ui_About_Dialog):
    
    """Pyslvs about dialog."""
    
    def __init__(self, parent=None):
        super(PyslvsAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Title.setText(html(
            title("Pyslvs") +
            content("Version {}.{}.{}({}) 2016-2018".format(*VERSION))
        ))
        self.Content.setText(html(content(
            "Pyslvs is a Open Source support tools to help user " +
            "solving 2D linkage problem.",
            "It can use in Mechanical Design and Simulation.",
            "This program using Python 3 with Python Solvespace.",
            "Pyslvs just like a ordinary CAD software, but use table to " +
            "add and edit points.",
            "Within changing points location, finally give the answer " +
            "to designer.",
            "We have these features:"
        ) + orderList(
            "2D Linkages dynamic simulation.",
            "Dimensional Synthesis of Planar Four-bar Linkages.",
            "Output points coordinate to Data Sheet (*.csv) format.",
            "Change canvas appearance.",
            "Draw dynamic simulation path with any point in the machinery.",
            "Using triangle iterate the mechanism results.")+content(
            "If you want to know about more, you can reference by our website."))
        )
        self.Versions.setText(html(orderList(*INFO)))
        self.Arguments.setText(html(content(
            "Startup arguments are as follows:")+orderList(
            "The loaded file when startup: {}".format(ARGUMENTS.r),
            "Start Path: {}".format(ARGUMENTS.i),
            "Enable solving warning: {}".format(ARGUMENTS.w),
            "Fusion style: {}".format(ARGUMENTS.fusion),
            "Debug mode: {}".format(ARGUMENTS.debug_mode))+content(
            "Using the \"-h\" argument to view the help."))
        )
