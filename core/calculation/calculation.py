# -*- coding: utf-8 -*-
#System infomation
import sys, platform, numpy
py_nm = sys.version[0:sys.version.find(" ")][0:3]

#SLVS Version & pyslvs_generate Version
if platform.system().lower()=="linux":
    if py_nm=="3.4":
        from ..kernel.py34.slvs import *
        from ..kernel.pyslvs_generate.py34 import tinycadlib
        from ..kernel.pyslvs_generate.py34.planarlinkage import build_planar
        from ..kernel.pyslvs_generate.py34.rga import Genetic
        from ..kernel.pyslvs_generate.py34.firefly import Firefly
        from ..kernel.pyslvs_generate.py34.de import DiffertialEvolution
    elif py_nm=="3.5":
        from ..kernel.py35.slvs import *
        from ..kernel.pyslvs_generate.py35 import tinycadlib
        from ..kernel.pyslvs_generate.py35.planarlinkage import build_planar
        from ..kernel.pyslvs_generate.py35.rga import Genetic
        from ..kernel.pyslvs_generate.py35.firefly import Firefly
        from ..kernel.pyslvs_generate.py35.de import DiffertialEvolution
elif platform.system().lower()=="windows":
    if py_nm=="3.5":
        from ..kernel.py35w.slvs import *
        from ..kernel.pyslvs_generate.py35w import tinycadlib
        from ..kernel.pyslvs_generate.py35w.planarlinkage import build_planar
        from ..kernel.pyslvs_generate.py35w.rga import Genetic
        from ..kernel.pyslvs_generate.py35w.firefly import Firefly
        from ..kernel.pyslvs_generate.py35w.de import DiffertialEvolution

def slvsProcess(Point=False, Line=False, Chain=False, Shaft=False, Slider=False, Rod=False,
        currentShaft=0, point_int=False, angle=False, hasWarning=True):
    pathTrackProcess = not(Point is False) and not angle is False
    staticProcess = not(Point is False) and angle is False
    sys = System(1000)
    p0 = sys.add_param(0.)
    p1 = sys.add_param(0.)
    p2 = sys.add_param(0.)
    Point0 = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Workplane1 = Workplane(Point0, Normal3d(p3, p4, p5, p6))
    p7 = sys.add_param(0.)
    p8 = sys.add_param(0.)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
    if pathTrackProcess:
        p9 = sys.add_param(10.)
        p10 = sys.add_param(0.)
        Point2 = Point2d(Workplane1, p9, p10)
        Constraint.dragged(Workplane1, Point2)
        Line0 = LineSegment2d(Workplane1, Point1, Point2)
    Points = [Point1]
    if pathTrackProcess or staticProcess:
        for e in Point[1:]:
            x = sys.add_param(e['x'])
            if len(Shaft)>0:
                #Quadrant Fix
                if Shaft[currentShaft]['ref']==Point.index(e):
                    cen = Point[Shaft[currentShaft]['cen']]['y']
                    ref = e['y']
                    diff = ref-cen
                    case1 = diff>=0
                    case2 = angle>=180 if pathTrackProcess else Shaft[currentShaft]['demo']>=180
                    if case1 and not case2: y = sys.add_param(ref)
                    elif case1 and case2: y = sys.add_param(cen-diff)
                    elif not case1 and not case2: y = sys.add_param(cen-diff)
                    elif not case1 and case2: y = sys.add_param(ref)
                elif not e['fix'] and (angle>=180 or Shaft[currentShaft]['demo']>=180) and Shaft[currentShaft]['isParallelogram']:
                    change = False
                    for f in Line:
                        if Point.index(e) in f.values() and not Shaft[currentShaft]['ref'] in f.values():
                            cen = Point[f['start'] if f['end']==Point.index(e) else f['end']]['y']
                            ref = e['y']
                            diff = ref-cen
                            for t in [Line, Chain]:
                                for k in t:
                                    if Point.index(e) in k.values() and Shaft[currentShaft]['ref'] in k.values():
                                        change = True
                                        y = sys.add_param(cen-diff)
                            break
                    if change==False: y = sys.add_param(e['y'])
                else: y = sys.add_param(e['y'])
            else: y = sys.add_param(e['y'])
            Points.append(Point2d(Workplane1, x, y))
            if e['fix']: Constraint.dragged(Workplane1, Points[-1])
        for e in Chain:
            pa = e['p1']
            pb = e['p2']
            pc = e['p3']
            Constraint.distance(e['p1p2'], Workplane1, Points[pa], Points[pb])
            Constraint.distance(e['p2p3'], Workplane1, Points[pb], Points[pc])
            Constraint.distance(e['p1p3'], Workplane1, Points[pa], Points[pc])
        for e in Line:
            Constraint.distance(e['len'], Workplane1, Points[e['start']], Points[e['end']])
        for e in Slider:
            Constraint.on(Workplane1, Points[e['cen']], LineSegment2d(Workplane1, Points[e['start']], Points[e['end']]))
        for e in Rod:
            Constraint.on(Workplane1, Points[e['cen']], LineSegment2d(Workplane1, Points[e['start']], Points[e['end']]))
            Constraint.distance(e['pos'], Workplane1, Points[e['start']], Points[e['cen']])
        if pathTrackProcess:
            center = Shaft[currentShaft]['cen']
            reference = Shaft[currentShaft]['ref']
            Constraint.angle(Workplane1, angle, LineSegment2d(Workplane1, Points[center], Points[reference]), Line0, False)
        elif staticProcess:
            Points.append(Point2d(Workplane1, sys.add_param(10.), sys.add_param(0.)))
            Constraint.dragged(Workplane1, Points[-1])
            Line0 = LineSegment2d(Workplane1, Points[0], Points[-1])
            for e in Shaft:
                #shaft demo switch
                center = e['cen']
                reference = e['ref']
                line = LineSegment2d(Workplane1, Points[center], Points[reference])
                try:
                    angle0 = e['demo']
                    Constraint.angle(Workplane1, angle0, line, Line0, False)
                except: pass
    sys.solve()
    if sys.result==SLVS_RESULT_OKAY:
        if pathTrackProcess:
            x = float(sys.get_param((point_int+2)*2+5).val)
            y = float(sys.get_param((point_int+2)*2+6).val)
        elif staticProcess:
            resultList = list()
            for i in range(0, len(Point)*2, 2): resultList.append({'x':sys.get_param(i+7).val, 'y':sys.get_param(i+8).val})
    elif sys.result==SLVS_RESULT_INCONSISTENT and hasWarning: print("SLVS_RESULT_INCONSISTENT")
    elif sys.result==SLVS_RESULT_DIDNT_CONVERGE and hasWarning: print("SLVS_RESULT_DIDNT_CONVERGE")
    elif sys.result==SLVS_RESULT_TOO_MANY_UNKNOWNS and hasWarning: print("SLVS_RESULT_TOO_MANY_UNKNOWNS")
    if pathTrackProcess:
        try: return x, y
        except: return 0, 0
    elif staticProcess:
        try: return resultList, sys.dof
        except: return list(), False

def slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod):
    script = """'''This code is generate by Pyslvs'''
sys = System(1000)
p0 = sys.add_param(0.0)\np1 = sys.add_param(0.0)\np2 = sys.add_param(0.0)
Point0 = Point3d(p0, p1, p2)
qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
p3 = sys.add_param(qw)\np4 = sys.add_param(qx)\np5 = sys.add_param(qy)\np6 = sys.add_param(qz)
Normal1 = Normal3d(p3, p4, p5, p6)
Workplane1 = Workplane(Point0, Normal1)
p7 = sys.add_param(0.0)\np8 = sys.add_param(0.0)
Point1 = Point2d(Workplane1, p7, p8)
Constraint.dragged(Workplane1, Point1)
"""
    for e in Point:
        i = Point.index(e)
        script += "p{} = sys.add_param({})\n".format(i*2+7, e['x'])
        script += "p{} = sys.add_param({})\n".format(i*2+8, e['y'])
        script += "Point{} = Point2d(Workplane1, p{}, p{})\n".format(i+1, i*2+7, i*2+8)
        if e['fix']: script += "Constraint.dragged(Workplane1, Point{})\n".format(i+1)
    for e in Chain:
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e['p1p2'], e['p1']+1, e['p2']+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e['p2p3'], e['p2']+1, e['p3']+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e['p1p3'], e['p1']+1, e['p3']+1)
    for e in Line: script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e['len'], e['start']+1, e['end']+1)
    for e in Slider: script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e['cen']+1, e['start']+1, e['end']+1)
    for e in Rod:
        script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e['cen']+1, e['start']+1, e['end']+1)
        script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e['pos'], e['start']+1, e['cen']+1)
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
            'bDelta':5.0,
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
            'gamma':1.0,
            'beta0':1.0,
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
