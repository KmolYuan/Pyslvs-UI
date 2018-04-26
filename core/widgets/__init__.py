# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .custom import initCustomWidgets
from . import custom_io as _io
from . import custom_entities as _entities
from . import custom_storage as _storage

__all__ = [
    'initCustomWidgets',
    '_io',
    '_entities',
    '_storage',
]
