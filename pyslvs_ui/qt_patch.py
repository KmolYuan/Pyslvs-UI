# -*- coding: utf-8 -*-

"""This module contains all the Qt objects we needed.

Customized class will define below.
"""

__all__ = ['API', 'qt_image_suffix', 'qt_image_format', 'QABCMeta']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import ABCMeta
from os.path import join, dirname, abspath
from importlib.metadata import version
from qtpy import API_NAME
from qtpy.QtCore import QObject, QDir

API = f"{API_NAME} {version(API_NAME)}"
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
QDir.addSearchPath("icons", join(abspath(dirname(__file__)), "icons"))


class QABCMeta(type(QObject), ABCMeta):  # type: ignore
    """Qt ABCMeta class.

    Usage:
    >>> from abc import abstractmethod
    >>> class MyQObject(QObject, metaclass=QABCMeta):
    >>>    @abstractmethod
    >>>    def my_abstract_method(self) -> None:
    >>>        raise NotImplementedError
    """
    pass
