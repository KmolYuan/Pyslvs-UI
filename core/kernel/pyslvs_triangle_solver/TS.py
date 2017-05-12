# -*- coding: utf-8 -*-
from math import *
import logging, traceback

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
    def Type(self): return self._type
    @Type.setter
    def Type(self, Type): self._type = Type
    
    def set(self, name, value):
        if name in self.ITEM: self.__dict__.update({name:value})
    def get(self, name, elseObject=None): return getattr(self, name) if hasattr(self, name) else elseObject
    def items(self): return {t:getattr(self, t) for t in self.ITEM if hasattr(self, t)}
    
    def __str__(self): return "<{}>".format(self.items())

class solver:
    def __init__(self, Directions=list(), *keywords): self.set(Directions)
    def set(self, Directions): self.Directions = Directions
    
    def answer(self):
        answer = self.Iterator() if self.Parser() else list()
        self.Directions.clear()
        return answer
    
    def Parser(self):
        for e in self.Directions:
            pos = self.Directions.index(e)
            if self.getCheck(e, 'p1', 'p2', 'len1', 'angle'): self.Directions[pos].Type = 'PLAP'
            elif self.getCheck(e, 'p1', 'p2', 'len1', 'len2'): self.Directions[pos].Type = 'PLLP'
            elif self.getCheck(e, 'p1', 'p2', 'len1', 'p3'): self.Directions[pos].Type = 'PLPP'
            elif self.getCheck(e, 'p1', 'p2', 'p3'): self.Directions[pos].Type = 'PPP'
            else: return False
        return bool(self.Directions)
    
    def getCheck(self, e, *args):
        for arg in args:
            if e.get(arg, False) is False: return False
        return True
    
    def Iterator(self):
        results = list()
        for e in self.Directions:
            p1 = results[e.p1] if type(e.p1)==int else e.p1
            p2 = results[e.p2] if type(e.p2)==int else e.p2
            if e.Type in ['PLPP', 'PPP']: p3 = results[e.p3] if type(e.p3)==int else e.p3
            #Direction of the point
            other = e.get('other', False)
            ##True: angle1-angle2
            ##False: angle1+angle2
            if e.Type=='PLAP': results.append(self.PLAP(p1, e.len1, e.angle, p2, other))
            elif e.Type=='PLLP': results.append(self.PLLP(p1, e.len1, e.len2, p2, other))
            elif e.Type=='PLPP': results.append(self.PLPP(p1, e.len1, p3, p2, other))
            elif e.Type=='PPP': results.append(self.PPP(p1, p2, p3))
        return results
    
    def PLAP(self, p1, line1, angle, p2, other=False):
        try:
            x1 = p1[0] #p1 start point
            y1 = p1[1]
            x2 = p2[0] #p2 start point2
            y2 = p2[1]
            len1 = float(line1)
            angle2 = radians(float(angle))
            angle1 = self.m(p1, p2)
            if other:
                cx = x1+len1*cos(angle1-angle2)
                cy = y1+len1*sin(angle1-angle2)
            else:
                cx = x1+len1*cos(angle1+angle2)
                cy = y1+len1*sin(angle1+angle2)
            return cx, cy
        except Exception as e: return self.ErrorBack(e)
    
    def PLLP(self, p1, line1, line2, p2, other=False):
        try:
            x1 = p1[0] #p1 start point
            y1 = p1[1]
            x2 = p2[0] #p2 start point2
            y2 = p2[1]
            len1 = float(line1)
            len2 = float(line2)
            d = self.diff(p1, p2)
            angle1 = self.m(p1, p2)
            angle2 = self.CosineTheoremAngle(len2, d, len1)
            if other:
                cx = x1+len1*cos(angle1-angle2)
                cy = y1+len1*sin(angle1-angle2)
            else:
                cx = x1+len1*cos(angle1+angle2)
                cy = y1+len1*sin(angle1+angle2)
            return cx, cy
        except Exception as e: return self.ErrorBack(e)
    
    def PLPP(self, p1, line1, p2, p3, other=False):
        try:
            x1 = p1[0] #p1 start point
            y1 = p1[1]
            x2 = p2[0] #p2 slider start point
            y2 = p2[1]
            x3 = p3[0] #p3 slider end point
            y3 = p3[1]
            len1 = float(line1) #len1 slider link
            if other:
                ex = ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))
                ey = (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (-y2 + y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
            else:
                ex = ((x2-x3)*(x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2)) - (x2*y3 - y2*x3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))/((y2 - y3)*(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2))
                ey = (x1*x2*y2 - x1*x2*y3 - x1*y2*x3 + x1*x3*y3 + y1*y2**2 - 2*y1*y2*y3 + y1*y3**2 + x2**2*y3 - x2*y2*x3 - x2*x3*y3 + y2*x3**2 + (y2 - y3)*sqrt(len1**2*x2**2 - 2*len1**2*x2*x3 + len1**2*y2**2 - 2*len1**2*y2*y3 + len1**2*x3**2 + len1**2*y3**2 - x1**2*y2**2 + 2*x1**2*y2*y3 - x1**2*y3**2 + 2*x1*y1*x2*y2 - 2*x1*y1*x2*y3 - 2*x1*y1*y2*x3 + 2*x1*y1*x3*y3 - 2*x1*x2*y2*y3 + 2*x1*x2*y3**2 + 2*x1*y2**2*x3 - 2*x1*y2*x3*y3 - y1**2*x2**2 + 2*y1**2*x2*x3 - y1**2*x3**2 + 2*y1*x2**2*y3 - 2*y1*x2*y2*x3 - 2*y1*x2*x3*y3 + 2*y1*y2*x3**2 - x2**2*y3**2 + 2*x2*y2*x3*y3 - y2**2*x3**2))/(x2**2 - 2*x2*x3 + y2**2 - 2*y2*y3 + x3**2 + y3**2)
            return ex, ey
        except Exception as e: return self.ErrorBack(e)
    
    def PPP(self, p1, p2, p3): return self.diff(p1, p2), self.diff(p2, p3), self.diff(p1, p3)
    
    def m(self, p1, p2):
        x = p2[0]-p1[0]
        y = p2[1]-p1[1]
        d = self.diff(p1, p2)
        angle = self.CosineTheoremAngle(y, x, d)
        return angle*(-1 if y<0 else 1)
    
    def diff(self, p1, p2): return sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    
    def CosineTheoremAngle(self, a, b, c):
        numerator = float(b**2+c**2-a**2)
        denominator = float(2*b*c)
        try: return acos(numerator/denominator)
        except ZeroDivisionError:
            if numerator>0: return radians(90.)
            else: return radians(270.)
    
    def ErrorBack(self, e):
        logging.exception("TS Exception.")
        traceback.print_tb(e.__traceback__)
        print(e)
        return False

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
