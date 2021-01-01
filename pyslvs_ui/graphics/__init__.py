# -*- coding: utf-8 -*-

"""'graphics' module contains custom display widgets."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .color import color_num, color_icon, color_qt, target_path_style
from .chart import DataChart, DataChartDialog
from .canvas import (
    LINK_COLOR, BaseCanvas, AnimationCanvas, PreviewCanvas, convex_hull,
    RangeDetector,
)
from .nx_layout import graph2icon, engine_picker, engines
from .path_parser import parse_path
