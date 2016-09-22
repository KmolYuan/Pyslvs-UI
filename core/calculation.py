# -*- coding: utf-8 -*-
from .slvs import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Solvespace():
    def __init__(self):
        self.Script = """# -*- coding: utf-8 -*-
'''This Code is Generate by Pyslvs.'''

from slvs import *
import matplotlib.pyplot as plt

#Please Choose Point number.
Point_num = 2
wx = Point_num*2+5
wy = Point_num*2+6
"""
        self.Entity_num = 4
        self.Constraint_num = 1
        self.Param_num = 262160
        self.Request_num = 4
        self.Slvs_Script = """±²³SolveSpaceREVa


Group.h.v=00000001
Group.type=5000
Group.name=#references
Group.color=ff000000
Group.skipFirst=0
Group.predef.swapUV=0
Group.predef.negateU=0
Group.predef.negateV=0
Group.visible=1
Group.suppress=0
Group.relaxConstraints=0
Group.allowRedundant=0
Group.allDimsReference=0
Group.remap={
}
AddGroup

Group.h.v=00000002
Group.type=5001
Group.order=1
Group.name=Pyslvs-2D
Group.activeWorkplane.v=80020000
Group.color=ff000000
Group.subtype=6000
Group.skipFirst=0
Group.predef.q.w=1.00000000000000000000
Group.predef.origin.v=00010001
Group.predef.swapUV=0
Group.predef.negateU=0
Group.predef.negateV=0
Group.visible=1
Group.suppress=0
Group.relaxConstraints=0
Group.allowRedundant=0
Group.allDimsReference=0
Group.remap={
}
AddGroup

Param.h.v.=00010010
AddParam

Param.h.v.=00010011
AddParam

Param.h.v.=00010012
AddParam

Param.h.v.=00010020
Param.val=1.00000000000000000000
AddParam

Param.h.v.=00010021
AddParam

Param.h.v.=00010022
AddParam

Param.h.v.=00010023
AddParam

Param.h.v.=00020010
AddParam

Param.h.v.=00020011
AddParam

Param.h.v.=00020012
AddParam

Param.h.v.=00020020
Param.val=0.50000000000000000000
AddParam

Param.h.v.=00020021
Param.val=0.50000000000000000000
AddParam

Param.h.v.=00020022
Param.val=0.50000000000000000000
AddParam

Param.h.v.=00020023
Param.val=0.50000000000000000000
AddParam

Param.h.v.=00030010
AddParam

Param.h.v.=00030011
AddParam

Param.h.v.=00030012
AddParam

Param.h.v.=00030020
Param.val=0.50000000000000000000
AddParam

Param.h.v.=00030021
Param.val=-0.50000000000000000000
AddParam

Param.h.v.=00030022
Param.val=-0.50000000000000000000
AddParam

Param.h.v.=00030023
Param.val=-0.50000000000000000000
AddParam

Request.h.v=00000001
Request.type=100
Request.group.v=00000001
Request.construction=0
AddRequest

Request.h.v=00000002
Request.type=100
Request.group.v=00000001
Request.construction=0
AddRequest

Request.h.v=00000003
Request.type=100
Request.group.v=00000001
Request.construction=0
AddRequest

Entity.h.v=00010000
Entity.type=10000
Entity.construction=0
Entity.point[0].v=00010001
Entity.normal.v=00010020
Entity.actVisible=1
AddEntity

Entity.h.v=00010001
Entity.type=2000
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=00010020
Entity.type=3000
Entity.construction=0
Entity.point[0].v=00010001
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00020000
Entity.type=10000
Entity.construction=0
Entity.point[0].v=00020001
Entity.normal.v=00020020
Entity.actVisible=1
AddEntity

Entity.h.v=00020001
Entity.type=2000
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=00020020
Entity.type=3000
Entity.construction=0
Entity.point[0].v=00020001
Entity.actNormal.w=0.50000000000000000000
Entity.actNormal.vx=0.50000000000000000000
Entity.actNormal.vy=0.50000000000000000000
Entity.actNormal.vz=0.50000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00030000
Entity.type=10000
Entity.construction=0
Entity.point[0].v=00030001
Entity.normal.v=00030020
Entity.actVisible=1
AddEntity

Entity.h.v=00030001
Entity.type=2000
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=00030020
Entity.type=3000
Entity.construction=0
Entity.point[0].v=00030001
Entity.actNormal.w=0.50000000000000000000
Entity.actNormal.vx=-0.50000000000000000000
Entity.actNormal.vy=-0.50000000000000000000
Entity.actNormal.vz=-0.50000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80020000
Entity.type=10000
Entity.construction=0
Entity.point[0].v=80020002
Entity.normal.v=80020001
Entity.actVisible=1
AddEntity

Entity.h.v=80020001
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80020002
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80020002
Entity.type=2012
Entity.construction=0
Entity.actVisible=1
AddEntity
"""
    
    def table_process(self, table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter):
        table_point_l = []
        table_line_l = []
        table_chain_l = []
        table_shaft_l = []
        table_slider_l = []
        table_rod_l = []
        table_parameter_l = []
        for i in range(table_parameter.rowCount()):
            try: table_parameter_l += [float(table_parameter.item(i, 1).text())]
            except: pass
        for i in range(table_point.rowCount()):
            k = []
            for j in range(1, 3):
                #float
                table_item = table_point.item(i, j).text()
                table_val = table_item if not 'n' in table_item else table_parameter_l[int(table_item.replace("n", ""))]
                k += [float(table_val)]
            #bool
            k += [bool(table_point.item(i, 3).checkState())]
            #XY
            try:
                k += [float(table_point.item(i, 4).text().replace("(", "").replace(")", "").split(", ")[0])]
                k += [float(table_point.item(i, 4).text().replace("(", "").replace(")", "").split(", ")[1])]
            except: pass
            table_point_l += [k]
        for i in range(table_line.rowCount()):
            k = []
            for j in range(1, 3):
                #int Point
                table_item = table_line.item(i, j).text().replace("Point", "")
                k += [int(table_item)]
            #float
            table_item = table_line.item(i, 3).text()
            table_val = table_item if not 'n' in table_item else table_parameter_l[int(table_item.replace("n", ""))]
            k += [float(table_val)]
            table_line_l += [k]
        for i in range(table_chain.rowCount()):
            k = []
            for j in range(1, 4):
                #int Point
                table_item = table_chain.item(i, j).text().replace("Point", "")
                k += [int(table_item)]
            for j in range(4, 7):
                #float
                table_item = table_chain.item(i, j).text()
                table_val = table_item if not 'n' in table_item else table_parameter_l[int(table_item.replace("n", ""))]
                k += [float(table_val)]
            table_chain_l += [k]
        for i in range(table_shaft.rowCount()):
            k = []
            for j in range(1, 3):
                #int Point
                table_item = table_shaft.item(i, j).text().replace("Point", "")
                k += [int(table_item)]
            for j in range(3, 5):
                #float angle
                table_item = table_shaft.item(i, j).text().replace("°", "")
                table_val = table_item if not 'n' in table_item else table_parameter_l[int(table_item.replace("n", ""))]
                k += [float(table_val)]
            table_item = table_shaft.item(i, 5).text().replace("°", "")
            k += [float(table_item if table_shaft.item(i, 5) else False)]
            table_shaft_l += [k]
        for i in range(table_slider.rowCount()):
            k = []
            #int Point
            k += [int(table_slider.item(i, 1).text().replace("Point", ""))]
            #int Line
            k += [int(table_slider.item(i, 2).text().replace("Line", ""))]
            table_slider_l += [k]
        for i in range(table_rod.rowCount()):
            k = []
            for j in range(1, 4):
                #int Point
                table_item = table_rod.item(i, j).text().replace("Point", "")
                k += [int(table_item)]
            #float
            table_item = table_rod.item(i, 4).text()
            table_val = table_item if not 'n' in table_item else table_parameter_l[int(table_item.replace("n", ""))]
            k += [float(table_val)]
            table_slider_l += [k]
        return table_point_l, table_line_l, table_chain_l, table_shaft_l, table_slider_l, table_rod_l
    
    def static_process(self, table_point, table_line, table_chain, table_shaft, table_slider, table_rod, filename, table_parameter):
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = self.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter)
        sys = System(1000)
        #Pre-oder
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
        self.Script += """
def """+filename.replace(" ", "_")+"""(degree):
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
    other = -1 if degree >= 180 else 1

    p7 = sys.add_param(0.0)
    p8 = sys.add_param(0.0)
    Point1 = Point2d(Workplane1, p7, p8)
    Constraint.dragged(Workplane1, Point1)
"""
        Point = [Point1]
        #Load tables to constraint
        for i in range(1, len(table_point) if len(table_point)>=1 else 1):
            x_val = 0
            if not(len(table_shaft)>=1):
                x = sys.add_param(table_point[i][0])
                y = sys.add_param(table_point[i][1])
            else:
                for j in range(len(table_shaft)):
                    case = table_shaft[j][1]==i
                    if case and table_shaft[j][4]:
                        angle = table_shaft[j][4]
                        other = -1 if angle >= 180 else 1
                        a = table_shaft[j][0]
                        x = sys.add_param(table_point[a][0])
                        x_val = table_point[a][0]
                        y = sys.add_param(table_point[i][1]*other)
                    else:
                        x_val = table_point[i][0]
                        x = sys.add_param(table_point[i][0])
                        y = sys.add_param(table_point[i][1])
            p = Point2d(Workplane1, x, y)
            Point += [p]
            self.Script += """
    p"""+str(i*2+7)+""" = sys.add_param("""+str(x_val)+""")
    p"""+str(i*2+8)+""" = sys.add_param("""+str(table_point[i][1])+""")
    Point"""+str(i+1)+""" = Point2d(Workplane1, p"""+str(i*2+7)+""", p"""+str(i*2+8)+""")
"""
            if table_point[i][2]:
                Constraint.dragged(Workplane1, p)
                self.Script += """    Constraint.dragged(Workplane1, Point"""+str(i+1)+""")
"""
        for i in range(len(table_chain)):
            pa = table_chain[i][0]
            pb = table_chain[i][1]
            pc = table_chain[i][2]
            lengab = table_chain[i][3]
            lengbc = table_chain[i][4]
            lengac = table_chain[i][5]
            Constraint.distance(lengab, Workplane1, Point[pa], Point[pb])
            Constraint.distance(lengbc, Workplane1, Point[pb], Point[pc])
            Constraint.distance(lengac, Workplane1, Point[pa], Point[pc])
            self.Script += """    Constraint.distance("""+str(lengab)+""", Workplane1, Point"""+str(pa+1)+""", Point"""+str(pb+1)+""")
    Constraint.distance("""+str(lengbc)+""", Workplane1, Point"""+str(pb+1)+""", Point"""+str(pc+1)+""")
    Constraint.distance("""+str(lengac)+""", Workplane1, Point"""+str(pa+1)+""", Point"""+str(pc+1)+""")
"""
        for i in range(len(table_line)):
            start = table_line[i][0]
            end = table_line[i][1]
            leng = table_line[i][2]
            Constraint.distance(leng, Workplane1, Point[start], Point[end])
            self.Script += """    Constraint.distance("""+str(leng)+""", Workplane1, Point"""+str(start+1)+""", Point"""+str(end+1)+""")
"""
        for i in range(len(table_slider)):
            pt = table_slider[i][0]
            start = table_line[table_slider[i][1]][0]
            end = table_line[table_slider[i][1]][1]
            line = LineSegment2d(Workplane1, Point[start], Point[end])
            Constraint.on(Workplane1, Point[pt], line)
            self.Script += """    Constraint.on(Workplane1, Point"""+str(pt+1)+""", LineSegment2d(Workplane1, Point"""+str(start+1)+""", Point"""+str(end+1)+""")
"""
            self.Constraint_num += 1
        if len(table_shaft) >= 1:
            pN = sys.add_param(10)
            pNN = sys.add_param(0.0)
            PointN = Point2d(Workplane1, pN, pNN)
            Point += [PointN]
            Constraint.dragged(Workplane1, Point[-1])
            Line0 = LineSegment2d(Workplane1, Point[0], Point[-1])
            self.Script += """    px = sys.add_param(10)
    py = sys.add_param(0.0)
    PointN = Point2d(Workplane1, px, py)
    Constraint.dragged(Workplane1, PointN)
    Line0 = LineSegment2d(Workplane1, Point1, PointN)
"""
            for i in range(len(table_shaft)):
                center = table_shaft[i][0]
                reference = table_shaft[i][1]
                line = LineSegment2d(Workplane1, Point[center], Point[reference])
                try:
                    angle = table_shaft[i][4]
                    Constraint.angle(Workplane1, angle, line, Line0, False)
                except: pass
                self.Script += """    Line1 = LineSegment2d(Workplane1, Point"""+str(center+1)+""", Point"""+str(reference+1)+""")
    Constraint.angle(Workplane1, degree, Line1, Line0, False)
    
    sys.solve()
    if (sys.result == SLVS_RESULT_OKAY):
        x = sys.get_param(wx).val
        y = sys.get_param(wy).val
        return x, y

if __name__=="__main__":
    Xval  = []
    Yval  = []
    for i in range(0, 361, 1):
        x, y = """+filename.replace(" ", "_")+"""(i)
        Xval += [x]
        Yval += [y]
    print("Solve Completed")
    plt.plot(Xval, Yval)
    plt.show()
"""
        sys.solve()
        result = []
        if (sys.result == SLVS_RESULT_OKAY):
            for i in range(len(table_point)*2):
                result += [sys.get_param(i+7).val]
        elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
        elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
        elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        return result, sys.dof

    def Solve(self, point_int, angle, table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter):
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = self.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter)
        sys = System(1000)
        #Pre-oder
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
        p9 = sys.add_param(10)
        p10 = sys.add_param(0.0)
        Point2 = Point2d(Workplane1, p9, p10)
        Constraint.dragged(Workplane1, Point2)
        Line0 = LineSegment2d(Workplane1, Point1, Point2)
        Point = [Point1]
        #Load tables to constraint
        for i in range(1, len(table_point)):
            for j in range(len(table_shaft)):
                case = table_shaft[j][1]==i
                if case:
                    if angle >= 180: other = -1
                    else: other = 1
                    a = table_shaft[j][0]
                    x = sys.add_param(table_point[a][0])
                    y = sys.add_param(table_point[i][1]*other)
                else:
                    x = sys.add_param(table_point[i][0])
                    y = sys.add_param(table_point[i][1])
            p = Point2d(Workplane1, x, y)
            Point += [p]
            if table_point[i][2]:
                Constraint.dragged(Workplane1, p)
        for i in range(len(table_chain)):
            pa = table_chain[i][0]
            pb = table_chain[i][1]
            pc = table_chain[i][2]
            lengab = table_chain[i][3]
            lengbc = table_chain[i][4]
            lengac = table_chain[i][5]
            Constraint.distance(lengab, Workplane1, Point[pa], Point[pb])
            Constraint.distance(lengbc, Workplane1, Point[pb], Point[pc])
            Constraint.distance(lengac, Workplane1, Point[pa], Point[pc])
        for i in range(len(table_line)):
            start = table_line[i][0]
            end = table_line[i][1]
            leng = table_line[i][2]
            Constraint.distance(leng, Workplane1, Point[start], Point[end])
        for i in range(len(table_slider)):
            pt = table_slider[i][0]
            start = table_line[table_slider[i][1]][1]
            end = table_line[table_slider[i][1]][1]
            line = LineSegment2d(Workplane1, Point[start], Point[end])
            Constraint.on(Workplane1, Point[pt], line)
        for i in range(len(table_shaft)):
            center = table_shaft[i][0]
            reference = table_shaft[i][1]
            line = LineSegment2d(Workplane1, Point[center], Point[reference])
            Constraint.angle(Workplane1, angle, line, Line0, False)
        #TODO: to be continue...
        sys.solve()
        x = 0
        y = 0
        if (sys.result == SLVS_RESULT_OKAY):
            x = sys.get_param((point_int+2)*2+5).val
            y = sys.get_param((point_int+2)*2+6).val
        elif (sys.result == SLVS_RESULT_INCONSISTENT): print ("SLVS_RESULT_INCONSISTENT")
        elif (sys.result == SLVS_RESULT_DIDNT_CONVERGE): print ("SLVS_RESULT_DIDNT_CONVERGE")
        elif (sys.result == SLVS_RESULT_TOO_MANY_UNKNOWNS): print ("SLVS_RESULT_TOO_MANY_UNKNOWNS")
        return x, y
    
    def slvs_formate(self, table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter):
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = self.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter)
        print(table_line)
        #point
        for i in range(1, len(table_point) if len(table_point)>=1 else 1):
            self.Slvs_Script += """
Param.h.v.=%08x"""%self.Param_num+"""
Param.val=%.020f"""%table_point[i][0]+"""
AddParam

Param.h.v.=%08x"""%(self.Param_num+1)+"""
Param.val=%.020f"""%table_point[i][1]+"""
AddParam
"""
            if table_line or table_chain:
                for j in [table_line, table_chain]:
                    for k in j:
                        if not(i in k):
                            self.Slvs_Script += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Entity.h.v=%04x"""%self.Entity_num+"""0000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[i][0]+"""
Entity.actPoint.y=%.020f"""%table_point[i][1]+"""
Entity.actVisible=1
AddEntity
"""
                            self.Entity_num += 1
                            self.Request_num += 1
            else:
                self.Slvs_Script += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Entity.h.v=%04x"""%self.Entity_num+"""0000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[i][0]+"""
Entity.actPoint.y=%.020f"""%table_point[i][1]+"""
Entity.actVisible=1
AddEntity
"""
                self.Entity_num += 1
                self.Request_num += 1
            if table_point[i][2]:
                self.Slvs_Script += """
Constraint.h.v=%08x"""%self.Constraint_num+"""
Constraint.type=200
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=%04x"""%(i+3)+"""0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
"""
                self.Constraint_num += 1
            self.Param_num += 3
        for i in range(len(table_line)):
            self.Slvs_Script += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Entity.h.v=%04x"""%self.Entity_num+"""0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=%04x"""%self.Entity_num+"""0001
Entity.point[1].v=%04x"""%self.Entity_num+"""0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=%04x"""%self.Entity_num+"""0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_line[i][0]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_line[i][0]][1]+"""
Entity.actVisible=1
AddEntity

Entity.h.v=%04x"""%self.Entity_num+"""0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_line[i][1]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_line[i][1]][1]+"""
Entity.actVisible=1
AddEntity

Constraint.h.v=%08x"""%self.Constraint_num+"""
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA=%.020f"""%table_line[i][2]+"""
Constraint.ptA.v=%04x"""%self.Entity_num+"""0001
Constraint.ptB.v=%04x"""%self.Entity_num+"""0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-10
Constraint.disp.offset.y=-10
AddConstraint
"""
            self.Entity_num += 1
            self.Request_num += 1
            self.Constraint_num += 1
        for i in range(len(table_chain)):
            pa = """
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_chain[i][0]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_chain[i][0]][1]+"""
Entity.actVisible=1
AddEntity
"""
            pb = """
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_chain[i][1]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_chain[i][1]][1]+"""
Entity.actVisible=1
AddEntity
"""
            pc = """
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_chain[i][2]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_chain[i][2]][1]+"""
Entity.actVisible=1
AddEntity
"""
            self.Slvs_Script += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=%08x"""%(self.Request_num+1)+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=%08x"""%(self.Request_num+2)+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Entity.h.v=%04x"""%self.Entity_num+"""0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=%04x"""%self.Entity_num+"""0001
Entity.point[1].v=%04x"""%self.Entity_num+"""0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=%04x"""%self.Entity_num+"""0001
"""+pa+"""
Entity.h.v=%04x"""%self.Entity_num+"""0002
"""+pb+"""
Entity.h.v=%04x"""%(self.Entity_num+1)+"""0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=%04x"""%(self.Entity_num+1)+"""0001
Entity.point[1].v=%04x"""%(self.Entity_num+1)+"""0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=%04x"""%(self.Entity_num+1)+"""0001
"""+pb+"""
Entity.h.v=%04x"""%(self.Entity_num+1)+"""0002
"""+pc+"""
Entity.h.v=%04x"""%(self.Entity_num+2)+"""0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=%04x"""%(self.Entity_num+2)+"""0001
Entity.point[1].v=%04x"""%(self.Entity_num+2)+"""0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=%04x"""%(self.Entity_num+2)+"""0001
"""+pa+"""
Entity.h.v=%04x"""%(self.Entity_num+2)+"""0002
"""+pc+"""
Constraint.h.v=%08x"""%self.Constraint_num+"""
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA=%.020f"""%table_line[i][2]+"""
Constraint.ptA.v=%04x"""%self.Entity_num+"""0001
Constraint.ptB.v=%04x"""%self.Entity_num+"""0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-10
Constraint.disp.offset.y=-10
AddConstraint

Constraint.h.v=%08x"""%(self.Constraint_num+1)+"""
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA=%.020f"""%table_line[i][2]+"""
Constraint.ptA.v=%04x"""%(self.Entity_num+1)+"""0001
Constraint.ptB.v=%04x"""%(self.Entity_num+1)+"""0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-10
Constraint.disp.offset.y=-10
AddConstraint

Constraint.h.v=%08x"""%(self.Constraint_num+2)+"""
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA=%.020f"""%table_line[i][2]+"""
Constraint.ptA.v=%04x"""%(self.Entity_num+2)+"""0001
Constraint.ptB.v=%04x"""%(self.Entity_num+2)+"""0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-10
Constraint.disp.offset.y=-10
AddConstraint

Constraint.h.v=%08x"""%(self.Constraint_num+3)+"""
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=%04x"""%self.Entity_num+"""0002
Constraint.ptB.v=%04x"""%(self.Entity_num+1)+"""0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=%08x"""%(self.Constraint_num+4)+"""
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=%04x"""%(self.Entity_num+1)+"""0002
Constraint.ptB.v=%04x"""%(self.Entity_num+2)+"""0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=%08x"""%(self.Constraint_num+5)+"""
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=%04x"""%(self.Entity_num+2)+"""0002
Constraint.ptB.v=%04x"""%self.Entity_num+"""0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
"""
            self.Entity_num += 3
            self.Request_num += 3
            self.Constraint_num += 6
        #TODO:
        #AddParam
        #AddRequest
        #AddEntity
        #AddConstraint
