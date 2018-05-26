# -*- coding: utf-8 -*-

"""Solvespace format output as linkage sketch."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List
from core.libs import VPoint
from core.graphics import convex_hull
from .write import (
    header_group,
    header_param,
    header_request,
    header_entity,
    save_slvs,
)


def slvs_part(vpoints: List[VPoint], radius: float, file_name: str):
    """TODO: Generate a linkage sketch by specified radius."""
    pos = convex_hull([vpoint.c[0] for vpoint in vpoints])
    
    #File headers of default framework.
    script_param = header_param()
    script_request = header_request()
    script_entity = header_entity()
    script_constraint = []
    
    #Write file
    save_slvs(
        file_name,
        header_group(),
        script_param,
        script_request,
        script_entity,
        script_constraint
    )
