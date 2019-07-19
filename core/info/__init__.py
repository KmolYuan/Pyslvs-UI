# -*- coding: utf-8 -*-

"""'info' module contains Pyslvs program information."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .info import (
    SYS_INFO,
    ARGUMENTS,
    check_update,
)
from .about import PyslvsAbout, html
from .logging_handler import logger, XStream

__all__ = [
    'SYS_INFO',
    'ARGUMENTS',
    'check_update',
    'PyslvsAbout',
    'html',
    'logger',
    'XStream',
    'kernel_list',
]

kernel_list = ("Pyslvs", "Python-Solvespace", "Sketch Solve")
