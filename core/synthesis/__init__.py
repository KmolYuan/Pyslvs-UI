# -*- coding: utf-8 -*-

"""'synthesis' module contains synthesis functional interfaces."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .Collections import Collections, CollectionsDialog
from .StructureSynthesis import StructureSynthesis
from .DimensionalSynthesis import DimensionalSynthesis

__all__ = [
    'StructureSynthesis',
    'Collections',
    'CollectionsDialog',
    'DimensionalSynthesis'
]
