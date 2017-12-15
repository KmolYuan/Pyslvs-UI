# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

def slvs2D(VPointList, VLinkList, fileName):
    #The number of same points.
    point_num = [[] for vpoint in VPointList]
    #The number of same lines.
    line_num = [[] for vlink in VLinkList if vlink.name!="ground"]
    script_group = '''±²³SolveSpaceREVa


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
'''
    script_param = '''
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
'''
    #Add "Param"
    param_num = 0x40000
    for i, vlink in enumerate(VLinkList):
        if i==0:
            continue
        param_num += 0x10
        for p in vlink.points:
            script_param = Param(script_param, param_num, VPointList[p].cx)
            param_num += 1
            script_param = Param(script_param, param_num, VPointList[p].cy)
            param_num += 2
        param_num = up(param_num, 4)
    script_request = '''
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
'''
    #Add "Request"
    request_num = 0x4
    for i in range(len(VLinkList)):
        if i==0:
            continue
        script_request = Request(script_request, request_num)
        request_num += 1
    script_entity = '''
Entity.h.v=00010000
Entity.type=10000
Entity.construction=0
Entity.point[0].v=00010001
Entity.normal.v=00010020
Entity.actVisible=1
AddEntity

Entity.h.v=00010001
Entity.type=2000
Entity.construction=1
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
Entity.construction=1
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
Entity.construction=1
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
'''
    #Add "Entity"
    entity_num = 0x40000
    for i, vlink in enumerate(VLinkList):
        if i==0:
            continue
        script_entity = Entity_line(script_entity, entity_num)
        for p in vlink.points:
            entity_num += 1
            point_num[p].append(entity_num)
            script_entity = Entity_point(script_entity, entity_num, VPointList[p].cx, VPointList[p].cy)
            line_num[i].append(entity_num)
        entity_num = up(entity_num, 4)
    script_entity += '''
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
Entity.construction=1
Entity.actVisible=1
AddEntity
'''
    #Add "Constraint"
    script_constraint = []
    constraint_num = 0x1
    #Same point constraint
    for p in point_num:
        for p_ in p[1:]:
            script_constraint.append(Constraint_point(constraint_num, p[0], p_))
            constraint_num += 1
    #Comment constraint
    for i, vpoint in enumerate(VPointList):
        script_constraint.append(Constraint_comment(constraint_num, 'VPointList{}'.format(i), vpoint.cx, vpoint.cy))
        constraint_num += 1
    #Position constraint
    for i, vpoint in enumerate(VPointList):
        if "ground" in vpoint.links and point_num[i]:
            script_constraint.append(Constraint_fix(script_constraint, constraint_num, point_num[i][0], vpoint.cx, vpoint.cy))
            constraint_num += 2
    #Distance constraint
    for i, l in enumerate(line_num):
        script_constraint.append(Constraint_line(script_constraint, constraint_num, l[0], l[1], VLinkList[i].len))
        constraint_num += 1
    #Write file
    with open(fileName, 'w', encoding="iso-8859-15", newline="") as f:
        f.write(script_group+script_param+script_request+script_entity+script_constraint)

def up(num, digit):
    ten = 0x10**digit
    num += ten
    num -= num%ten
    return num

def Param(script, num, val):
    script += '''
Param.h.v.={:08x}
Param.val={:.20f}
AddParam
'''.format(num, val)
    return script

def Request(script, num):
    script += '''
Request.h.v={:08x}
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest
'''.format(num)
    return script

def Entity_line(script, num):
    script += '''
Entity.h.v={0:08x}
Entity.type=11000
Entity.construction=0
Entity.point[0].v={1:08x}
Entity.point[1].v={2:08x}
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity
'''.format(num, num+1, num+2)
    return script

def Entity_point(script, num, x, y):
    script += '''
Entity.h.v={0:08x}
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x={1:.20f}
Entity.actPoint.y={2:.20f}
Entity.actVisible=1
AddEntity
'''.format(num, x, y)
    return script

def Constraint_point(num, p1, p2):
    return '''
Constraint.h.v={0:08x}
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v={1:08x}
Constraint.ptB.v={2:08x}
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
'''.format(num, p1, p2)

def Constraint_fix(num, p0, x, y):
    return Constraint_fix_hv(num, p0, 0x30000, y) + Constraint_fix_hv(num+1, p0, 0x20000, x)

def Constraint_fix_hv(num, p0, phv, val):
    return '''
Constraint.h.v={0:08x}
Constraint.type=31
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={3:.20f}
Constraint.ptA.v={1:08x}
Constraint.entityA.v={2:08x}
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x={4:.20f}
Constraint.disp.offset.y={4:.20f}
AddConstraint
'''.format(num, p0, phv, val, 10)

def Constraint_line(num, p1, p2, len):
    return '''
Constraint.h.v={0:08x}
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={3:.20f}
Constraint.ptA.v={1:08x}
Constraint.ptB.v={2:08x}
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x={4:.20f}
Constraint.disp.offset.y={4:.20f}
AddConstraint
'''.format(num, p1, p2, len, 10)

def Constraint_comment(num, comment, x, y):
    return '''
Constraint.h.v={0:08x}
Constraint.type=1000
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.comment={1}
Constraint.disp.offset.x={2:.20f}
Constraint.disp.offset.y={3:.20f}
AddConstraint
'''.format(num, comment, x, y)
