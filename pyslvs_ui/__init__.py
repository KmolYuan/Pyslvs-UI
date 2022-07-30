# -*- coding: utf-8 -*-

"""Pyslvs-UI module."""

__version__ = "22.07.0"
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2022"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from warnings import warn
from pyslvs import __version__ as __kernel_version__

if __kernel_version__ != __version__:
    warn(Warning(f"Warning: Use kernel version {__kernel_version__}"))
