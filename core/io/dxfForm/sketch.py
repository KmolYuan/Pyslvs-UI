# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf

def dxfSketch(file_name, Point, Link, Chain):
    mechanism = dxf.drawing(file_name)
    for e in Point:
        pt = dxf.point((e['cx'], e['cy']))
        mechanism.add(pt)
    for e in Link:
        ln = dxf.line((Point[e['cen']]['cx'], Point[e['cen']]['cy']), (Point[e['ref']]['cx'], Point[e['ref']]['cy']))
        mechanism.add(ln)
    for e in Chain:
        ln1 = dxf.line((Point[e['p1']]['cx'], Point[e['p1']]['cy']), (Point[e['p2']]['cx'], Point[e['p2']]['cy']))
        ln2 = dxf.line((Point[e['p2']]['cx'], Point[e['p2']]['cy']), (Point[e['p3']]['cx'], Point[e['p3']]['cy']))
        ln3 = dxf.line((Point[e['p1']]['cx'], Point[e['p1']]['cy']), (Point[e['p3']]['cx'], Point[e['p3']]['cy']))
        mechanism.add(ln1)
        mechanism.add(ln2)
        mechanism.add(ln3)
    mechanism.save()
