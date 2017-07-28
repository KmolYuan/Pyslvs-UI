# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf

def dxfSketch(file_name, Point, Link, Chain):
    mechanism = dxf.drawing(file_name)
    for e in Point:
        mechanism.add(dxf.point((e.cx, e.cy)))
    for e in Link:
        mechanism.add(dxf.line((Point[e.start].cx, Point[e.start].cy), (Point[e.end].cx, Point[e.end].cy)))
    for e in Chain:
        mechanism.add(dxf.line((Point[e.p1].cx, Point[e.p1].cy), (Point[e.p2].cx, Point[e.p2].cy)))
        mechanism.add(dxf.line((Point[e.p2].cx, Point[e.p2].cy), (Point[e.p3].cx, Point[e.p3].cy)))
        mechanism.add(dxf.line((Point[e.p1].cx, Point[e.p1].cy), (Point[e.p3].cx, Point[e.p3].cy)))
    mechanism.save()
