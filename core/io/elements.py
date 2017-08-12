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

class VPoint:
    def __init__(self, x=0., y=0., fix=False, color='Red'):
        self.set(x, y, fix)
        self.setColor(color)
        self._cx = self._x
        self._cy = self._y
    
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @x.setter
    def x(self, x):
        self._x = x
    @y.setter
    def y(self, y):
        self._y = y
    @property
    def fix(self):
        return self._fix
    @property
    def color(self):
        return self._color
    @property
    def cx(self):
        return self._cx
    @property
    def cy(self):
        return self._cy
    
    def set(self, x=0., y=0., fix=False):
        self._x = x
        self._y = y
        self._fix = fix
    
    def round(self, d=8):
        self._x = round(self._x, d)
        self._y = round(self._y, d)
    
    def setColor(self, color='Red'):
        self._color = color
    
    def move(self, x=None, y=None):
        if x==None:
            x = self._x
        if y==None:
            y = self._y
        self._cx = x
        self._cy = y
    
    def reset(self):
        self._x = self._cx
        self._y = self._cy
    
    def items(self, index=0):
        return ('Point{}'.format(index), self.x, self.y, self.fix, self.color)
    def items_tags(self, index=0):
        return ('Point{}'.format(index), ('x', self.x), ('y', self.y), ('fix', self.fix), ('color', self.color))
    
    def __str__(self):
        return "<Point x={v.x} y={v.y} fix={v.fix} cx={v.cx} cy={v.cy}>".format(v=self)

class VLine:
    def __init__(self, start=0, end=0, len=0.):
        self.set(start, end, len)
    
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._end
    @property
    def len(self):
        return self._len
    
    def set(self, start=VPoint(), end=VPoint(), len=0.):
        self._start = start
        self._end = end
        self._len = len
    
    def items(self, index=0):
        return ('Line{}'.format(index), self.start, self.end, self.len)
    def items_tags(self, index=0):
        return ('Line{}'.format(index), ('start', self.start), ('end', self.end), ('len', self.len))
    
    def __contains__(self, point):
        return point==self._start or point==self._end
    def __str__(self):
        return "<Line start={v.start} end={v.end} len={v.len}>".format(v=self)

class VChain:
    def __init__(self, p1=VPoint(), p2=0, p3=0, p1p2=0., p2p3=0., p1p3=0.):
        self.set(p1, p2, p3, p1p2, p2p3, p1p3)
    
    @property
    def p1(self):
        return self._p1
    @property
    def p2(self):
        return self._p2
    @property
    def p3(self):
        return self._p3
    @property
    def p1p2(self):
        return self._p1p2
    @property
    def p2p3(self):
        return self._p2p3
    @property
    def p1p3(self):
        return self._p1p3
    
    def set(self, p1=0, p2=0, p3=0, p1p2=0., p2p3=0., p1p3=0.):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._p1p2 = p1p2
        self._p2p3 = p2p3
        self._p1p3 = p1p3
    
    def items(self, index=0):
        return ('Chain{}'.format(index), self.p1, self.p2, self.p3, self.p1p2, self.p2p3, self.p1p3)
    def items_tags(self, index=0):
        return ('Chain{}'.format(index), ('p1', self.p1), ('p2', self.p2), ('p3', self.p3), ('p1p2', self.p1p2), ('p2p3', self.p2p3), ('p1p3', self.p1p3))
    
    def __contains__(self, point):
        return point==self._p1 or point==self._p2 or point==self._p3
    def __str__(self):
        return "<Chain p1={v.p1} p2={v.p2} p3={v.p3} p1p2={v.p1p2} p2p3={v.p2p3} p1p3={v.p1p3}>".format(v=self)

class VShaft:
    def __init__(self, cen=0, ref=0, start=0., end=360., demo=0.):
        self.set(cen, ref, start, end, demo)
    
    @property
    def cen(self):
        return self._cen
    @property
    def ref(self):
        return self._ref
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._end
    @property
    def demo(self):
        return self._demo
    @demo.setter
    def demo(self, demo):
        self._demo = demo
    
    def set(self, cen=0, ref=0, start=0., end=360., demo=0.):
        self._cen = cen
        self._ref = ref
        self._start = start
        self._end = end
        self._demo = demo
    
    def drive(self, demo):
        if demo>self._start and demo<self._end:
            self._demo = demo
    
    def items(self, index=0):
        return ('Shaft{}'.format(index), self.cen, self.ref, self.start, self.end, self.demo)
    def items_tags(self, index=0):
        return ('Shaft{}'.format(index), ('cen', self.cen), ('ref', self.ref), ('start', self.start), ('end', self.end), ('demo', self.demo))
    
    def __contains__(self, point):
        return point==self._cen or point==self._ref
    def __str__(self):
        return "<Shaft cen={v.cen} ref={v.ref} start={v.start}, end={v.end} demo={v.demo}".format(v=self)

class VSlider:
    def __init__(self, cen=0, start=0, end=0):
        self.set(cen, start, end)
    
    @property
    def cen(self):
        return self._cen
    @property
    def start(self):
        return self._start
    @property
    def end(self):
        return self._end
    
    def set(self, cen=0, start=0, end=0):
        self._cen = cen
        self._start = start
        self._end = end
    
    def items(self, index=0):
        return ('Slider{}'.format(index), self.cen, self.start, self.end)
    def items_tags(self, index=0):
        return ('Slider{}'.format(index), ('cen', self.cen), ('start', self.start), ('end', self.end))
    
    def __contains__(self, point):
        return point==self._cen or point==self._start or point==self._end
    def __str__(self):
        return "<Slider cen={v.cen} start={v.start} end={v.end}>".format(v=self)

class VRod(VSlider):
    def __init__(self, cen=0, start=0, end=0, pos=0.):
        self.set(cen, start, end, pos)
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, pos):
        self._pos = pos
    
    def set(self, cen=0, start=0, end=0, pos=0.):
        super(VRod, self).set(cen, start, end)
        self._pos = pos
    
    def items(self, index=0):
        return ('Rod{}'.format(index), self.cen, self.start, self.end, self.pos)
    def items_tags(self, index=0):
        return ('Rod{}'.format(index), ('cen', self.cen), ('start', self.start), ('end', self.end), ('pos', self.pos))
    
    def __str__(self):
        return "<Rod cen={v.cen} start={v.start} end={v.end} pos={v.pos}>".format(v=self)

class VParameter:
    def __init__(self, val=0., commit=''):
        self.set(val, commit)
    @property
    def val(self):
        return self._val
    @property
    def commit(self):
        return self._commit
    
    def set(self, val=0., commit=''):
        self._val = val
        self._commit = commit
    
    def items(self, index=0):
        return ('n{}'.format(index), self.val, self.commit)
    def items_tags(self, index=0):
        return ('n{}'.format(index), ('val', self.val), ('commit', self.commit))
    
    def __str__(self):
        return "<Parameter val={v.val} commit=\"{v.commit}\">".format(v=self)

class VPath:
    def __init__(self, point=0, points=list(), show=True):
        self.set(point, points, show)
    
    @property
    def point(self):
        return self._point
    @property
    def path(self):
        return self._path
    @property
    def show(self):
        return self._show
    @show.setter
    def show(self, show):
        self._show = show
    
    def set(self, point=0, points=list(), show=True):
        self._point = point
        self._path = list()
        self._show = show
        if points:
            for p in points:
                PointType = type(p)
                if PointType==tuple or PointType==list or p==None:
                    #(x, y)
                    self._path.append(p)
    
    def isBroken(self):
        for point in self.path:
            if point is False or point[0] is False:
                return True
        return False
    
    def __str__(self):
        return "<Path point={v.point} path={v.path}>".format(v=self)

class VPaths:
    def __init__(self, shaft=0, paths=list()):
        self.set(shaft, paths)
    @property
    def shaft(self):
        return self._shaft
    @property
    def paths(self):
        return self._paths
    
    def set(self, shaft=0, paths=list()):
        self._shaft = shaft
        self._paths = list()
        if paths:
            for path in paths:
                if type(path)==VPath:
                    self._paths.append(path)
    
    def isBroken(self):
        for path in self.paths:
            if path.isBroken():
                return True
        return False
    
    def __str__(self):
        return "<Paths shaft={v.shaft} paths={v.paths}>".format(v=self)

if __name__=='__main__':
    a = VPath(1, (None, (0, 2)))
    b = VPath(2, ((3, 5), (0, 2)))
    print(a.path)
    c = VPaths(0, (a, b))
    print(c.paths)
