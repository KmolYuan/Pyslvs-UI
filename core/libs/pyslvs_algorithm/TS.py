# -*- coding: utf-8 -*-
from math import sqrt, radians
from .tinycadlib import (
    Coordinate,
    PLAP,
    PLLP,
    PLPP
)

##Directions:
##[Direction('p1':Point1, 'p2':Point2, 'len1':Line1, ('len2':Line2, 'angle':angle ...)), ...]

class Direction:
    ITEM = ['Type', 'merge', 'p1', 'p2', 'p3', 'len1', 'len2', 'angle', 'other']
    def __init__(self, **Args):
        if not Args.get('Type', False) is False:
            self._type = Args['Type']
            del Args['Type']
        self.__dict__.update(Args)
    @property
    def Type(self):
        return self._type
    @Type.setter
    def Type(self, Type):
        self._type = Type
    
    def set(self, name, value):
        if name in self.ITEM:
            self.__dict__.update({name:value})
    def get(self, name, elseObject=None):
        return getattr(self, name) if hasattr(self, name) else elseObject
    def items(self):
        return {t:getattr(self, t) for t in self.ITEM if hasattr(self, t)}
    
    def __str__(self):
        return "<{}>".format(self.items())

class solver:
    
    def __init__(self, Directions=[], showError=True, *keywords):
        self.showError = showError
        self.set(Directions)
    def set(self, Directions):
        self.Directions = Directions
    
    def answer(self):
        answer = self.Iterator() if self.Parser() else []
        self.Directions.clear()
        return answer
    
    def Parser(self):
        for e in self.Directions:
            pos = self.Directions.index(e)
            if self.getCheck(e, 'p1', 'p2', 'len1', 'angle'):
                self.Directions[pos].Type = 'PLAP'
            elif self.getCheck(e, 'p1', 'p2', 'len1', 'len2'):
                self.Directions[pos].Type = 'PLLP'
            elif self.getCheck(e, 'p1', 'p2', 'len1', 'p3'):
                self.Directions[pos].Type = 'PLPP'
            elif self.getCheck(e, 'p1', 'p2', 'p3'):
                self.Directions[pos].Type = 'PPP'
            else:
                return False
        return bool(self.Directions)
    
    def getCheck(self, e, *args):
        for arg in args:
            if e.get(arg, False) is False:
                return False
        return True
    
    def Iterator(self):
        results = []
        for d in self.Directions:
            p1 = results[d.p1] if type(d.p1)==int else d.p1
            p2 = results[d.p2] if type(d.p2)==int else d.p2
            if d.Type in ['PLPP', 'PPP']:
                p3 = results[d.p3] if type(d.p3)==int else d.p3
            #Direction of the point
            other = d.get('other', False)
            ##True: angle1-angle2
            ##False: angle1+angle2
            if d.Type=='PLAP':
                results.append(PLAP(Coordinate(*p1), d.len1, radians(d.angle), Coordinate(*p2), other))
            elif d.Type=='PLLP':
                results.append(PLLP(Coordinate(*p1), d.len1, d.len2, Coordinate(*p2), other))
            elif d.Type=='PLPP':
                results.append(PLPP(Coordinate(*p1), d.len1, p3, Coordinate(*p2), other))
            elif d.Type=='PPP':
                results.append(self.PPP(p1, p2, p3))
        return results
    
    def PPP(self, p1, p2, p3):
        return self.diff(p1, p2), self.diff(p2, p3), self.diff(p1, p3)
    
    def diff(self, p1, p2):
        return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

if __name__=='__main__':
    #Test
    print(Direction(p1=(-60, 0), p2=(0, 0), len1=30, angle=50))
    s1 = solver([
        Direction(p1=(-60, 0), p2=(0, 0), len1=30, angle=50), #C PLAP
        Direction(p1=0, p2=(0, 0), len1=50, len2=60), #D PLLP
        Direction(p1=0, p2=1, len1=50, len2=50), #E PLLP
        Direction(p1=(-45, 0), p2=(0, 12), len1=30, angle=55), # PLAP
        Direction(p1=3, len1=40, p2=(0, 12), p3=(10, 30)), #Slider E PLPP
        ])
    answer = s1.answer()
    print("C={}\nD={}\nE={}\n\nSlider B={}\nSlider E={}".format(*answer))
    s2 = solver([
        Direction(p1=(0, 0), p2=(0, 10), len1=30, angle=0)
        ])
    print(s2.answer())
    
    ##C= (-40.716371709403816, 22.98133329356934)
    ##D= (-6.698073034033397, 59.62495968661744)
    ##E= (-55.44153371488418, 70.76385733649067)
    
    ##Silder B=(-34.705658808271956, 28.17847652780915)
    ##Silder E=(4.452256484254149, 20.01406167165747)
