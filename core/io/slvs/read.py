# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List


class SlvsParser:
    
    """Use to read data from solvespace file format."""
    
    def __init__(self, file_name: str):
        """Open the file when initialize."""
        self.f = open(file_name, 'r', encoding="iso-8859-15")
    
    def isValid(self) -> bool:
        """Simple check whether if file is valid."""
        self.f.seek(0)
        first_line = self.f.readline()
        return first_line == "±²³SolveSpaceREVa\n"
    
    def layouts(self) -> List[str]:
        """Read and return layout names."""
        layouts = []
        self.f.seek(0)
        for line in self.f:
            if ('Group.h.v' not in line) and ('Group.name' not in line):
                continue
            
            attribute, data = line[:-1].split('=')
            
            #Number code and layout name.
            if attribute == 'Group.h.v':
                layouts.append(data)
            elif attribute == 'Group.name':
                layouts[-1] += ':' + data
        return layouts
    
    def parse(self, layout: str) -> str:
        """Parse as PMKS expression.
        
        + Requests: Get all linkages.
            + Independence points will be ignored.
        + Entities: Get positions.
        """
        #Block handle.
        lock = False
        
        #Requests: Get all linkages.
        self.f.seek(0)
        wrong_type = False
        requests = []
        for line in self.f:
            if 'Request.h.v' in line:
                lock = True
            if 'AddRequest' in line:
                lock = False
            if not lock:
                continue
            
            attribute, data = line[:-1].split('=')
            
            #Append data first, if wrong, just remove it.
            if attribute == 'Request.h.v':
                #4<<16 -> 262144
                requests.append(int(data, 16) << 16)
            elif attribute == 'Request.type':
                wrong_type = data != '200'
                if wrong_type:
                    del requests[-1]
            elif not wrong_type and (attribute == 'Request.group.v'):
                if data != layout:
                    del requests[-1]
        
        #TODO: Can be simplify.
        #Entities: Get positions.
        self.f.seek(0)
        in_p1 = False
        in_p2 = False
        request_index = 0
        entities = {}
        for line in self.f:
            if 'Entity.h.v' in line:
                lock = True
            if 'AddEntity' in line:
                lock = False
            if not lock:
                if in_p2:
                    #Next entity.
                    request_index += 1
                    if request_index == len(requests):
                        break
                in_p1 = False
                in_p2 = False
                continue
            
            num = requests[request_index]
            attribute, data = line[:-1].split('=')
            
            if attribute == 'Entity.type':
                #Line and it's points.
                if data not in ('11000', '2001'):
                    lock = False
                    continue
            
            if attribute == 'Entity.h.v':
                if data == "{:08x}".format(num):
                    entities[num] = ([], [])
                elif data == "{:08x}".format(num + 1):
                    in_p1 = True
                elif data == "{:08x}".format(num + 2):
                    in_p1 = False
                    in_p2 = True
            elif 'Entity.actPoint.' in attribute:
                #X or Y value.
                if in_p1:
                    entities[num][0].append(float(data))
                elif in_p2:
                    entities[num][1].append(float(data))
        
        return ""
    
    def close(self):
        """Close the file."""
        self.f.close()
