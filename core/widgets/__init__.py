# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .custom import MainWindowBase
from .tables import PointTableWidget, LinkTableWidget
from .undo_redo import (
    AddTable,
    AddPath,
    AddStorage,
    AddStorageName,
    AddVariable,
    ClearStorageName,
    DeletePath,
    DeleteStorage,
    DeleteTable,
    DeleteVariable,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)

__all__ = [
    'MainWindowBase',
    'PointTableWidget',
    'LinkTableWidget',
    'AddTable',
    'AddPath',
    'AddStorage',
    'AddStorageName',
    'AddVariable',
    'ClearStorageName',
    'DeletePath',
    'DeleteStorage',
    'DeleteTable',
    'DeleteVariable',
    'EditPointTable',
    'EditLinkTable',
    'FixSequenceNumber',
]
