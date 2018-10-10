# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .script import ScriptDialog, slvs_process_script
from .slvs import SlvsParser
from .logging_handler import XStream
from .output_option import SlvsOutputDialog, DxfOutputDialog
from .database import DatabaseWidget
from .pyslvs_yaml import YamlEditor
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
    'slvs_process_script',
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
    'SlvsParser',
    'SlvsOutputDialog',
    'DxfOutputDialog',
    'XStream',
    'DatabaseWidget',
    'YamlEditor',
    'strbetween',
    'strbefore',
]


def strbetween(s: str, front: str, back: str) -> str:
    """Get from parenthesis."""
    return s[(s.find(front) + 1):s.find(back)]


def strbefore(s: str, front: str) -> str:
    """Get from parenthesis."""
    return s[:s.find(front)]
