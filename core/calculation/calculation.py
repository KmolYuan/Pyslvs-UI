# -*- coding: utf-8 -*-
import numpy
from ..kernel.kernel_getter import *

def slvsProcess(Point=False, Line=False, Chain=False, Shaft=False, Slider=False, Rod=False,
        currentShaft=0, point_int=False, angle=False, hasWarning=True):
    pathTrackProcess = not(Point is False) and not angle is False
    staticProcess = not(Point is False) and angle is False
    Sys = System(len(Point)*2+9)
    p0 = Sys.add_param(0.)
    p1 = Sys.add_param(0.)
    p2 = Sys.add_param(0.)
    Point0 = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = Sys.add_param(qw)
    p4 = Sys.add_param(qx)
    p5 = Sys.add_param(qy)
    p6 = Sys.add_param(qz)
    Workplane1 = Workplane(Point0, Normal3d(p3, p4, p5, p6))
    p7 = Sys.add_param(0.)
    p8 = Sys.add_param(0.)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
    if pathTrackProcess:
        p9 = Sys.add_param(10.)
        p10 = Sys.add_param(0.)
        Point2 = Point2d(Workplane1, p9, p10)
        Constraint.dragged(Workplane1, Point2)
        Line0 = LineSegment2d(Workplane1, Point1, Point2)
    Points = [Point1]
    if pathTrackProcess or staticProcess:
        for i, e in enumerate(Point[1:]):
            x = Sys.add_param(e.x)
            if len(Shaft)>0:
                #Quadrant Fix
                if Shaft[currentShaft].ref==i+1:
                    cen = Point[Shaft[currentShaft].cen].y
                    ref = e.y
                    case1 = ref-cen>=0
                    case2 = (angle if pathTrackProcess else Shaft[currentShaft].demo)>=180
                    if case1:
                        if case2: y = cen*2-ref
                        else: y = e.y
                    else:
                        if case2: y = e.y
                        else: y = cen*2-ref
                elif Shaft[currentShaft].isParallelogram and (not e.fix) and (angle>=180 or Shaft[currentShaft].demo>=180):
                    change = False
                    for f in Line:
                        if i+1 in f and not Shaft[currentShaft].ref in f:
                            cen = Point[f.start if f.end==i+1 else f.end].y
                            ref = e.y
                            diff = ref-cen
                            for table in [Line, Chain]:
                                for k in table:
                                    if i+1 in k and Shaft[currentShaft].ref in k:
                                        change = True
                                        y = cen-diff
                            break
                    if change==False: y = e.y
                else: y = e.y
            else: y = e.y
            y = Sys.add_param(y)
            Points.append(Point2d(Workplane1, x, y))
            if e.fix: Constraint.dragged(Workplane1, Points[-1])
        for e in Chain:
            Constraint.distance(e.p1p2, Workplane1, Points[e.p1], Points[e.p2])
            Constraint.distance(e.p2p3, Workplane1, Points[e.p2], Points[e.p3])
            Constraint.distance(e.p1p3, Workplane1, Points[e.p1], Points[e.p3])
        for e in Line:
            Constraint.distance(e.len, Workplane1, Points[e.start], Points[e.end])
        for e in Slider:
            Constraint.on(Workplane1, Points[e.cen], LineSegment2d(Workplane1, Points[e.start], Points[e.end]))
        for e in Rod:
            Constraint.on(Workplane1, Points[e.cen], LineSegment2d(Workplane1, Points[e.start], Points[e.end]))
            Constraint.distance(e.pos, Workplane1, Points[e.start], Points[e.cen])
        if pathTrackProcess:
            center = Shaft[currentShaft].cen
            reference = Shaft[currentShaft].ref
            Constraint.angle(Workplane1, angle, LineSegment2d(Workplane1, Points[center], Points[reference]), Line0, False)
        elif staticProcess:
            Points.append(Point2d(Workplane1, Sys.add_param(10.), Sys.add_param(0.)))
            Constraint.dragged(Workplane1, Points[-1])
            Line0 = LineSegment2d(Workplane1, Points[0], Points[-1])
            for e in Shaft: Constraint.angle(Workplane1, e.demo, LineSegment2d(Workplane1, Points[e.cen], Points[e.ref]), Line0, True)
    Sys.solve()
    if Sys.result==SLVS_RESULT_OKAY:
        if pathTrackProcess:
            x = float(Sys.get_param((point_int+2)*2+5).val)
            y = float(Sys.get_param((point_int+2)*2+6).val)
            return x, y
        elif staticProcess:
            resultList = list()
            for i in range(0, len(Point)*2, 2): resultList.append({'x':float(Sys.get_param(i+7).val), 'y':float(Sys.get_param(i+8).val)})
            return resultList, Sys.dof
    else:
        if Sys.result==SLVS_RESULT_INCONSISTENT and hasWarning: print("SLVS_RESULT_INCONSISTENT")
        elif Sys.result==SLVS_RESULT_DIDNT_CONVERGE and hasWarning: print("SLVS_RESULT_DIDNT_CONVERGE")
        elif Sys.result==SLVS_RESULT_TOO_MANY_UNKNOWNS and hasWarning: print("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        if pathTrackProcess: return None, None
        elif staticProcess: return list(), False

def slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod):
    script = """'''This code is generate by Pyslvs'''
Sys = System(1000)
p0 = Sys.add_param(0.0)\np1 = Sys.add_param(0.0)\np2 = Sys.add_param(0.0)
Point0 = Point3d(p0, p1, p2)
qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
p3 = Sys.add_param(qw)\np4 = Sys.add_param(qx)\np5 = Sys.add_param(qy)\np6 = Sys.add_param(qz)
Normal1 = Normal3d(p3, p4, p5, p6)
Workplane1 = Workplane(Point0, Normal1)
p7 = Sys.add_param(0.0)\np8 = Sys.add_param(0.0)
Point1 = Point2d(Workplane1, p7, p8)
Constraint.dragged(Workplane1, Point1)
"""
    for i, e in enumerate(Point):
        script += "p{} = Sys.add_param({})\n".format(i*2+7, e.x)
        script += "p{} = Sys.add_param({})\n".format(i*2+8, e.y)
        script += "Point{} = Point2d(Workplane1, p{}, p{})\n".format(i+1, i*2+7, i*2+8)
        if e.fix: script += "Constraint.dragged(Workplane1, Point{})\n".format(i+1)
    for e in Chain:
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p1p2, e.p1+1, e.p2+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p2p3, e.p2+1, e.p3+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p1p3, e.p1+1, e.p3+1)
    for e in Line: script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.len, e.start+1, e.end+1)
    for e in Slider: script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e.cen+1, e.start+1, e.end+1)
    for e in Rod:
        script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e.cen+1, e.start+1, e.end+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.pos, e.start+1, e.cen+1)
    return script

def generateProcess(path, upper, lowerVal, type=0):
    p = len(path)
    upperVal = upper+[360.0]*p
    lowerVal = lowerVal+[0.0]*p
    Parm_num = p+9
    maxGen = 1500
    report = 100
    mechanismParams = {
        'Driving':'A',
        'Follower':'D',
        'Link':'L0,L1,L2,L3,L4',
        'Target':'E',
        'ExpressionName':'PLAP,PLLP,PLLP',
        'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
        'targetPath':path,
        'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'},],
        'VARS':9,
        'formula':['PLAP','PLLP'],
    }
    mechanismObj = build_planar(mechanismParams)
    if type==0:
        algorithmPrams = {
            'nParm':Parm_num,
            'nPop':250,
            'pCross':0.95,
            'pMute':0.05,
            'pWin':0.95,
            'bDelta':5.,
            'upper':upperVal,
            'lower':lowerVal,
            'maxGen':maxGen,
            'report':report,
        }
        foo = Genetic(mechanismObj, **algorithmPrams)
    elif type==1:
        algorithmPrams = {
            'D':Parm_num,
            'n':40,
            'alpha':0.01,
            'betaMin':0.2,
            'gamma':1.,
            'beta0':1.,
            'ub':upperVal,
            'lb':lowerVal,
            'maxGen':maxGen,
            'report':report,
        }
        foo = Firefly(mechanismObj, **algorithmPrams)
    elif type==2:
        algorithmPrams = {
            'strategy':1,
            'D':Parm_num,
            'NP':190,
            'F':0.6,
            'CR':0.9,
            'upper':upperVal,
            'lower':lowerVal,
            'maxGen':maxGen,
            'report':report,
        }
        foo = DiffertialEvolution(mechanismObj, **algorithmPrams)
    time_and_fitness, fitnessParameter = foo.run()
    time_and_fitness = [float(k[1]) for k in [e.split(',') for e in time_and_fitness.split(';')[0:-1]]]
    fitnessParameter = [float(e) for e in fitnessParameter.split(',')]
    print('time_and_fitness: {}'.format(time_and_fitness))
    print('fitnessParameter: {}'.format(fitnessParameter))
    return time_and_fitness, fitnessParameter
