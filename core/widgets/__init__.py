# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .custom import CustomizeFunc
from .custom_io import IOFunc
from .custom_entities import EntitiesCmds
from .custom_storage import StorageFunc

__all__ = [
    'CustomizeFunc',
    'IOFunc',
    'EntitiesCmds',
    'StorageFunc',
]
