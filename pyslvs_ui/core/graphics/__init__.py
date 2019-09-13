# -*- coding: utf-8 -*-

"""'graphics' module contains custom display widgets."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .color import (
    color_num,
    color_names,
    color_icon,
    color_qt,
    target_path_style
)
from .chart import DataChart
from .canvas import (
    BaseCanvas,
    PreviewCanvas,
    convex_hull,
)
from .nx_layout import (
    graph2icon,
    engine_picker,
    engines,
)

__all__ = [
    'color_num',
    'color_names',
    'color_icon',
    'color_qt',
    'target_path_style',
    'DataChart',
    'BaseCanvas',
    'PreviewCanvas',
    'convex_hull',
    'graph2icon',
    'engine_picker',
    'engines',
]
