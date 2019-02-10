# -*- coding: utf-8 -*-

"""'dialogs' module contains
contains the dialog of this tab.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .options import (
    GeneticPrams,
    FireflyPrams,
    defaultSettings,
    DifferentialPrams,
    AlgorithmType,
    AlgorithmOptionDialog
)
from .path_adjust import PathAdjustDialog
from .progress import ProgressDialog
from .preview import PreviewDialog
from .chart import ChartDialog

__all__ = [
    'GeneticPrams',
    'FireflyPrams',
    'defaultSettings',
    'DifferentialPrams',
    'AlgorithmType',
    'AlgorithmOptionDialog',
    'PathAdjustDialog',
    'ProgressDialog',
    'PreviewDialog',
    'ChartDialog'
]
