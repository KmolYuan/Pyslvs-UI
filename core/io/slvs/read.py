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
        + Constraint: Adjacency.
            + Collecting linkages for each point.
        + Entities: Get positions.
        """
        layout = layout.split(':')[0]
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
                #4 << 16 == 0x40000
                requests.append(int(data, 16) << 16)
            elif attribute == 'Request.type':
                wrong_type = data != '200'
                if wrong_type:
                    del requests[-1]
            elif not wrong_type and (attribute == 'Request.group.v'):
                if data != layout:
                    del requests[-1]
        
        vlinks = {link: {link + 1, link + 2} for link in requests}
        
        #TODO: Grounded.
        #Constraint: Adjacency.
        self.f.seek(0)
        is_multiple = False
        now_replace = 0x0
        for line in self.f:
            if 'Constraint.h.v' in line:
                lock = True
            if 'AddConstraint' in line:
                lock = False
            if not lock:
                is_multiple = False
                continue
            
            attribute, data = line[:-1].split('=')
            
            if attribute == 'Constraint.type':
                if data == '20':
                    is_multiple = True
            
            if not is_multiple:
                continue
            
            if attribute == 'Constraint.ptA.v':
                now_replace = int(data, 16)
            elif attribute == 'Constraint.ptB.v':
                for vlink in vlinks.values():
                    num = int(data, 16)
                    if num in vlink:
                        vlink.remove(num)
                        vlink.add(now_replace)
        
        pos = {}
        for vlink in vlinks.values():
            for point in vlink:
                if point not in pos:
                    pos[point] = []
        
        points = sorted(pos)
        
        #Entities: Get positions.
        self.f.seek(0)
        in_c = False
        point = 0
        for line in self.f:
            if 'Entity.h.v' in line:
                lock = True
            if 'AddEntity' in line:
                lock = False
            if not lock:
                if in_c:
                    #Next entity.
                    point += 1
                    if point == len(points):
                        break
                in_c = False
                continue
            
            num = points[point]
            attribute, data = line[:-1].split('=')
            
            if attribute == 'Entity.type':
                #Line and it's points.
                if data not in ('11000', '2001'):
                    lock = False
                    continue
            
            if attribute == 'Entity.h.v':
                if data == "{:08x}".format(num):
                    in_c = True
            elif in_c and ('Entity.actPoint.' in attribute):
                #X or Y value.
                pos[num].append(float(data))
        
        #Rename link names.
        for i, name in enumerate(sorted(vlinks)):
            if i == 0:
                vlinks['ground'] = vlinks.pop(name)
            else:
                vlinks['link_{}'.format(i)] = vlinks.pop(name)
        
        exprs = []
        for num in points:
            x, y = pos[num]
            links = [name for name, link in vlinks.items() if (num in link)]
            exprs.append("J[R, color[Green], P[{}, {}], L[{}]]".format(
                x, y, ", ".join(links)
            ))
        print(exprs)
        return "M[{}]".format(", ".join(exprs))
    
    def close(self):
        """Close the file."""
        self.f.close()
