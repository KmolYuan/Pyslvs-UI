# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .QtModules import QApplication
from .main import MainWindow
from .info import (
    ARGUMENTS,
    INFO,
    PyslvsSplash
)

__all__ = [
    'QApplication',
    'MainWindow',
    'ARGUMENTS',
    'INFO',
    'PyslvsSplash',
]
