# -*- coding: utf-8 -*-

"""This module contains all the Qt objects we needed.

Customized class will define below.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import ABCMeta
from qtpy import QtCore, API_NAME
from importlib import import_module
if API_NAME == 'PyQt5':
    API = f"{API_NAME} {QtCore.PYQT_VERSION_STR}"
elif API_NAME == 'PySide2':
    qt = import_module('PySide2')
    API = f"{API_NAME} {qt.__version__}"
    del qt
else:
    raise ModuleNotFoundError("module not found: PyQt5 or PySide2")
del API_NAME

QT_VERSION = QtCore.__version__

__all__ = ['API', 'QT_VERSION', 'qt_image_format', 'QABCMeta']


qt_image_format = (
    "Portable Network Graphics (*.png)",
    "Joint Photographic Experts Group (*.jpg)",
    "Bitmap Image file (*.bmp)",
    "Business Process Model (*.bpm)",
    "Tagged Image File Format (*.tiff)",
    "Windows Icon (*.ico)",
    "Wireless Application Protocol Bitmap (*.wbmp)",
    "X Bitmap (*.xbm)",
    "X Pixmap (*.xpm)",
)


class QABCMeta(type(QtCore.QObject), ABCMeta):
    """Qt ABCMeta class.

    Usage:

    class MyQObject(QObject, metaclass=QABCMeta):
        @abstractmethod
        def my_abstract_method(self) -> None:
            ...
    """
    pass
