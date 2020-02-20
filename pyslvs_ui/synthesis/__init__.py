# -*- coding: utf-8 -*-

"""'synthesis' module contains synthesis functional interfaces."""

__all__ = [
    'StructureSynthesis',
    'Collections',
    'CollectionsDialog',
    'ConfigureWidget',
    'DimensionalSynthesis'
]
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .collections import Collections, CollectionsDialog, ConfigureWidget
from .structure_synthesis import StructureSynthesis
from .dimensional_synthesis import DimensionalSynthesis
