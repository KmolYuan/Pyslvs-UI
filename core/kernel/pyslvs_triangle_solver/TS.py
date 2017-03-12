# -*- coding: utf-8 -*-
from math import *

##Directions:
##[{'p1':Point1, 'p2':Point2, 'len1':Line1, ('len2':Line2, 'angle':angle)}, ...]

class solver():
    def __init__(self, Directions):
        #Cosine Theorem
        self.CosineTheoremAngle = lambda a, b, c: acos((b**2+c**2-a**2)/(2*b*c))
        self.CosineTheoremSide = lambda alpha, b, c: b**2+c**2-2*b*c*cos(alpha)
        self.Directions = Directions
        if self.Parser(): self.results = self.Iterator()
        else: self.results = None
    
    def Parser(self):
        for e in self.Directions:
            pos = self.Directions.index(e)
            if e.get('p1', False) is False: return False
            if e.get('p2', False) is False: return False
            if e.get('len1', False) is False: return False
            if e.get('len2', False) is False and e.get('angle', False) is False: return False
            if e.get('len2', False) is False: self.Directions[pos]['Type'] = 'PLAP'
            elif e.get('angle', False) is False: self.Directions[pos]['Type'] = 'PLLP'
        return True
    
    def Iterator(self):
        results = list()
        for e in self.Directions:
            p1 = results[e['p1']] if type(e['p1'])==int else e['p1']
            p2 = results[e['p2']] if type(e['p2'])==int else e['p2']
            if e['Type']=='PLAP': results.append(self.PLAP(p1, e['len1'], e['angle'], p2))
            elif e['Type']=='PLLP': results.append(self.PLLP(p1, e['len1'], e['len2'], p2))
        return results
    
    def PLAP(self, p1, line1, angle, p2):
        x1 = tuple(p1)[0]
        y1 = tuple(p1)[1]
        len1 = float(line1)
        angle2 = radians(float(angle))
        angle1 = self.m(p1, p2)
        return x1+len1*cos(angle1+angle2), y1+len1*sin(angle1+angle2)
    
    def PLLP(self, p1, line1, line2, p2):
        x1 = tuple(p1)[0]
        y1 = tuple(p1)[1]
        len1 = float(line1)
        len2 = float(line2)
        angle1 = self.m(p1, p2)
        angle2 = self.CosineTheoremAngle(len2, diffAB, len1)
        return x1+len1*cos(angle1+angle2), y1+len1*sin(angle1+angle2)
    
    def m(self, p1, p2):
        #Get info
        x1 = tuple(p1)[0]
        y1 = tuple(p1)[1]
        x2 = tuple(p2)[0]
        y2 = tuple(p2)[1]
        #Solve
        diffABx = x1-x2
        diffABy = y1-y2
        diffAB = sqrt(diffABx**2+diffABy**2)
        return self.CosineTheoremAngle(diffABy, diffABx, diffAB)
