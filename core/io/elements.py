# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from math import sqrt, degrees, atan2
from networkx import Graph
from core.graphics import colorQt
from typing import Tuple

class VPoint:
    __slots__ = ('__links', '__type', '__angle', '__color', '__x', '__y', '__c')
    Jtype = ('R', 'P', 'RP')
    
    def __init__(self,
        links: str ='',
        type: int =0,
        angle: float =0.,
        color: str ='Red',
        x: float =0.,
        y: float =0.
    ):
        self.set(links, type, angle, color, x, y)
        self.reset()
    
    @property
    def links(self):
        return self.__links
    
    def setLinks(self, links: str):
        self.__links = tuple(filter(lambda a: a!='', links.split(',')))
    
    @property
    def type(self) -> int:
        return self.__type
    
    @property
    def typeSTR(self) -> str:
        return self.Jtype[self.type]
    
    def setType(self, type: int):
        self.__type = type
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    def setAngle(self, angle: float):
        self.__angle = angle
    
    @property
    def color(self) -> 'QColor':
        return colorQt(self.__color)
    
    @property
    def colorSTR(self) -> str:
        return self.__color
    
    def setColor(self, color: str):
        self.__color = color
    
    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y
    
    def setCoordinate(self, x: float, y: float):
        self.__x = x
        self.__y = y
    
    @property
    def cx(self) -> float:
        return self.__c[0][0]
    
    @property
    def cy(self) -> float:
        return self.__c[0][1]
    
    #Get the coordinates of all pin.
    @property
    def c(self) -> Tuple[Tuple[float, float]]:
        return self.__c
    
    def set(self, links, type, angle, color, x, y):
        self.__links = tuple(filter(lambda a: a!='', links.split(',')))
        self.__type = type
        self.__angle = angle
        self.__color = color
        self.__x = x
        self.__y = y
    
    def round(self, d=8):
        self.__c = tuple(tuple(round(p, d) for p in coordinate) for coordinate in self.__c)
    
    def move(self, *coordinates):
        self.__c = tuple(coordinates)
    
    def reset(self):
        if self.type==1 or self.type==2:
            self.__c = tuple((self.x, self.y) for i in range(len(self.links)))
        else:
            self.__c = ((self.x, self.y),)
    
    def distance(self, p):
        return round(sqrt((self.x-p.x)**2 + (self.y-p.y)**2), 4)
    
    def slopeAngle(self, p):
        return round(degrees(atan2(p.y-self.y, p.x-self.x)), 4)
    
    @property
    def expr(self):
        return "J[{}, color[{}], P[{}], L[{}]]".format(
            "{}, A[{}]".format(self.typeSTR, self.angle) if self.typeSTR!='R' else 'R',
            self.colorSTR,
            "{}, {}".format(self.x, self.y),
            ", ".join(l for l in self.links)
        )
    
    def __repr__(self):
        return "VPoint({p.links}, {p.type}, {p.angle}, {p.c})".format(p=self)

class VLink:
    __slots__ = ('__name', '__color', '__points')
    
    def __init__(self, name: str, color: str, points: Tuple[int]):
        self.set(name, color, points)
    
    @property
    def name(self) -> str:
        return self.__name
    
    def setName(self, name: str):
        self.__name = name
    
    @property
    def color(self) -> 'QColor':
        return colorQt(self.__color)
    
    @property
    def colorSTR(self) -> str:
        return self.__color
    
    def setColor(self, color: str):
        self.__color = color
    
    @property
    def points(self) -> Tuple[int]:
        return self.__points
    
    def setPoints(self, points: Tuple[int]):
        self.__points = points
    
    def set(self, name, color, points):
        self.__name = name
        self.__color = color
        self.__points = points
    
    def __contains__(self, point):
        return point in self.points
    
    def __repr__(self):
        return "VLink('{l.name}', {l.points})".format(l=self)

#Generalization chain
def v_to_graph(jointData: Tuple[VPoint,], linkData: Tuple[VLink,]):
    G = Graph()
    #Links name for RP joint.
    k = len(linkData)
    used_point = []
    for i, vlink in enumerate(linkData):
        for p in vlink.points:
            if p in used_point:
                continue
            match = [m for m, vlink_ in enumerate(linkData) if i!=m and (p in vlink_.points)]
            for m in match:
                if jointData[p].type==2:
                    G.add_edge(i, k)
                    G.add_edge(k, m)
                    k += 1
                else:
                    G.add_edge(i, m)
            used_point.append(p)
    return G

#Solvespace edges
def v_to_slvs(jointData: Tuple[VPoint,], linkData: Tuple[VLink,]):
    edges = []
    for vlink in linkData:
        if vlink.name=='ground':
            continue
        for i, p in enumerate(vlink.points):
            if i==0:
                continue
            edges.append((vlink.points[0], p))
            if i>1:
                edges.append((vlink.points[i-1], p))
    return tuple(edges)
