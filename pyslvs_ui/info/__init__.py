# -*- coding: utf-8 -*-

"""'info' module contains Pyslvs program information."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .info import KERNELS, SYS_INFO, ARGUMENTS, HAS_SLVS, HAS_SCIPY, Kernel
from .about import PyslvsAbout, html, check_update
from .logging_handler import logger, XStream


def size_format(num: float) -> str:
    """Calculate file size."""
    if num <= 0:
        return "0 B"
    for u in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(num) < 1024:
            return f"{num:3.1f} {u}B"
        num /= 1024
    return f"{num:.1f} YB"
