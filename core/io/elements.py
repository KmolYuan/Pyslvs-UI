# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
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

from math import sqrt, degrees, atan
from ..graphics.color import colorQt
from typing import List, Tuple

class VPoint:
    def __init__(self,
        links: str ='',
        type: int =0,
        angle: float =0.,
        color: str ='Red',
        x: float =0.,
        y: float =0.
    ):
        self.set(links, type, angle, color, x, y)
        self.__cx = self.__x
        self.__cy = self.__y
    
    @property
    def links(self):
        links = self.__links.split(',')
        return tuple(filter(lambda a: a!='', links))
    
    @property
    def type(self) -> int:
        return self.__type
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    @property
    def color(self) -> 'QColor':
        return colorQt(self.__color)
    
    @property
    def colorSTR(self) -> str:
        return self.__color
    
    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y
    
    @property
    def cx(self) -> float:
        return self.__cx
    
    @property
    def cy(self) -> float:
        return self.__cy
    
    def set(self, links, type, angle, color, x, y):
        self.__links = links
        self.__type = type
        self.__angle = angle
        self.__color = color
        self.__x = x
        self.__y = y
    
    def round(self, d=8):
        self.__x = round(self.__x, d)
        self.__y = round(self.__y, d)
    
    def move(self, x=None, y=None):
        if x==None:
            x = self.__x
        if y==None:
            y = self.__y
        self.__cx = x
        self.__cy = y
    
    def reset(self):
        self.__x = self.__cx
        self.__y = self.__cy
    
    def distance(self, p):
        return round(sqrt((self.x-p.x)**2+(self.y-p.y)**2), 4)
    
    def slopeAngle(self, p):
        try:
            return degrees(atan(p.y-self.y/p.x-self.x))
        except ZeroDivisionError:
            return 90.

class VLink:
    def __init__(self, name: str, color: str, points: Tuple[int]):
        self.set(name, color, points)
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def color(self) -> 'QColor':
        return colorQt(self.__color)
    
    @property
    def colorSTR(self) -> str:
        return self.__color
    
    @property
    def points(self) -> Tuple[int]:
        return self.__points
    
    def set(self, name, color, points):
        self.__name = name
        self.__color = color
        self.__points = points
    
    def __contains__(self, point):
        return point in self.points

class VPath:
    def __init__(self,
        point: int =0,
        points: List[Tuple[int, int]] =[],
        show: bool =True
    ):
        self.set(point, points, show)
    
    @property
    def point(self):
        return self.__point
    
    @property
    def path(self):
        return self.__path
    
    def set(self, point=0, points=[], show=True):
        self.__point = point
        self.__path = []
        self.show = show
        if points:
            for p in points:
                PointType = type(p)
                if PointType==tuple or PointType==list or p==None:
                    #(x, y)
                    self.__path.append(p)
    
    def isBroken(self):
        for point in self.path:
            if point is False or point[0] is False:
                return True
        return False

class VPaths:
    def __init__(self,
        shaft: int =0,
        paths: List[VPath] =[]
    ):
        self.set(shaft, paths)
    
    @property
    def shaft(self):
        return self.__shaft
    
    @property
    def paths(self):
        return self.__paths
    
    def set(self, shaft=0, paths=[]):
        self.__shaft = shaft
        self.__paths = []
        if paths:
            for path in paths:
                if type(path)==VPath:
                    self.__paths.append(path)
    
    def isBroken(self):
        for path in self.paths:
            if path.isBroken():
                return True
        return False
