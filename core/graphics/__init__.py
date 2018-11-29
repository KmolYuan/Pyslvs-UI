# -*- coding: utf-8 -*-

"""'graphics' module contains custom display widgets."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .color import (
    color_num,
    colorNames,
    color_icon,
    color_qt,
    target_path_style
)
from .chart import DataChart
from .canvas import (
    BaseCanvas,
    PreviewCanvas,
    convex_hull,
    edges_view,
    graph2vpoints,
)
from .nx_layout import (
    to_graph,
    engine_picker,
    engines,
    EngineError,
)

__all__ = [
    'color_num',
    'colorNames',
    'color_icon',
    'color_qt',
    'target_path_style',
    'DataChart',
    'BaseCanvas',
    'PreviewCanvas',
    'convex_hull',
    'edges_view',
    'graph2vpoints',
    'to_graph',
    'engine_picker',
    'engines',
    'EngineError',
]
