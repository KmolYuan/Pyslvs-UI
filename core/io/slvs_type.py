class SLVS_Code():
    def _init_(self):
        self.Entity_num = 4
        self.Constraint_num = 1
        self.Param_num = 4
        self.Request_num = 4
        self.AddParam = []
        self.AddRequest = []
        self.AddEntity = []
        self.AddConstraint = []
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
    #TODO:
    def output(self):
        
        return self.Slvs_Script
    
    def point(self, x, y):
        self.AddParam += [[x, y]]
        self.AddRequest += ["Point"]
    
    def line(self, x1, y1, x2, y2):
        self.AddParam += [[[x1, y1], [x2, y2]]]
        self.AddRequest += ["Line"]
    
    def slider(self, pt, line):
        """"""
    
    def formate_input(self, table_point, table_line, table_chain, table_shaft, table_slider, table_rod):
        point_numberlist = [[None] for i in range(len(table_point))]
        #point
        for i in range(1, len(table_point) if len(table_point)>=1 else 1):
            case1 = False
            case2 = False
            for k in table_line:
                case1 = i in k
                if i in k: break
            for k in table_chain:
                case2 = i in k
                if i in k: break
            if  not(case1 or case2):
                self.Slvs_Script += """
Param.h.v.=%04x"""%self.Param_num+"""0010
Param.val=%.020f"""%table_point[i][0]+"""
AddParam

Param.h.v.=%04x"""%(self.Param_num+1)+"""0011
Param.val=%.020f"""%table_point[i][1]+"""
AddParam

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
                self.Param_num += 1
                self.Request_num += 1
                if table_point[i][2]:
                    self.Slvs_Script += """
Constraint.h.v=%08x"""%self.Constraint_num+"""
Constraint.type=200
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=%04x"""%self.Entity_num+"""0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
"""
                    self.Constraint_num += 1
        for i in range(len(table_line)):
            if None in point_numberlist[table_line[i][0]]: point_numberlist[table_line[i][0]] = []
            if None in point_numberlist[table_line[i][1]]: point_numberlist[table_line[i][1]] = []
            point_numberlist[table_line[i][0]] += ["%04x"%self.Entity_num+"0001"]
            point_numberlist[table_line[i][1]] += ["%04x"%self.Entity_num+"0002"]
            self.Slvs_Script += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Param.h.v.=%04x"""%self.Param_num+"""0010
Param.val=%.020f"""%table_point[table_line[i][0]][0]+"""
AddParam

Param.h.v.=%04x"""%self.Param_num+"""0011
Param.val=%.020f"""%table_point[table_line[i][0]][1]+"""
AddParam

Param.h.v.=%04x"""%self.Param_num+"""0013
Param.val=%.020f"""%table_point[table_line[i][1]][0]+"""
AddParam

Param.h.v.=%04x"""%self.Param_num+"""0014
Param.val=%.020f"""%table_point[table_line[i][1]][1]+"""
AddParam

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
        #chain
        for i in range(len(table_chain)):
            if None in point_numberlist[table_chain[i][0]]: point_numberlist[table_chain[i][0]] = []
            if None in point_numberlist[table_chain[i][1]]: point_numberlist[table_chain[i][1]] = []
            if None in point_numberlist[table_chain[i][2]]: point_numberlist[table_chain[i][2]] = []
            point_numberlist[table_chain[i][0]] += ["%04x"%self.Entity_num+"0001"]
            point_numberlist[table_chain[i][1]] += ["%04x"%self.Entity_num+"0002"]
            point_numberlist[table_chain[i][2]] += ["%04x"%(self.Entity_num+1)+"0002"]
            pa = """Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_chain[i][0]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_chain[i][0]][1]+"""
Entity.actVisible=1
AddEntity
"""
            pb = """Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.020f"""%table_point[table_chain[i][1]][0]+"""
Entity.actPoint.y=%.020f"""%table_point[table_chain[i][1]][1]+"""
Entity.actVisible=1
AddEntity
"""
            pc = """Entity.type=2001
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
        #coincident
        for k in point_numberlist:
            for i in range(len(k)-1):
                try:
                    self.Slvs_Script += """
Constraint.h.v=%08x"""%self.Constraint_num+"""
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v="""+k[i]+"""
Constraint.ptB.v="""+k[i+1]+"""
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
"""
                    self.Constraint_num += 1
                except: pass
        #AddParam
        #AddRequest
        #AddEntity
        #AddConstraint
