# -*- coding: utf-8 -*-

"""Solvespace format output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Iterator,
)


class SlvsParser:
    
    """Use to read data from solvespace file format."""
    
    def __init__(self, file_name: str):
        """Open the file when initialize."""
        self.f = open(file_name, 'r', encoding="iso-8859-15")
    
    def isValid(self) -> bool:
        """Simple check whether if file is valid."""
        self.f.seek(0)
        return self.f.readline() == "±²³SolveSpaceREVa\n"
    
    def __readBlock(self,
        start: str,
        end: str,
        *,
        match: Tuple[str, str] = None
    ) -> Iterator[Tuple[str, str]]:
        """A generator can scan around of the file.
        
        parameter:
        + match: Skip the block when the data of attribute is not correct.
        """
        self.f.seek(0)
        lock = False
        for line in self.f:
            if start in line:
                lock = True
            if end in line:
                lock = False
            if (not lock) or ('=' not in line):
                continue
            attribute, data = line[:-1].split('=')
            if match is not None:
                if (attribute == match[0]) and (data != match[1]):
                    lock = False
                    continue
            yield attribute, data
    
    def layouts(self) -> List[str]:
        """Read and return layout names."""
        layouts = []
        for attribute, data in self.__readBlock('Group.h.v', 'AddGroup'):
            #Number code and layout name.
            if attribute == 'Group.h.v':
                layouts.append(data)
            elif attribute == 'Group.name':
                layouts[-1] += ':' + data
        return layouts[1:]
    
    def parse(self, layout: str) -> str:
        """Parse as PMKS expression.
        
        + Requests: Get all linkages.
            + Independence points will be ignored.
        + Constraint: Adjacency.
            + Collecting linkages for each point.
        + Entities: Get positions.
        """
        layout = layout.split(':')[0]
        
        #Requests: Get all linkages.
        wrong_type = False
        requests = []
        for attribute, data in self.__readBlock('Request.h.v', 'AddRequest'):
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
        
        #Constraint: Adjacency.
        self.f.seek(0)
        now_replace = 0x0
        for attribute, data in self.__readBlock(
            'Constraint.h.v',
            'AddConstraint',
            match=('Constraint.type', '20')
        ):
            if attribute == 'Constraint.ptA.v':
                now_replace = int(data, 16)
            elif attribute == 'Constraint.ptB.v':
                for vlink in vlinks.values():
                    num = int(data, 16)
                    if num in vlink:
                        vlink.remove(num)
                        vlink.add(now_replace)
        
        #Grounded. Other linkages at least will greater than 4.
        vlinks[0] = set()
        lock = False
        self.f.seek(0)
        for attribute, data in self.__readBlock(
            'Constraint.h.v',
            'AddConstraint',
            match=('Constraint.type', '31')
        ):
            if attribute == 'Constraint.ptA.v':
                vlinks[0].add(int(data, 16))
        
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
                vlinks['link_{}'.format(i - 1)] = vlinks.pop(name)
        
        exprs = []
        for num in points:
            x, y = pos[num]
            links = [name for name, link in vlinks.items() if (num in link)]
            exprs.append("J[R, color[Green], P[{}, {}], L[{}]]".format(
                x, y, ", ".join(links)
            ))
        
        return "M[{}]".format(", ".join(exprs))
    
    def close(self):
        """Close the file."""
        self.f.close()
