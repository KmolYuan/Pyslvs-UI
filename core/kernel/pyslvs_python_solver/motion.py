# -*- coding: utf-8 -*-

class vector:
    def __init__(self, p1=(0., 0.), p2=(0., 0.)):
        if type(p1)==tuple and type(p2)==tuple:
            self.x = p2[0]-p1[0]
            self.y = p2[1]-p1[1]
        elif ((type(p1)==float and type(p2)==float) or
                (type(p1)==int and type(p2)==int)):
            self.x = p1
            self.y = p2
    
    def distance(self):
        return ((self.x**2)+(self.y**2))**(1/2)
    
    def __add__(self, v):
        if type(v)==vector:
            return vector(self.x+v.x, self.y+v.y)
        else:
            raise TypeError
    
    def __sub__(self, v):
        if type(v)==vector:
            return vector(self.x-v.x, self.y-v.y)
        else:
            raise TypeError
    
    def __mul__(self, v):
        if type(v)==float or type(v)==int:
            return vector(self.x*v, self.y*v)
        else:
            raise TypeError

def velocity(Ra, Rb, omega):
    if type(Ra)==vector and type(Rb)==vector and (type(omega)==float or type(omega)==int):
        return Ra + Rb + Rb*omega
    else:
        raise TypeError

a = vector(10, 10)
b = vector(20, 20)
c = velocity(a, b, 10)

print(c.distance())
