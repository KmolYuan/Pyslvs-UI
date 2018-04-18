# -*- coding: utf-8 -*-

"""'graphics' module contains custom display widgets."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .color import (
    colorNum,
    colorName,
    colorIcons,
    colorQt,
    colorPath
)
from .chart import DataChart
from .canvas import (
    BaseCanvas,
    PreviewCanvas,
    convex_hull,
    edges_view,
    replace_by_dict,
)
from .nx_pydot import (
    graph,
    engine_picker,
    EngineList,
    EngineError,
)

__all__ = [
    'colorNum',
    'colorName',
    'colorIcons',
    'colorQt',
    'colorPath',
    'DataChart',
    'BaseCanvas',
    'PreviewCanvas',
    'convex_hull',
    'edges_view',
    'replace_by_dict',
    'graph',
    'engine_picker',
    'EngineList',
    'EngineError',
]
