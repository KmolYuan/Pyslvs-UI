# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from . import solver as _solver
from . import actions as _actions
from . import io as _io
from . import entities as _entities
from . import storage as _storage

__all__ = [
    '_solver',
    '_actions',
    '_io',
    '_entities',
    '_storage',
]
