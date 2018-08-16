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
    QWidget,
)
from .info import __version__, INFO, ARGUMENTS
_major, _minor, _build, _label = __version__
from .Ui_about import Ui_Dialog


def html(s: str) -> str:
    """Turn simple string to html format."""
    s = s.replace('\n', '<br/>')
    return f"<html><head/><body>{s}</body></html>"

def _title(name: str, *s: str) -> str:
    """Wrap title."""
    s = f'<h3>{"</h3><h3>".join(s)}</h3>' if s else ''
    return f'<h2>{name}</h2>{s}'

def _content(*s: str) -> str:
    """Wrap as paragraph."""
    return f'<p>{"</p><p>".join(s)}</p>'

def _orderList(*s: str) -> str:
    """Wrap as list."""
    return f'<ul><li>{"</li><li>".join(s)}</li></ul>'


class PyslvsSplash(QSplashScreen):
    
    """Qt splash show up when startup."""
    
    def __init__(self):
        super(PyslvsSplash, self).__init__(None, QPixmap(":/icons/Splash.png"))
        self.showMessage(
            f"Version {_major}.{_minor}.{_build}({_label})",
            Qt.AlignBottom | Qt.AlignRight
        )


class PyslvsAbout(QDialog, Ui_Dialog):
    
    """Pyslvs about dialog."""
    
    def __init__(self, parent: QWidget):
        """About descript strings."""
        super(PyslvsAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Title.setText(html(_title("Pyslvs") + _content(
            f"Version {_major}.{_minor}.{_build}({_label}) 2016-2018"
        )))
        self.description_text.setText(html(_content(
            "A GUI-based tool use to solving 2D linkage subject.",
            f"Author: {__author__}",
            f"Email: {__email__}",
            "If you want to know more, see to our website or contact the email.",
        )))
        self.ver_text.setText(html(_orderList(*INFO)))
        self.args_text.setText(html(_content("Startup arguments are as follows:") + _orderList(
            f"Open with: {ARGUMENTS.file}",
            f"Start Path: {ARGUMENTS.c}",
            f"Fusion style: {ARGUMENTS.fusion}",
            f"Debug mode: {ARGUMENTS.debug_mode}",
            f"Specified kernel: {ARGUMENTS.kernel}",
        ) + _content("Use \"-h\" or \"--help\" argument to view the help.")))
