# -*- coding: utf-8 -*-

"""This module will try to found the backend of Qt."""

__all__ = ['BACKEND']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

try:
    import PyQt5.QtCore
except ImportError:
    raise ImportError("no Qt backend found (support PyQt5 only)")
else:
    BACKEND = "PyQt5"
