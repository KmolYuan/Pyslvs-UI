# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List


def slvs_layouts(file_name: str) -> List[str]:
    """Read and return layout names."""
    layouts = []
    with open(file_name, 'r', encoding="iso-8859-15") as f:
        group_buffer = []
        for line in f:
            if ('Group.h.v' in line) or ('Group.name' in line):
                group_buffer.append(line)
        for group_data in group_buffer:
            attribute, data = group_data.split('=')
            data = data.replace('\n', '')
            #Number code and layout name.
            if attribute == 'Group.h.v':
                layouts.append(data)
            elif attribute == 'Group.name':
                layouts[-1] += ':' + data
    return layouts
