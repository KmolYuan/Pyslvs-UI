# -*- coding: utf-8 -*-

"""This module mounted Qt.QtGui."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .backend import BACKEND

if BACKEND == "PyQt5":
    from PyQt5.QtGui import *
else:
    raise ImportError
