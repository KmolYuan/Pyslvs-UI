# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf

def dxfCode(file_name, Point, Link, Chain):
    mechanism = dxf.drawing(file_name)
    for i in range(len(Point)):
        pt = dxf.point((Point[i]['cx'], Point[i]['cy']))
        mechanism.add(pt)
    for i in range(len(Link)):
        ln = dxf.line((Point[Link[i]['cen']]['cx'], Point[Link[i]['cen']]['cy']),
            (Point[Link[i]['ref']]['cx'], Point[Link[i]['ref']]['cy']))
        mechanism.add(ln)
    for i in range(len(Chain)):
        ln1 = dxf.line((Point[Chain[i]['p1']]['cx'], Point[Chain[i]['p1']]['cy']),
            (Point[Chain[i]['p2']]['cx'], Point[Chain[i]['p2']]['cy']))
        ln2 = dxf.line((Point[Chain[i]['p2']]['cx'], Point[Chain[i]['p2']]['cy']),
            (Point[Chain[i]['p3']]['cx'], Point[Chain[i]['p3']]['cy']))
        ln3 = dxf.line((Point[Chain[i]['p1']]['cx'], Point[Chain[i]['p1']]['cy']),
            (Point[Chain[i]['p3']]['cx'], Point[Chain[i]['p3']]['cy']))
        mechanism.add(ln1)
        mechanism.add(ln2)
        mechanism.add(ln3)
    mechanism.save()
