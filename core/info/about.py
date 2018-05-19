# -*- coding: utf-8 -*-

"""About informations."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    Qt,
    QDialog,
    QSplashScreen,
    QPixmap,
)
from .info import __version__, INFO, ARGUMENTS
from .Ui_about import Ui_Dialog


def html(s: str) -> str:
    """Turn simple string to html format."""
    return "<html><head/><body>{}</body></html>".format(s.replace('\n', '<br/>'))

def _title(name: str, *s: str) -> str:
    """Wrap title."""
    return (
        '<h2>{}</h2>'.format(name) +
        ('<h3>{}</h3>'.format('</h3><h3>'.join(s)) if s else '')
    )

def _content(*s: str) -> str:
    """Wrap as paragraph."""
    return '<p>{}</p>'.format('</p><p>'.join(s))

def _orderList(*s: str) -> str:
    """Wrap as list."""
    return '<ul><li>{}</li></ul>'.format('</li><li>'.join(s))


class PyslvsSplash(QSplashScreen):
    
    """Qt splash show up when startup."""
    
    def __init__(self):
        super(PyslvsSplash, self).__init__(None, QPixmap(":/icons/Splash.png"))
        self.showMessage("Version {}.{}.{}({})".format(*__version__), (Qt.AlignBottom|Qt.AlignRight))


class PyslvsAbout(QDialog, Ui_Dialog):
    
    """Pyslvs about dialog."""
    
    def __init__(self, parent):
        """About descript strings."""
        super(PyslvsAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Title.setText(html(
            _title("Pyslvs") +
            _content("Version {}.{}.{}({}) 2016-2018".format(*__version__))
        ))
        self.Content.setText(html(_content(
            "A GUI-based tool use to solving 2D linkage subject.",
            "Author: {}".format(__author__),
            "Email: {}".format(__email__),
            "If you want to know more, go to see to our website or contact the email."))
        )
        self.Versions.setText(html(_orderList(*INFO)))
        self.Arguments.setText(html(_content(
            "Startup arguments are as follows:") + _orderList(
            "The loaded file when startup: {}".format(ARGUMENTS.r),
            "Start Path: {}".format(ARGUMENTS.i),
            "Enable solving warning: {}".format(ARGUMENTS.w),
            "Fusion style: {}".format(ARGUMENTS.fusion),
            "Debug mode: {}".format(ARGUMENTS.debug_mode)) + _content(
            "Using the \"-h\" argument to view the help."))
        )
