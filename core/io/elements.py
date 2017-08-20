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

from math import sqrt

class VList:
    def __init__(self):
        self.__list = []
    
    def __getitem__(self, i):
        return self.__list[i]
    
    def pop(self):
        return self.__list.pop()

class VPoint:
    def __init__(self, x=0., y=0., fix=False, color='Red'):
        self.set(x, y, fix)
        self.setColor(color)
        self.__cx = self.__x
        self.__cy = self.__y
    
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @x.setter
    def x(self, x):
        self.__x = x
    @y.setter
    def y(self, y):
        self.__y = y
    @property
    def fix(self):
        return self.__fix
    @property
    def color(self):
        return self.__color
    @property
    def cx(self):
        return self.__cx
    @property
    def cy(self):
        return self.__cy
    
    def set(self, x, y, fix):
        self.__x = x
        self.__y = y
        self.__fix = fix
    
    def round(self, d=8):
        self.__x = round(self.__x, d)
        self.__y = round(self.__y, d)
    
    def setColor(self, color='Red'):
        self.__color = color
    
    def move(self, x=None, y=None):
        if x==None:
            x = self.__x
        if y==None:
            y = self.__y
        self.__cx = x
        self.__cy = y
    
    def distance(self, p):
        return round(sqrt((self.cx-p.cx)**2+(self.cy-p.cy)**2), 4)
    
    def reset(self):
        self.__x = self.__cx
        self.__y = self.__cy
    
    def items(self, index=0):
        return ('Point{}'.format(index), self.x, self.y, self.fix, self.color)
    def items_tags(self, index=0):
        return ('Point{}'.format(index), ('x', self.x), ('y', self.y), ('fix', self.fix), ('color', self.color))

class VPointList(VList):
    def __init__(self):
        self.__list = [VPoint(fix=True)]
    
    def add(self, x, y, fix, color):
        self.__list.append(VPoint(x, y, fix, color))

class VLine:
    def __init__(self, start=0, end=0, len=0.):
        self.set(start, end, len)
    
    @property
    def start(self):
        return self.__start
    @property
    def end(self):
        return self.__end
    @property
    def len(self):
        return self.__len
    
    def set(self, start, end, len):
        self.__start = start
        self.__end = end
        self.__len = len
    
    def items(self, index=0):
        return ('Line{}'.format(index), self.start, self.end, self.len)
    def items_tags(self, index=0):
        return ('Line{}'.format(index), ('start', self.start), ('end', self.end), ('len', self.len))
    
    def __contains__(self, point):
        return point==self.start or point==self.end

class VLineList(VList):
    def add(self, start, end, len):
        self.__list.append(VLine(start, end, len))

class VChain:
    def __init__(self, p1=VPoint(), p2=0, p3=0, p1p2=0., p2p3=0., p1p3=0.):
        self.set(p1, p2, p3, p1p2, p2p3, p1p3)
    
    @property
    def p1(self):
        return self.__p1
    @property
    def p2(self):
        return self.__p2
    @property
    def p3(self):
        return self.__p3
    @property
    def p1p2(self):
        return self.__p1p2
    @property
    def p2p3(self):
        return self.__p2p3
    @property
    def p1p3(self):
        return self.__p1p3
    
    def set(self, p1, p2, p3, p1p2, p2p3, p1p3):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        self.__p1p2 = p1p2
        self.__p2p3 = p2p3
        self.__p1p3 = p1p3
    
    def items(self, index=0):
        return ('Chain{}'.format(index), self.p1, self.p2, self.p3, self.p1p2, self.p2p3, self.p1p3)
    def items_tags(self, index=0):
        return ('Chain{}'.format(index), ('p1', self.p1), ('p2', self.p2), ('p3', self.p3), ('p1p2', self.p1p2), ('p2p3', self.p2p3), ('p1p3', self.p1p3))
    
    def __contains__(self, point):
        return point==self.p1 or point==self.p2 or point==self.p3

class VChainList(VList):
    def add(self, p1, p2, p3, p1p2, p2p3, p1p3):
        self.__list.append(VChain(p1, p2, p3, p1p2, p2p3, p1p3))

class VShaft:
    def __init__(self, cen=0, ref=0, start=0., end=360., demo=0.):
        self.set(cen, ref, start, end, demo)
    
    @property
    def cen(self):
        return self.__cen
    @property
    def ref(self):
        return self.__ref
    @property
    def start(self):
        return self.__start
    @property
    def end(self):
        return self.__end
    @property
    def demo(self):
        return self.__demo
    @demo.setter
    def demo(self, demo):
        self.__demo = demo
    
    def set(self, cen, ref, start, end, demo):
        self.__cen = cen
        self.__ref = ref
        self.__start = start
        self.__end = end
        self.__demo = demo
    
    def drive(self, demo):
        if demo>self.start and demo<self.end:
            self.__demo = demo
    
    def items(self, index=0):
        return ('Shaft{}'.format(index), self.cen, self.ref, self.start, self.end, self.demo)
    def items_tags(self, index=0):
        return ('Shaft{}'.format(index), ('cen', self.cen), ('ref', self.ref), ('start', self.start), ('end', self.end), ('demo', self.demo))
    
    def __contains__(self, point):
        return point==self.cen or point==self.ref

class VShaftList(VList):
    def add(self, cen, ref, start, end, demo):
        self.__list.append(VShaft(cen, ref, start, end, demo))

class VSlider:
    def __init__(self, cen=0, start=0, end=0):
        self.set(cen, start, end)
    
    @property
    def cen(self):
        return self.__cen
    @property
    def start(self):
        return self.__start
    @property
    def end(self):
        return self.__end
    
    def set(self, cen, start, end):
        self.__cen = cen
        self.__start = start
        self.__end = end
    
    def items(self, index=0):
        return ('Slider{}'.format(index), self.cen, self.start, self.end)
    def items_tags(self, index=0):
        return ('Slider{}'.format(index), ('cen', self.cen), ('start', self.start), ('end', self.end))
    
    def __contains__(self, point):
        return point==self.cen or point==self.start or point==self.end

class VSliderList(VList):
    def add(self, cen, start, end):
        self.__list.append(VSlider(cen, start, end))

class VRod(VSlider):
    def __init__(self, cen=0, start=0, end=0, pos=0.):
        self.set(cen, start, end, pos)
    
    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, pos):
        self.__pos = pos
    
    def set(self, cen=0, start=0, end=0, pos=0.):
        super(VRod, self).set(cen, start, end)
        self.__pos = pos
    
    def items(self, index=0):
        return ('Rod{}'.format(index), self.cen, self.start, self.end, self.pos)
    def items_tags(self, index=0):
        return ('Rod{}'.format(index), ('cen', self.cen), ('start', self.start), ('end', self.end), ('pos', self.pos))

class VRodList(VList):
    def add(self, cen, start, end, pos):
        self.__list.append(VRod(cen, start, end, pos))

class VParameter:
    def __init__(self, val=0., commit=''):
        self.set(val, commit)
    @property
    def val(self):
        return self.__val
    @property
    def commit(self):
        return self._commit
    
    def set(self, val=0., commit=''):
        self.__val = val
        self.__commit = commit
    
    def items(self, index=0):
        return ('n{}'.format(index), self.val, self.commit)
    def items_tags(self, index=0):
        return ('n{}'.format(index), ('val', self.val), ('commit', self.commit))

class VParameterList(VList):
    def add(self, val, commit):
        self.__list.append(VParameter(val, commit))

class VPath:
    def __init__(self, point=0, points=list(), show=True):
        self.set(point, points, show)
    
    @property
    def point(self):
        return self.__point
    @property
    def path(self):
        return self.__path
    @property
    def show(self):
        return self.__show
    @show.setter
    def show(self, show):
        self.__show = show
    
    def set(self, point=0, points=list(), show=True):
        self.__point = point
        self.__path = list()
        self.__show = show
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
    def __init__(self, shaft=0, paths=list()):
        self.set(shaft, paths)
    @property
    def shaft(self):
        return self.__shaft
    @property
    def paths(self):
        return self.__paths
    
    def set(self, shaft=0, paths=list()):
        self.__shaft = shaft
        self.__paths = list()
        if paths:
            for path in paths:
                if type(path)==VPath:
                    self.__paths.append(path)
    
    def isBroken(self):
        for path in self.paths:
            if path.isBroken():
                return True
        return False

class VPathsList(VList):
    def add(self, shaft, paths):
        self.__list.append(VPaths(shaft, paths))

if __name__=='__main__':
    a = VPoint(10, 20)
    print(a)
