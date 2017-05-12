# -*- coding: utf-8 -*-

def slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod):
    script = """'''This code is generate by Pyslvs'''
from slvs import *

def mechanism({}):""".format(', '.join(['angle{}'.format(i) for i in range(len(Shaft))]))
    classScript = """
Sys = System({})
p0 = Sys.add_param(0.0)
p1 = Sys.add_param(0.0)
p2 = Sys.add_param(0.0)
Origin = Point3d(p0, p1, p2)
qw, qx, qy, qz = Slvs_MakeQuaternion(1, 0, 0, 0, 1, 0)
p3 = Sys.add_param(qw)
p4 = Sys.add_param(qx)
p5 = Sys.add_param(qy)
p6 = Sys.add_param(qz)
Normal1 = Normal3d(p3, p4, p5, p6)
Workplane1 = Workplane(Origin, Normal1)
p7 = Sys.add_param(0.0)
p8 = Sys.add_param(0.0)
Point0 = Point2d(Workplane1, p7, p8)
Constraint.dragged(Workplane1, Point0)
""".format(len(Point)*2+9)
    for i, e in enumerate(Point):
        bx = i*2+9
        by = i*2+10
        classScript += "p{} = Sys.add_param({})\n".format(bx, e.cx)
        classScript += "p{} = Sys.add_param({})\n".format(by, e.cy)
        classScript += "Point{} = Point2d(Workplane1, p{}, p{})\n".format(i+1, bx, by)
        if e.fix: classScript += "Constraint.dragged(Workplane1, Point{})\n".format(i+1)
    for e in Chain:
        classScript += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p1p2, e.p1+1, e.p2+1)
        classScript += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p2p3, e.p2+1, e.p3+1)
        classScript += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.p1p3, e.p1+1, e.p3+1)
    for e in Line:
        classScript += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.len, e.start+1, e.end+1)
    for e in Slider:
        classScript += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e.cen+1, e.start+1, e.end+1)
    for e in Rod:
        classScript += "Constraint.on(Workplane1, Point{}, LineSegment2d(Workplane1, Point{}, Point{})\n".format(e.cen+1, e.start+1, e.end+1)
        classScript += "Constraint.distance({}, Workplane1, Point{}, Point{})\n".format(e.pos, e.start+1, e.cen+1)
    for e in Shaft:
        classScript += "Constraint.angle(Workplane1, {}, LineSegment2d(Workplane1, Point{}, Point{}), xAxis, False)\n".format(e.demo, e.cen+1, e.ref+1)
    classScript += """Sys.solve()
if Sys.result==SLVS_RESULT_OKAY:
    point_int = {}
    x = round(float(Sys.get_param((point_int+2)*2+5).val), 4)
    y = round(float(Sys.get_param((point_int+2)*2+6).val), 4)
else:
    if Sys.result==SLVS_RESULT_INCONSISTENT:
        print("SLVS_RESULT_INCONSISTENT")
    elif Sys.result==SLVS_RESULT_DIDNT_CONVERGE:
        print("SLVS_RESULT_DIDNT_CONVERGE")
    elif Sys.result==SLVS_RESULT_TOO_MANY_UNKNOWNS:
        print("SLVS_RESULT_TOO_MANY_UNKNOWNS")""".format(len(Point))
    classScript = classScript.replace('\n', '\n    ')
    script += classScript+'\n'
    return script
