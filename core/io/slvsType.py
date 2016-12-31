# -*- coding: utf-8 -*-
from copy import copy, deepcopy

def SLVS_Code(point, line, chain, slider, rod):
    Param_num = 0x30023
    Request_num = 0x3
    Entity_num = 0x30020
    Constraint_num = 0x0
    Slvs_code = """±²³SolveSpaceREVa


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
    #TODO: SlvsFile
    #Find independent Points
    samePoints = [list() for e in point]
    independentPoints = list(range(len(point)))
    for e in line:
        try:
            independentPoints.remove(e['start'])
            independentPoints.remove(e['end'])
        except ValueError: pass
    for e in chain:
        try:
            independentPoints.remove(e['p1'])
            independentPoints.remove(e['p2'])
            independentPoints.remove(e['p3'])
        except ValueError: pass
    #Param
    for e in line:
        next(Param_num)
        Param_num+=0x10
        Param(Slvs_code, Param_num, point[e['start']]['cx'])
        Param_num+=0x1
        Param(Slvs_code, Param_num, point[e['start']]['cy'])
        Param_num+=0x2
        Param(Slvs_code, Param_num, point[e['end']]['cx'])
        Param_num+=0x1
        Param(Slvs_code, Param_num, point[e['end']]['cy'])
    for e in chain:
        num = ['p1', 'p2', 'p3']
        for k in range(len(num)):
            next(Param_num)
            Param_num+=0x10
            Param(Slvs_code, Param_num, point[e[num[k]]]['cx'])
            Param_num+=0x1
            Param(Slvs_code, Param_num, point[e[num[k]]]['cy'])
            Param_num+=0x2
            Param(Slvs_code, Param_num, point[e[num[k+1 if k<len(num)-1 else 0]]]['cx'])
            Param_num+=0x1
            Param(Slvs_code, Param_num, point[e[num[k+1 if k<len(num)-1 else 0]]]['cy'])
    for e in independentPoints:
        next(Param_num)
        Param_num+=0x10
        Param(Slvs_code, Param_num, point[e]['cx'])
        Param_num+=0x1
        Param(Slvs_code, Param_num, point[e]['cy'])
    #Request
    for e in line:
        Request_num+=0x1
        Request(Slvs_code, Request_num, 200)
    for e in chain:
        for k in range(3):
            Request_num+=0x1
            Request(Slvs_code, Request_num, 200)
    for e in independentPoints:
        Request_num+=0x1
        Request(Slvs_code, Request_num, 101)
    #Entity
    for e in line:
        next(Entity_num)
        Entity(Slvs_code, Entity_num, 1100, point[e['start']]['cx'], point[e['start']]['cy'], point[e['end']]['cx'], point[e['end']]['cy'])
    for e in chain:
        num = ['p1', 'p2', 'p3']
        for k in range(len(num)):
            next(Entity_num)
            Entity(Slvs_code, Entity_num, 1100, point[e[num[k]]]['cx'], point[e[num[k]]]['cy'], point[e[num[k+1 if k<len(num)-1 else 0]]]['cx'], point[e[num[k+1 if k<len(num)-1 else 0]]]['cy'])
    for e in independentPoints:
        next(Entity_num)
        Entity(Slvs_code, Entity_num, 2001, point[e]['cx'], point[e]['cy'])
    #Constraint
    
    #Answer
    Slvs_code+="\n\n"
    print(Slvs_code)
    return Slvs_code

def next(num):
    num -= num%0x10000
    num += 0x10000

def Param(code, num, val):
    code+="Param.h.v.=%08x\n"%num
    if val!=0: code+="Param.val=%.20f\n"%val
    code+="AddParam\n"
    code+="\n"

def Request(code, num, type):
    code+="Request.h.v=%08x\n"%num
    code+="Request.type=%i\n"%type
    code+="Request.workplane.v=80020000\n"
    code+="Request.group.v=00000002\n"
    code+="Request.construction=0\n"
    code+="AddRequest\n"
    code+="\n"

def Entity(code, num, type, val1, val2, val3=0.0, val4=0.0):
    code+="Entity.h.v=%08x\n"%num
    code+="Entity.type=%08x\n"%type
    code+="Entity.construction=0\n"
    code+="Entity.workplane.v=80020000\n"
    if type==1100:
        code+="Entity.point[0].v=%08x\n"%(num+1)
        code+="Entity.point[1].v=%08x\n"%(num+2)
        code+="\n"
        num+=0x1
        code+="Entity.h.v=%08x\n"%num
        code+="Entity.type=%08x\n"%2001
        code+="Entity.construction=0\n"
        code+="Entity.workplane.v=80020000\n"
        code+="Entity.actPoint.x=%.20f"%val1
        code+="Entity.actPoint.y=%.20f"%val2
        code+="Entity.workplane.v=80020000\n"
        code+="Entity.actVisible=1\n"
        code+="AddEntity\n"
        code+="\n"
        num+=0x1
        code+="Entity.h.v=%08x\n"%num
        code+="Entity.type=%08x\n"%2001
        code+="Entity.construction=0\n"
        code+="Entity.workplane.v=80020000\n"
        code+="Entity.actPoint.x=%.20f"%val3
        code+="Entity.actPoint.y=%.20f"%val4
        code+="Entity.workplane.v=80020000\n"
        code+="Entity.actVisible=1\n"
        code+="AddEntity\n"
        code+="\n"
    elif type==2001:
        code+="Entity.actPoint.x=%.20f"%val1
        code+="Entity.actPoint.y=%.20f"%val2
    else: raise ValueError
    code+="Entity.actVisible=1\n"
    code+="AddEntity\n"
    code+="\n"
