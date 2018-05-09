# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .scriptIO import ScriptDialog, slvsProcessScript
from .undoRedo import (
    AddTable, DeleteTable,
    FixSequenceNumber,
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
from .larkParser import parse, PMKSLexer
from .peeweeIO import FileWidget

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
    'parse',
    'PMKSLexer',
    'FileWidget',
    'strbetween',
    'strbefore',
]


"""Get from parenthesis."""
strbetween = lambda s, front, back: s[(s.find(front) + 1):s.find(back)]
strbefore = lambda s, front: s[:s.find(front)]
