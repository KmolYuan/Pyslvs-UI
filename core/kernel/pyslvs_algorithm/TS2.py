from sympy import pi, sqrt, cos, sin, acos, atan2, diff, lambdify
from sympy.abc import w, t

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, p):
        '''
        Coordinate p
        '''
        return sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
    
    def m(self, p):
        '''
        Coordinate p
        '''
        return atan2(p.y-self.y, p.x-self.x)
    
    @property
    def functions(self):
        return (
            lambdify((t, w), self.x),
            lambdify((t, w), self.y))

class FunctionBase:
    '''
    Input Coordinate should get from position function.
    '''
    @property
    def p(self):
        return Coordinate(self.pxFunc, self.pyFunc)
    
    @property
    def v(self):
        return Coordinate(diff(self.pxFunc, t), diff(self.pyFunc, t))
    
    @property
    def a(self):
        return Coordinate(diff(self.pxFunc, t, 2), diff(self.pyFunc, t, 2))
    
    @property
    def j(self):
        return Coordinate(diff(self.pxFunc, t, 3), diff(self.pyFunc, t, 3))

class pl(FunctionBase):
    def __init__(self, A, L):
        self.pxFunc = A.x+L*cos(w*t)
        self.pyFunc = A.y+L*sin(w*t)

class pllp(FunctionBase):
    def __init__(self, A, L, R, B, reverse=False):
        
        alpha = A.m(B)
        base = A.distance(B)
        beta = acos((L**2 + base**2 - R**2)/(2*L*base))
        if reverse:
            self.pxFunc = A.x+L*cos(alpha-beta)
            self.pyFunc = A.y+L*sin(alpha-beta)
        else:
            self.pxFunc = A.x+L*cos(alpha+beta)
            self.pyFunc = A.y+L*sin(alpha+beta)

def solver(mechanism, progress=False, progressFunc=None, stopedFunc=None):
    results = []
    resultCount = len(mechanism)
    for i, e in enumerate(mechanism):
        if stopedFunc is not None:
            if stopedFunc():
               return
        if len(e)==2:
            foo = pl(*e)
            results.append(foo)
        else:
            e = list(e)
            if type(e[0])==int:
                e[0] = results[e[0]].p
            if type(e[3])==int:
                e[3] = results[e[3]].p
            foo = pllp(*e)
            results.append(foo)
        if progress:
            print("{} / {}".format(i+1, resultCount))
        if progressFunc is not None:
            progressFunc(i+1)
    return results

if __name__=='__main__':
    W = pi/180 #rad/s
    from time import time
    t0 = time()
    '''
    p0 = Coordinate(0, 0)
    p1 = Coordinate(-38, -7.8)
    results = solver([
        (p0, 15.), #p2
        (p1, 41.5, 50., 0), #p3
        (p1, 40.1, 55.8, 1), #p4
        (0, 61.9, 39.3, 1), #p5
        (3, 36.7, 39.4, 2), #p6
        (3, 49., 65.7, 4), #p7
    ], progress=True)
    '''
    p0 = Coordinate(-20.77, -26.65)
    p1 = Coordinate(44.94, -36.83)
    results = solver([
        (p0, 8.76), #p2
        (0, 41.16, 50., p1), #p3
        (1, 50., 50., p0), #p4
    ], progress=True)
    
    print("time: {}".format(time()-t0))
    '''
    index: results[i]
    method: position (p) / velocity (v) / acceleration (a) / jerk (j)
    '''
    xfun, yfun = results[2].p.functions
    plot = []
    for T in range(0, 360+1, 5):
        print("{}\t{}".format(float(xfun(T, W)), float(yfun(T, W))))
        x = xfun(T, W)
        y = yfun(T, W)
        plot.append((x, y, sqrt(x**2+y**2)))
    #Pyplot
    #import matplotlib.pyplot as plt
    #plt.plot(plot)
    #plt.show()
