# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .script_io import ScriptDialog, slvsProcessScript
from .undo_redo import (
    AddTable, DeleteTable,
    FixSequenceNumber,
    EditPointTable, EditLinkTable,
    AddPath, DeletePath,
    AddStorage, DeleteStorage,
    AddStorageName, ClearStorageName,
    AddVariable, DeleteVariable,
)
from .images import QTIMAGES
from .slvs_io import slvs2D
from .dxf_io import dxfSketch
from .loggingHandler import XStream
from .peewee_io import FileWidget

__all__ = [
    'ScriptDialog',
    'slvsProcessScript',
    'AddTable',
    'DeleteTable',
    'FixSequenceNumber',
    'EditPointTable',
    'EditLinkTable',
    'AddPath',
    'DeletePath',
    'AddStorage',
    'DeleteStorage',
    'AddStorageName',
    'ClearStorageName',
    'AddVariable',
    'DeleteVariable',
    'QTIMAGES',
    'slvs2D',
    'dxfSketch',
    'XStream',
    'FileWidget',
    'strbetween',
    'strbefore',
]


def strbetween(s: str, front: str, back: str) -> str:
    """Get from parenthesis."""
    return s[(s.find(front) + 1):s.find(back)]


def strbefore(s: str, front: str) -> str:
    """Get from parenthesis."""
    return s[:s.find(front)]
