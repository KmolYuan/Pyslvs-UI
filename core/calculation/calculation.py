# -*- coding: utf-8 -*-
#System infomation
import sys, platform, numpy
py_nm = sys.version[0:sys.version.find(" ")][0:3]
argv = sys.argv
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

def slvsProcess(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter, currentShaft, point_int=None, angle=None):
    pathTrackProcess = not angle==None
    staticProcess = angle==None
    sys = System(1000)
    p0 = sys.add_param(0.0)
    p1 = sys.add_param(0.0)
    p2 = sys.add_param(0.0)
    Point0 = Point3d(p0, p1, p2)
    qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
    p3 = sys.add_param(qw)
    p4 = sys.add_param(qx)
    p5 = sys.add_param(qy)
    p6 = sys.add_param(qz)
    Normal1 = Normal3d(p3, p4, p5, p6)
    Workplane1 = Workplane(Point0, Normal1)
    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
    if pathTrackProcess:
        p9 = sys.add_param(10)
        p10 = sys.add_param(0.0)
        Point2 = Point2d(Workplane1, p9, p10)
        Constraint.dragged(Workplane1, Point2)
        Line0 = LineSegment2d(Workplane1, Point1, Point2)
    elif staticProcess:
        script = "'''This code is generate by Pyslvs'''\n"
        script += "sys = System(1000)\n"
        script += "p0 = sys.add_param(0.0)\np1 = sys.add_param(0.0)\np2 = sys.add_param(0.0)\n"
        script += "Point0 = Point3d(p0, p1, p2)\n"
        script += "qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)\n"
        script += "p3 = sys.add_param(qw)\np4 = sys.add_param(qx)\np5 = sys.add_param(qy)\np6 = sys.add_param(qz)\n"
        script += "Normal1 = Normal3d(p3, p4, p5, p6)\n"
        script += "Workplane1 = Workplane(Point0, Normal1)\n"
        script += "p7 = sys.add_param(0.0)\np8 = sys.add_param(0.0)\n"
        script += "Point1 = Point2d(Workplane1, p7, p8)\n"
        script += "Constraint.dragged(Workplane1, Point1)\n"
    Point = [Point1]
    #Load tables to constraint
    for i in range(1, len(table_point) if len(table_point)>=1 else 1):
        x = sys.add_param(table_point[i]['x'])
        if len(table_shaft)>0:
            #Quadrant Fix
            if table_shaft[currentShaft]['ref']==i:
                cen = table_point[table_shaft[currentShaft]['cen']]['y']
                ref = table_point[i]['y']
                diff = ref-cen
                case1 = diff>=0
                case2 = angle>=180 if pathTrackProcess else table_shaft[currentShaft]['demo']>=180
                if case1 and not case2: y = sys.add_param(ref)
                elif case1 and case2: y = sys.add_param(cen-diff)
                elif not case1 and not case2: y = sys.add_param(cen-diff)
                elif not case1 and case2: y = sys.add_param(ref)
            else: y = sys.add_param(table_point[i]['y'])
        else: y = sys.add_param(table_point[i]['y'])
        p = Point2d(Workplane1, x, y)
        Point += [p]
        if staticProcess:
            script += "p{} = sys.add_param({})\n".format(i*2+7, table_point[i]['x'])
            script += "p{} = sys.add_param({})\n".format(i*2+8, table_point[i]['y'])
            script += "Point{} = Point2d(Workplane1, p{}, p{})\n".format(i+1, i*2+7, i*2+8)
        if table_point[i]['fix']:
            Constraint.dragged(Workplane1, p)
            if staticProcess: script += "Constraint.dragged(Workplane1, Point{})\n".format(i+1)
    for i in range(len(table_chain)):
        pa = table_chain[i]['p1']
        pb = table_chain[i]['p2']
        pc = table_chain[i]['p3']
        lengab = table_chain[i]['p1p2']
        lengbc = table_chain[i]['p2p3']
        lengac = table_chain[i]['p1p3']
        Constraint.distance(lengab, Workplane1, Point[pa], Point[pb])
        Constraint.distance(lengbc, Workplane1, Point[pb], Point[pc])
        Constraint.distance(lengac, Workplane1, Point[pa], Point[pc])
        if staticProcess:
            script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(lengab, pa+1, pb+1)
            script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(lengbc, pb+1, pc+1)
            script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(lengac, pa+1, pc+1)
    for i in range(len(table_line)):
        start = table_line[i]['start']
        end = table_line[i]['end']
        leng = table_line[i]['len']
        Constraint.distance(leng, Workplane1, Point[start], Point[end])
        if staticProcess: script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(leng, start+1, end+1)
    for i in range(len(table_slider)):
        pt = table_slider[i]['cen']
        start = table_line[table_slider[i]['ref']]['start']
        end = table_line[table_slider[i]['ref']]['end']
        line = LineSegment2d(Workplane1, Point[start], Point[end])
        Constraint.on(Workplane1, Point[pt], line)
        if staticProcess: script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(pt+1, start+1, end+1)
    for i in range(len(table_rod)):
        pt = table_rod[i]['cen']
        start = table_rod[i]['start']
        end = table_rod[i]['end']
        leng = table_rod[i]['pos']
        line = LineSegment2d(Workplane1, Point[start], Point[end])
        Constraint.on(Workplane1, Point[pt], line)
        Constraint.distance(leng, Workplane1, Point[start], Point[pt])
        if staticProcess:
            script += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(pt+1, start+1, end+1)
            script += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(leng, start+1, pt+1)
    if pathTrackProcess:
        center = table_shaft[currentShaft]['cen']
        reference = table_shaft[currentShaft]['ref']
        line = LineSegment2d(Workplane1, Point[center], Point[reference])
        Constraint.angle(Workplane1, angle, line, Line0, False)
    elif staticProcess:
        if len(table_shaft) >= 1:
            pN = sys.add_param(10)
            pNN = sys.add_param(0.0)
            PointN = Point2d(Workplane1, pN, pNN)
            Point += [PointN]
            Constraint.dragged(Workplane1, Point[-1])
            Line0 = LineSegment2d(Workplane1, Point[currentShaft], Point[-1])
            #shaft demo switch
            center = table_shaft[currentShaft]['cen']
            reference = table_shaft[currentShaft]['ref']
            line = LineSegment2d(Workplane1, Point[center], Point[reference])
            try:
                angle0 = table_shaft[currentShaft]['demo']
                Constraint.angle(Workplane1, angle0, line, Line0, False)
            except: pass
    sys.solve()
    resultList = list()
    if sys.result==SLVS_RESULT_OKAY:
        if pathTrackProcess:
            x = sys.get_param((point_int+2)*2+5).val
            y = sys.get_param((point_int+2)*2+6).val
        elif staticProcess:
            for i in range(0, len(table_point)*2, 2): resultList += [{'x':sys.get_param(i+7).val, 'y':sys.get_param(i+8).val}]
    elif sys.result==SLVS_RESULT_INCONSISTENT and "-w" in argv: print ("SLVS_RESULT_INCONSISTENT")
    elif sys.result==SLVS_RESULT_DIDNT_CONVERGE and "-w" in argv: print ("SLVS_RESULT_DIDNT_CONVERGE")
    elif sys.result==SLVS_RESULT_TOO_MANY_UNKNOWNS and "-w" in argv: print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
    if pathTrackProcess:
        try: return x, y
        except: return 0, 0
    elif staticProcess: return resultList, sys.dof, script

def pathSolvingProcess(path, Limits, type=0):
    p = len(path)
    upperVal = Limits[0]+[360.0]*p
    lowerVal = Limits[1]+[0.0]*p
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
