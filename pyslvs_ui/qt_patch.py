# -*- coding: utf-8 -*-

"""This module contains all the Qt objects we needed.

Customized class will define below.
"""

__all__ = ['API', 'QT_VERSION', 'qt_image_suffix', 'qt_image_format', 'QABCMeta']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Any
from abc import ABCMeta
from qtpy import QtCore, API_NAME
from importlib import import_module

if API_NAME == 'PyQt5':
    API = f"{API_NAME} {QtCore.PYQT_VERSION_STR}"
elif API_NAME == 'PySide2':
    API = f"{API_NAME} {getattr(import_module('PySide2'), '__version__')}"
else:
    raise ModuleNotFoundError("module not found: PyQt5 or PySide2")

QT_VERSION = QtCore.__version__
qt_image_suffix = []
qt_image_format = []
for suffix, name in (
    ('png', "Portable Network Graphics"),
    ('jpg', "Joint Photographic Experts Group"),
    ('bmp', "Bitmap Image file"),
    ('bpm', "Business Process Model"),
    ('tiff', "Tagged Image File Format"),
    ('ico', "Windows Icon"),
    ('wbmp', "Wireless Application Protocol Bitmap"),
    ('xbm', "X Bitmap"),
    ('xpm', "X Pixmap"),
):
    qt_image_suffix.append(suffix)
    qt_image_format.append(f"{name} (*.{suffix})")
qt_image_suffix = tuple(qt_image_suffix)
qt_image_format = tuple(qt_image_format)
del suffix, name

_Wrapper: Any = type(QtCore.QObject)


class QABCMeta(_Wrapper, ABCMeta):
    """Qt ABCMeta class.

    Usage:
    >>> from abc import abstractmethod
    >>> class MyQObject(QtCore.QObject, metaclass=QABCMeta):
    >>>    @abstractmethod
    >>>    def my_abstract_method(self) -> None:
    >>>        ...
    """
    pass
