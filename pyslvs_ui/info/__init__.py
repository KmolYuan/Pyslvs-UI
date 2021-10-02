# -*- coding: utf-8 -*-

"""'info' module contains Pyslvs program information."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .info import (
    KERNELS, SYS_INFO, ARGUMENTS, HAS_SLVS, HAS_SCIPY, Kernel, parse_args,
)
from .about import PyslvsAbout, html, check_update
from .logging_handler import logger, sign_in_logger, XStream


def size_format(num: float) -> str:
    """Calculate file size based on binary."""
    if num < 0:
        raise ValueError("size must be positive value")
    s = "0 B"
    units = ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    for i, u in enumerate(units):
        s = f"{num:3.2f} {u}B"
        if abs(num) < 1024:
            break
        num /= 1024
    return s
