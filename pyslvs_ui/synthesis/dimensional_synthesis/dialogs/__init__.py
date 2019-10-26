# -*- coding: utf-8 -*-

"""'dialogs' module contains
contains the dialog of this tab.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .options import (
    GENETIC_PARAMS,
    FIREFLY_PARAMS,
    DEFAULT_PARAMS,
    DIFFERENTIAL_PARAMS,
    AlgorithmType,
    AlgorithmOptionDialog
)
from .edit_path import EditPathDialog
from .progress import ProgressDialog
from .preview import PreviewDialog
from .chart import ChartDialog

__all__ = [
    'GENETIC_PARAMS',
    'FIREFLY_PARAMS',
    'DEFAULT_PARAMS',
    'DIFFERENTIAL_PARAMS',
    'AlgorithmType',
    'AlgorithmOptionDialog',
    'EditPathDialog',
    'ProgressDialog',
    'PreviewDialog',
    'ChartDialog'
]
