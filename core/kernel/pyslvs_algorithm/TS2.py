from sympy import pi, sqrt, cos, sin, acos, asin, diff, lambdify
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
        return asin((p.y - self.y)/self.distance(p))
    
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

def solver(mechanism, progress=False):
    results = []
    resultCount = len(mechanism)
    for i, e in enumerate(mechanism):
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
        (p1, 41.5, 50., 0, True), #p3
        (p1, 40.1, 55.8, 1, True), #p4
        (p1, 39.3, 61.9, 0, True), #p5
        (2, 39.4, 36.7, 3, True), #p6
        #(3, 49., 65.7, 4), #p7
    ], progress=True)
    '''
    p0 = Coordinate(0, 0)
    p1 = Coordinate(90, 0)
    results = solver([
        (p0, 35.), #p2
        (0, 70., 70., p1), #p3
        (0, 40., 40., 1), #p4
    ], progress=True)
    
    print("time: {}".format(time()-t0))
    '''
    index: results[i]
    method: position (p) / velocity (v) / acceleration (a) / jerk (j)
    '''
    xfun, yfun = results[2].p.functions
    plot = []
    for T in range(0, 360+1, 5):
        print("{}\t{}".format(xfun(T, W), yfun(T, W)))
        plot.append((xfun(T, W), yfun(T, W)))
    #Pyplot
    import matplotlib.pyplot as plt
    plt.plot(plot)
    plt.show()
