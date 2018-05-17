# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .script import ScriptDialog, slvsProcessScript
from .images import QTIMAGES
from .slvs import (
    SlvsParser,
    slvs_output,
)
from .dxf import dxfSketch
from .loggingHandler import XStream
from .peewee import FileWidget
from .undo_redo import (
    AddTable, DeleteTable,
    FixSequenceNumber,
    EditPointTable, EditLinkTable,
    AddPath, DeletePath,
    AddStorage, DeleteStorage,
    AddStorageName, ClearStorageName,
    AddVariable, DeleteVariable,
)

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
    'SlvsParser',
    'slvs_output',
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
