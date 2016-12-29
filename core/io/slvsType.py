# -*- coding: utf-8 -*-
class SLVS_Code():
    def __init__(self):
        self.Param_num = 0x30023
        self.Request_num = 0x3
        self.Entity_num = 0x30020
        self.Constraint_num = 0x0
        self.Slvs_code = """±²³SolveSpaceREVa


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
Group.name=sketch-in-plane
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
    def next(self, num):
        num -= num%0x10000
        num += 0x10000
    #TODO:
    #point type:(x, y, fix=False)
    #line type:(point1, point2, len)
    #chain type:(point1, point2, point3, len1, len2, len3)
    def output(self):
        
        return self.Slvs_code
    
    def point(self, x, y, fix=False):
        ''''''
    
    def line(self, point1, point2, len=False):
        #AddParam
        self.next(self.Param_num)
        self.Param_num += 0x10
        self.Slvs_code += """
Param.h.v.=%08x"""%self.Param_num+"""
Param.val=%.20f"""%point1[0]+"""
AddParam
"""
        self.Param_num += 0x1
        self.Slvs_code += """
Param.h.v.=%08x"""%self.Param_num+"""
Param.val=%.20f"""%point1[1]+"""
AddParam
"""
        self.Param_num += 0x2
        self.Slvs_code += """
Param.h.v.=%08x"""%self.Param_num+"""
Param.val=%.20f"""%point2[0]+"""
AddParam
"""
        self.Param_num += 0x1
        self.Slvs_code += """
Param.h.v.=%08x"""%self.Param_num+"""
Param.val=%.20f"""%point2[1]+"""
AddParam
"""
        #AddRequest
        self.Request_num += 0x1
        self.Slvs_code += """
Request.h.v=%08x"""%self.Request_num+"""
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest
"""
        #AddEntity & AddConstraint
        self.next(self.Entity_num)
        self.Slvs_code += """
Entity.h.v=%08x"""%self.Entity_num+"""
Entity.type=11000
Entity.construction=0
Entity.point[0].v=%08x"""%(self.Entity_num+1)+"""
Entity.point[1].v=%08x"""%(self.Entity_num+2)+"""
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity
"""
        self.Entity_num += 0x1
        self.Slvs_code += """
Entity.h.v=%08x"""%self.Entity_num+"""
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.20f"""%point1[0]+"""
Entity.actPoint.y=%.20f"""%point1[1]+"""
Entity.actVisible=1
AddEntity
"""
        self.Entity_num += 0x1
        self.Slvs_code += """
Entity.h.v=%08x"""%self.Entity_num+"""
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=%.20f"""%point2[0]+"""
Entity.actPoint.y=%.20f"""%point2[1]+"""
Entity.actVisible=1
AddEntity
"""
        #AddConstraint
        if point1[2]:
            ''''''
        if point2[2]:
            ''''''
        if len:
            ''''''
    
    def chain(self, point1, point2, point3):
        ''''''
    
    def slider(self, pt, line):
        ''''''
