# -*- coding: utf-8 -*-

def slvs2D(Point, Line, Chain):
    point_num = [list() for i in range(len(Point))] #The number of same points.
    line_num = [list() for i in range(len(Line))] #The number of same lines.
    chain_num = [[list(), list(), list()] for i in range(len(Chain))] #The number of same chains.
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
    param_num = 0x40000
    for e in Line:
        param_num += 0x10
        for p in [e.start, e.end]:
            script_param = Param(script_param, param_num, Point[p].cx)
            param_num += 1
            script_param = Param(script_param, param_num, Point[p].cy)
            param_num += 2
        param_num = up(param_num, 4)
    for e in Chain:
        for k in [[e.p1, e.p2], [e.p2, e.p3], [e.p1, e.p3]]:
            param_num += 0x10
            for p in k:
                script_param = Param(script_param, param_num, Point[p].cx)
                param_num += 1
                script_param = Param(script_param, param_num, Point[p].cy)
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
    request_num = 0x4
    for e in Line:
        script_request = Request(script_request, request_num)
        request_num += 1
    for e in Chain:
        for i in range(3):
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
    entity_num = 0x40000
    for e in Line:
        script_entity = Entity_line(script_entity, entity_num)
        for p in [e.start, e.end]:
            entity_num += 1
            point_num[p].append(entity_num)
            script_entity = Entity_point(script_entity, entity_num, Point[p].cx, Point[p].cy)
            line_num[Line.index(e)].append(entity_num)
        entity_num = up(entity_num, 4)
    for e in Chain:
        band = [[e.p1, e.p2], [e.p2, e.p3], [e.p1, e.p3]]
        for k in band:
            script_entity = Entity_line(script_entity, entity_num)
            for p in k:
                entity_num += 1
                point_num[p].append(entity_num)
                script_entity = Entity_point(script_entity, entity_num, Point[p].cx, Point[p].cy)
                chain_num[Chain.index(e)][band.index(k)].append(entity_num)
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
    script_constraint = str()
    constraint_num = 0x1
    for e in point_num:
        for p in e[1:]:
            script_constraint = Constraint_point(script_constraint, constraint_num, e[0], p)
            constraint_num += 1
    for i, e in enumerate(Point):
        script_constraint = Constraint_comment(script_constraint, constraint_num, 'Point{}'.format(i), e.cx, e.cy)
        constraint_num += 1
    for i, e in enumerate(Point):
        if e.fix and point_num[Point.index(e)]:
            script_constraint = Constraint_fix(script_constraint, constraint_num, point_num[i][0], e.cx, e.cy)
            constraint_num += 2
    for e in line_num:
        script_constraint = Constraint_line(script_constraint, constraint_num, e[0], e[1], Line[line_num.index(e)].len)
        constraint_num += 1
    for i, e in enumerate(chain_num):
        band = [Chain[i].p1p2, Chain[i].p2p3, Chain[i].p1p3]
        for p in e:
            script_constraint = Constraint_line(script_constraint, constraint_num, p[0], p[1], band[e.index(p)])
            constraint_num += 1
    return script_group+script_param+script_request+script_entity+script_constraint

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

def Constraint_point(script, num, p1, p2):
    script += '''
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
    return script

def Constraint_fix(script, num, p0, x, y):
    script = Constraint_fix_hv(script, num, p0, 0x30000, y)
    script = Constraint_fix_hv(script, num+1, p0, 0x20000, x)
    return script

def Constraint_fix_hv(script, num, p0, phv, val):
    script += '''
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
    return script

def Constraint_line(script, num, p1, p2, len):
    script += '''
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
    return script

def Constraint_comment(script, num, comment, x, y):
    script += '''
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
    return script
