# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"graphics" module contains custom display widgets.
"""

from .color import (
    colorNum,
    colorName,
    colorIcons,
    colorQt
)
from .planarSolving import (
    slvsProcess,
    SlvsException
)
from .chart import dataChart
from .canvas import (
    BaseCanvas,
    PreviewCanvas,
    distance_sorted,
    edges_view,
    replace_by_dict
)
from .nx_pydot import (
    graph,
    engine_picker,
    EngineList,
    EngineError
)

__all__ = [
    'colorNum',
    'colorName',
    'colorIcons',
    'colorQt',
    'slvsProcess',
    'SlvsException',
    'dataChart',
    'BaseCanvas',
    'PreviewCanvas',
    'distance_sorted',
    'edges_view',
    'replace_by_dict',
    'graph',
    'engine_picker',
    'EngineList',
    'EngineError'
]
