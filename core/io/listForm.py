# -*- coding: utf-8 -*-

class PointList(list):
    def __init__(self):
        list.__init__([])
        self.append({'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0})
    def increase(self, x, y, fix):
        self.append({'x':float(x), 'y':float(y), 'fix':bool(fix)})
    def take(self, index, x=None, y=None, fix=None, cx=None, cy=None):
        try:
            table = self[index]
            if x!=None: table['x'] = float(x)
            if y!=None: table['y'] = float(y)
            if fix!=Nonee: table['fix'] = bool(fix)
            if cx!=None: table['cx'] = float(cx)
            if cy!=None: table['cy'] = float(cy)
        except IndexError: self.increase(x, y, fix)

class LineList(list):
    def __init__(self):
        list.__init__([])
    def increase(self, start, end, len):
        self.append({'start':int(start.replace('Point', '')), 'end':int(end.replace('Point', '')), 'len':float(len)})
    def take(self, index, start=None, end=None, len=None):
        try:
            table = self[index]
            if start!=None: table['start'] = int(start.replace('Point', ''))
            if end!=None: table['end'] = int(end.replace('Point', ''))
            if len!=None: table['len'] = float(len)
        except IndexError: self.increase(start, end, len)

class ChainList(list):
    def __init__(self):
        list.__init__([])
    def increase(self, p1, p2, p3, p1p2, p2p3, p1p3):
        self.append({
            'p1':int(p1.replace('Point', '')), 'p2':int(p2.replace('Point', '')), 'p3':int(p3.replace('Point', '')),
            'p1p2':float(p1p2), 'p2p3':float(p1p2), 'p1p3':float(p1p3)})
    def take(self, index, p1=None, p2=None, p3=None, p1p2=None, p2p3=None, p1p3=None):
        try:
            table = self[index]
            if p1!=None: table['p1'] = int(p1.replace('Point', ''))
            if p2!=None: table['p2'] = int(p2.replace('Point', ''))
            if p2!=None: table['p3'] = int(p3.replace('Point', ''))
            if p1p2!=None: table['p1p2'] = float(p1p2)
            if p2p3!=None: table['p2p3'] = float(p2p3)
            if p1p3!=None: table['p1p3'] = float(p1p3)
        except IndexError: self.increase(p1, p2, p3, p1p2, p2p3, p1p3)

class ShaftList(list):
    def __init__(self):
        list.__init__([])
    def increase(self, cen, ref, start, end, demo, isParallelogram):
        self.append({
            'cen':int(cen.replace('Point', '')), 'ref':int(ref.replace('Point', '')),
            'start':float(start), 'end':float(end), 'demo':float(demo), 'isParallelogram':bool(isParallelogram)})
    def take(self, index, cen=None, ref=None, start=None, end=None, demo=None, isParallelogram=None):
        try:
            table = self[index]
            if cen!=None: table['cen'] = int(cen.replace('Point', ''))
            if ref!=None: table['ref'] = int(ref.replace('Point', ''))
            if start!=None: table['start'] = float(start)
            if end!=None: table['end'] = float(end)
            if demo!=None: table['demo'] = float(demo)
            if isParallelogram!=None: table['isParallelogram'] = bool(isParallelogram)
        except IndexError: self.increase(cen, ref, start, end, demo, isParallelogram)

class SliderList(list):
    def __init__(self):
        list.__init__([])
    def increase(self, cen, start, end):
        self.append({'cen':int(cen), 'start':int(start), 'end':int(end)})
    def take(self, index, cen=None, start=None, end=None):
        try:
            table = self[index]
            if cen!=None: table['cen'] = int(cen.replace('Point', ''))
            if start!=None: table['start'] = int(start.replace('Point', ''))
            if end!=None: table['end'] = int(end.replace('Point', ''))
        except IndexError: self.increase(cen, start, end)

class RodList(list):
    def __init__(self):
        list.__init__([])
    def increase(self, cen, start, end, pos):
        self.append({'cen':int(cen), 'start':int(start), 'end':int(end), 'pos':float(pos)})
    def take(self, index, cen=None, start=None, end=None, pos=None):
        try:
            table = self[index]
            if cen!=None: table['cen'] = int(cen.replace('Point', ''))
            if start!=None: table['start'] = int(start.replace('Point', ''))
            if end!=None: table['end'] = int(end.replace('Point', ''))
            if pos!=None: table['pos'] = float(pos)
        except IndexError: self.increase(cen, start, end, pos)
