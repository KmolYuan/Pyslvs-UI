# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf

def dxfCode(file_name, table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
    mechanism = dxf.drawing(file_name)
    for i in range(len(table_point)):
        pt = dxf.point((table_point[i]['cx'], table_point[i]['cy']))
        mechanism.add(pt)
    for i in range(len(table_line)):
        ln = dxf.line((table_point[table_line[i]['cen']]['cx'], table_point[table_line[i]['cen']]['cy']),
            (table_point[table_line[i]['ref']]['cx'], table_point[table_line[i]['ref']]['cy']))
        mechanism.add(ln)
    for i in range(len(table_chain)):
        ln1 = dxf.line((table_point[table_chain[i]['p1']]['cx'], table_point[table_chain[i]['p1']]['cy']),
            (table_point[table_chain[i]['p2']]['cx'], table_point[table_chain[i]['p2']]['cy']))
        ln2 = dxf.line((table_point[table_chain[i]['p2']]['cx'], table_point[table_chain[i]['p2']]['cy']),
            (table_point[table_chain[i]['p3']]['cx'], table_point[table_chain[i]['p3']]['cy']))
        ln3 = dxf.line((table_point[table_chain[i]['p1']]['cx'], table_point[table_chain[i]['p1']]['cy']),
            (table_point[table_chain[i]['p3']]['cx'], table_point[table_chain[i]['p3']]['cy']))
        mechanism.add(ln1)
        mechanism.add(ln2)
        mechanism.add(ln3)
    mechanism.save()
