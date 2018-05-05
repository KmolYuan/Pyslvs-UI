# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .custom import initCustomWidgets
from . import solver_method as _solver
from . import actions_method as _actions
from . import io_method as _io
from . import entities_method as _entities
from . import storage_method as _storage

__all__ = [
    'initCustomWidgets',
    '_solver',
    '_actions',
    '_io',
    '_entities',
    '_storage',
]
