# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List


class SlvsParser:
    
    """"""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
    
    def isValid(self) -> bool:
        """Simple check whether if file is valid."""
        with open(self.file_name, 'r', encoding="iso-8859-15") as f:
            first_line = f.readline()
        print(first_line)
        return True
    
    def layouts(self) -> List[str]:
        """Read and return layout names."""
        layouts = []
        with open(self.file_name, 'r', encoding="iso-8859-15") as f:
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
    
    def parse(self) -> str:
        """TODO: Parse as PMKS expression."""
        return ""
