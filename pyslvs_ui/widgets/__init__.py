# -*- coding: utf-8 -*-

"""'widgets' module contains the custom widgets
that design without Qt designer.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .main_base import MainWindowBase, Preferences
from .tables import PointArgs, LinkArgs, PointTableWidget, LinkTableWidget
from .undo_redo import (
    AddTable,
    AddPath,
    AddStorage,
    AddStorageName,
    AddInput,
    ClearStorageName,
    DeletePath,
    DeleteStorage,
    DeleteTable,
    DeleteInput,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)

__all__ = [
    'MainWindowBase',
    'Preferences',
    'PointArgs',
    'LinkArgs',
    'PointTableWidget',
    'LinkTableWidget',
    'AddTable',
    'AddPath',
    'AddStorage',
    'AddStorageName',
    'AddInput',
    'ClearStorageName',
    'DeletePath',
    'DeleteStorage',
    'DeleteTable',
    'DeleteInput',
    'EditPointTable',
    'EditLinkTable',
    'FixSequenceNumber',
]
