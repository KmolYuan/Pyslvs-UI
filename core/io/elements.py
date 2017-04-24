# -*- coding: utf-8 -*-

class VPoint:
    def __init__(self, x=0., y=0., fix=False):
        self.set(x, y, fix)
        self._cx = self._x
        self._cy = self._y
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
    @property
    def fix(self): return self._fix
    @property
    def cx(self): return self._cx
    @property
    def cy(self): return self._cy
    
    def set(self, x=0., y=0., fix=False):
        self._x = x
        self._y = y
        self._fix = fix
    
    def move(self, x=0., y=0.):
        self._cx = x
        self._cy = y
    
    def reset(self):
        self._x = self._cx
        self._y = self._cy
    
    def __str__(self): return "<Point x={v.x} y={v.y} fix={v.fix} cx={v.cx} cy={v.cy}>".format(v=self)

class VLine:
    def __init__(self, start=0, end=0, len=0.): self.set(start, end, len)
    @property
    def start(self): return self._start
    @property
    def end(self): return self._end
    @property
    def len(self): return self._len
    
    def set(self, start=VPoint(), end=VPoint(), len=0.):
        self._start = start
        self._end = end
        self._len = len
    
    def __str__(self): return "<Line start={v.start} end={v.end} len={v.len}>".format(v=self)

class VChain:
    def __init__(self, p1=VPoint(), p2=0, p3=0, p1p2=0., p2p3=0., p1p3=0.): self.set(p1, p2, p3, p1p2, p2p3, p1p3)
    @property
    def p1(self): return self._p1
    @property
    def p2(self): return self._p2
    @property
    def p3(self): return self._p3
    @property
    def p1p2(self): return self._p1p2
    @property
    def p2p3(self): return self._p2p3
    @property
    def p1p3(self): return self._p1p3
    
    def set(self, p1=0, p2=0, p3=0, p1p2=0., p2p3=0., p1p3=0.):
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3
        self._p1p2 = p1p2
        self._p2p3 = p2p3
        self._p1p3 = p1p3
    
    def __str__(self):
        return "<Chain p1={v.p1} p2={v.p2} p3={v.p3} p1p2={v.p1p2} p2p3={v.p2p3} p1p3={v.p1p3}>".format(v=self)

class VShaft:
    def __init__(self, cen=0, ref=0, start=0., end=360., demo=0., isParallelogram=False): self.set(cen, ref, start, end, demo, isParallelogram)
    @property
    def cen(self): return self._cen
    @property
    def ref(self): return self._ref
    @property
    def start(self): return self._start
    @property
    def end(self): return self._end
    @property
    def demo(self): return self._demo
    @property
    def isParallelogram(self): return self._isParallelogram
    
    def set(self, cen=0, ref=0, start=0., end=360., demo=0., isParallelogram=False):
        self._cen = cen
        self._ref = ref
        self._start = start
        self._end = end
        self._demo = demo
        self._isParallelogram = isParallelogram
    
    def drive(self, demo):
        if demo>self._start and demo<self._end: self._demo = demo
    
    def __str__(self):
        return "<Shaft cen={v.cen} ref={v.ref} start={v.start}, end={v.end} demo={v.demo} isParallelogram={v.isParallelogram}>".format(v=self)

class VSlider:
    def __init___(self, cen=0, start=0, end=0): self.set(cen, start, end)
    @property
    def cen(self): return self._cen
    @property
    def start(self): return self._start
    @property
    def end(self): return self._end
    
    def set(self, cen=0, start=0, end=0):
        self._cen = cen
        self._start = start
        self._end = end
    
    def __str__(self):
        return "<Slider cen={v.cen} start={v.start} end={v.end}>".format(v=self)

class VRod(VSlider):
    def __init__(self, cen=0, start=0, end=0, pos=0.): self.set(cen, start, end, pos)
    @property
    def pos(self): return self._pos
    
    def set(self, cen=0, start=0, end=0, pos=0.):
        super(VRod, self).set(cen, start, end)
        self._pos = pos
    
    def __str__(self):
        return "<Rod cen={v.cen} start={v.start} end={v.end} pos={v.pos}>".format(v=self)

if __name__=='__main__':
    a = VPoint(10., 20., True)
    a.move(40., 30.)
    b = VPoint()
    l = VLine(b, a, 30)
    print(l)
    print(l.end)
