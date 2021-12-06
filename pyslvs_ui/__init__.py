# -*- coding: utf-8 -*-

"""Pyslvs-UI module."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"
__version__ = "21.12.0"

from warnings import warn
from pyslvs import __version__ as __kernel_version__

if __kernel_version__ != __version__:
    warn(Warning(f"Warning: Use kernel version {__kernel_version__}"))
