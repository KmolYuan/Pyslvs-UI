# -*- coding: utf-8 -*-

"""'io' module contains Pyslvs IO and undo redo functions."""

__all__ = [
    'ScriptDialog',
    'slvs_process_script',
    'SlvsParser',
    'SlvsOutputDialog',
    'DxfOutputDialog',
    'OverviewDialog',
    'ProjectWidget',
    'PreferencesDialog',
    'str_between',
    'str_before',
]
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .script import ScriptDialog, slvs_process_script
from .slvs import SlvsParser
from .output_option import SlvsOutputDialog, DxfOutputDialog
from .overview import OverviewDialog
from .project import ProjectWidget
from .preferences import PreferencesDialog


def str_between(s: str, front: str, back: str) -> str:
    """Get from parenthesis."""
    return s[(s.find(front) + 1):s.find(back)]


def str_before(s: str, front: str) -> str:
    """Get from parenthesis."""
    return s[:s.find(front)]
