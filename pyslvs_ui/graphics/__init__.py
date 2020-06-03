# -*- coding: utf-8 -*-

"""'graphics' module contains custom display widgets."""

__all__ = [
    'color_num',
    'color_names',
    'color_icon',
    'color_qt',
    'target_path_style',
    'DataChart',
    'DataChartDialog',
    'LINK_COLOR',
    'BaseCanvas',
    'AnimationCanvas',
    'PreviewCanvas',
    'convex_hull',
    'RangeDetector',
    'graph2icon',
    'engine_picker',
    'engines',
    'parse_path',
]
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .color import (color_num, color_names, color_icon, color_qt,
                    target_path_style)
from .chart import DataChart, DataChartDialog
from .canvas import (LINK_COLOR, BaseCanvas, AnimationCanvas, PreviewCanvas,
                     convex_hull, RangeDetector)
from .nx_layout import graph2icon, engine_picker, engines
from .path_parser import parse_path
