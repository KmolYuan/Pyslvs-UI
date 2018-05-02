# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .scriptIO import ScriptDialog
from .undoRedo import (
    AddTable, DeleteTable, FixSequenceNumber,
    EditPointTable, EditLinkTable,
    AddPath, DeletePath,
    AddStorage, DeleteStorage,
    AddStorageName, ClearStorageName,
    AddVariable, DeleteVariable,
)
from .images import QTIMAGES
from .slvsIO import slvs2D
from .dxfIO import dxfSketch
from .loggingHandler import XStream
from .larkParser import (
    PMKS_parser,
    PMKSArgsTransformer,
)
from .peeweeIO import FileWidget

__all__ = [
    'ScriptDialog',
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
    'PMKS_parser',
    'PMKSArgsTransformer',
    'strbetween',
    'strbefore',
    'FileWidget'
]


"""Get from parenthesis."""
strbetween = lambda s, front, back: s[(s.find(front) + 1):s.find(back)]
strbefore = lambda s, front: s[:s.find(front)]
