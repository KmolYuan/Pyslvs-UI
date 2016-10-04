from dxfwrite import DXFEngine as dxf

def dxf_code(file_name, table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
    mechanism = dxf.drawing(file_name)
    for i in range(len(table_point)):
        pt = dxf.point((table_point[i][3], table_point[i][4]))
        mechanism.add(pt)
    for i in range(len(table_line)):
        ln = dxf.line((table_point[table_line[i][0]][3], table_point[table_line[i][0]][4]),
            (table_point[table_line[i][1]][3], table_point[table_line[i][1]][4]))
        mechanism.add(ln)
    for i in range(len(table_chain)):
        ln1 = dxf.line((table_point[table_chain[i][0]][3], table_point[table_chain[i][0]][4]),
            (table_point[table_chain[i][1]][3], table_point[table_chain[i][1]][4]))
        ln2 = dxf.line((table_point[table_chain[i][1]][3], table_point[table_chain[i][1]][4]),
            (table_point[table_chain[i][2]][3], table_point[table_chain[i][2]][4]))
        ln3 = dxf.line((table_point[table_chain[i][0]][3], table_point[table_chain[i][0]][4]),
            (table_point[table_chain[i][2]][3], table_point[table_chain[i][2]][4]))
        mechanism.add(ln1)
        mechanism.add(ln2)
        mechanism.add(ln3)
    mechanism.save()
