# -*- coding: utf-8 -*-

def slvsLink(length, width=8, thickness=5, drilling=6, joint=0, type=0):
    if type==0:
        return """±²³SolveSpaceREVa


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
Group.scale=1.00000000000000000000
Group.remap={{
}}
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
Group.scale=1.00000000000000000000
Group.remap={{
}}
AddGroup

Group.h.v=00000003
Group.type=5100
Group.order=2
Group.name=extrude
Group.opA.v=00000002
Group.color=00646464
Group.subtype=7000
Group.skipFirst=0
Group.predef.entityB.v=80020000
Group.predef.swapUV=0
Group.predef.negateU=0
Group.predef.negateV=0
Group.visible=1
Group.suppress=0
Group.relaxConstraints=0
Group.allowRedundant=0
Group.allDimsReference=0
Group.scale=1.00000000000000000000
Group.remap={{
}}
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

Param.h.v.=00040010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=00040011
Param.val=4.29620854689095210688
AddParam

Param.h.v.=00050010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=00050011
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=00060010
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00060011
Param.val=4.29620854689095210688
AddParam

Param.h.v.=00070010
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00070011
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=00080010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=00080011
Param.val=0.29620854689095227341
AddParam

Param.h.v.=00080013
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=00080014
Param.val=4.29620854689095210688
AddParam

Param.h.v.=00080016
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=00080017
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=00090010
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00090011
Param.val=0.29620854689095216239
AddParam

Param.h.v.=00090013
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00090014
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=00090016
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00090017
Param.val=4.29620854689095210688
AddParam

Param.h.v.=000a0010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=000a0011
Param.val=4.29620854689095210688
AddParam

Param.h.v.=000a0013
Param.val=25.00000000000000000000
AddParam

Param.h.v.=000a0014
Param.val=4.29620854689095210688
AddParam

Param.h.v.=000b0010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=000b0011
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=000b0013
Param.val=25.00000000000000000000
AddParam

Param.h.v.=000b0014
Param.val=-3.70379145310904789312
AddParam

Param.h.v.=000c0010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=000c0011
Param.val=0.29620854689095227341
AddParam

Param.h.v.=000c0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000d0010
Param.val=25.00000000000000000000
AddParam

Param.h.v.=000d0011
Param.val=0.29620854689095216239
AddParam

Param.h.v.=000d0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000e0010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=000e0011
Param.val=0.29620854689095227341
AddParam

Param.h.v.=000e0013
Param.val=25.00000000000000000000
AddParam

Param.h.v.=000e0014
Param.val=0.29620854689095216239
AddParam

Param.h.v.=000f0010
Param.val=-25.00000000000000000000
AddParam

Param.h.v.=000f0011
Param.val=0.29620854689095227341
AddParam

Param.h.v.=000f0040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=00100010
Param.val=25.00000000000000000000
AddParam

Param.h.v.=00100011
Param.val=0.29620854689095216239
AddParam

Param.h.v.=00100040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=80030000
AddParam

Param.h.v.=80030001
AddParam

Param.h.v.=80030002
Param.val=2.50000000000000000000
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

Request.h.v=00000004
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000005
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000006
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000007
Request.type=101
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000008
Request.type=500
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000009
Request.type=500
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000000a
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000000b
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000000c
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000000d
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000000e
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=0000000f
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000010
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
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

Entity.h.v=00040000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=00050000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=00060000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=00070000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=00080000
Entity.type=14000
Entity.construction=0
Entity.point[0].v=00080001
Entity.point[1].v=00080002
Entity.point[2].v=00080003
Entity.normal.v=00080020
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00080001
Entity.type=2001
Entity.construction=1
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=1
AddEntity

Entity.h.v=00080002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=00080003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=00080020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00080001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00090000
Entity.type=14000
Entity.construction=0
Entity.point[0].v=00090001
Entity.point[1].v=00090002
Entity.point[2].v=00090003
Entity.normal.v=00090020
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00090001
Entity.type=2001
Entity.construction=1
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=1
AddEntity

Entity.h.v=00090002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=00090003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=00090020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00090001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000a0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=000a0001
Entity.point[1].v=000a0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000a0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=000a0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=1
AddEntity

Entity.h.v=000b0000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=000b0001
Entity.point[1].v=000b0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000b0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=000b0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=1
AddEntity

Entity.h.v=000c0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=000c0001
Entity.normal.v=000c0020
Entity.distance.v=000c0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000c0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=1
AddEntity

Entity.h.v=000c0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=000c0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000c0040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000d0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=000d0001
Entity.normal.v=000d0020
Entity.distance.v=000d0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000d0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=1
AddEntity

Entity.h.v=000d0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=000d0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000d0040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000e0000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=000e0001
Entity.point[1].v=000e0002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000e0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=1
AddEntity

Entity.h.v=000e0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=1
AddEntity

Entity.h.v=000f0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=000f0001
Entity.normal.v=000f0020
Entity.distance.v=000f0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=000f0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=1
AddEntity

Entity.h.v=000f0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=000f0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000f0040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00100000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=00100001
Entity.normal.v=00100020
Entity.distance.v=00100040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00100001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=1
AddEntity

Entity.h.v=00100020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00100001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00100040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
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
Entity.construction=1
Entity.actVisible=1
AddEntity

Entity.h.v=80030001
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=80030004
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003000a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=8003000d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030013
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030014
Entity.point[1].v=80030015
Entity.point[2].v=80030016
Entity.normal.v=80030017
Entity.actVisible=0
AddEntity

Entity.h.v=80030014
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=0
AddEntity

Entity.h.v=80030015
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=80030016
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=80030017
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030014
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030018
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030019
Entity.point[1].v=8003001a
Entity.point[2].v=8003001b
Entity.normal.v=8003001c
Entity.actVisible=0
AddEntity

Entity.h.v=80030019
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003001a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003001b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003001c
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030019
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003001d
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030019
Entity.point[1].v=80030014
Entity.actVisible=0
AddEntity

Entity.h.v=8003001e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003001a
Entity.point[1].v=80030015
Entity.actVisible=0
AddEntity

Entity.h.v=8003001f
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003001b
Entity.point[1].v=80030016
Entity.actVisible=0
AddEntity

Entity.h.v=80030020
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030021
Entity.point[1].v=80030022
Entity.point[2].v=80030023
Entity.normal.v=80030024
Entity.actVisible=0
AddEntity

Entity.h.v=80030021
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=0
AddEntity

Entity.h.v=80030022
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=80030023
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=80030024
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030021
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030025
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030026
Entity.point[1].v=80030027
Entity.point[2].v=80030028
Entity.normal.v=80030029
Entity.actVisible=0
AddEntity

Entity.h.v=80030026
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030027
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030028
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030029
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030026
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003002a
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030026
Entity.point[1].v=80030021
Entity.actVisible=0
AddEntity

Entity.h.v=8003002b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030027
Entity.point[1].v=80030022
Entity.actVisible=0
AddEntity

Entity.h.v=8003002c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030028
Entity.point[1].v=80030023
Entity.actVisible=0
AddEntity

Entity.h.v=8003002d
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003002e
Entity.point[1].v=80030059
Entity.actVisible=0
AddEntity

Entity.h.v=8003002e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=80030031
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030032
Entity.point[1].v=8003005a
Entity.actVisible=0
AddEntity

Entity.h.v=80030032
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030035
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030032
Entity.point[1].v=8003002e
Entity.actVisible=0
AddEntity

Entity.h.v=80030036
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030037
Entity.point[1].v=8003005d
Entity.actVisible=0
AddEntity

Entity.h.v=80030037
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=8003003a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003003b
Entity.point[1].v=8003005e
Entity.actVisible=0
AddEntity

Entity.h.v=8003003b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003003e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003003b
Entity.point[1].v=80030037
Entity.actVisible=0
AddEntity

Entity.h.v=80030041
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030042
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030042
Entity.type=2010
Entity.construction=1
Entity.actVisible=0
AddEntity

Entity.h.v=80030043
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030044
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030044
Entity.type=2010
Entity.construction=1
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030045
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030044
Entity.point[1].v=80030042
Entity.actVisible=0
AddEntity

Entity.h.v=80030046
Entity.type=5000
Entity.construction=0
Entity.point[0].v=80030044
Entity.actPoint.z={2:.20f}
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030047
Entity.type=5000
Entity.construction=0
Entity.point[0].v=80030042
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030048
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030049
Entity.normal.v=80030061
Entity.distance.v=80030062
Entity.actVisible=0
AddEntity

Entity.h.v=80030049
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=0
AddEntity

Entity.h.v=8003004b
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003004c
Entity.normal.v=80030063
Entity.distance.v=80030064
Entity.actVisible=0
AddEntity

Entity.h.v=8003004c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003004f
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003004c
Entity.point[1].v=80030049
Entity.actVisible=0
AddEntity

Entity.h.v=80030051
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=80030052
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030053
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030052
Entity.point[1].v=80030051
Entity.actVisible=0
AddEntity

Entity.h.v=80030054
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030004
Entity.point[1].v=80030001
Entity.actVisible=0
AddEntity

Entity.h.v=80030055
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=80030056
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030057
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030056
Entity.point[1].v=80030055
Entity.actVisible=0
AddEntity

Entity.h.v=80030058
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003000d
Entity.point[1].v=8003000a
Entity.actVisible=0
AddEntity

Entity.h.v=80030059
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actVisible=0
AddEntity

Entity.h.v=8003005a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003005b
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=4.29620854689095210688
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003005c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003005a
Entity.point[1].v=80030059
Entity.actVisible=0
AddEntity

Entity.h.v=8003005d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actVisible=0
AddEntity

Entity.h.v=8003005e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003005f
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=-3.70379145310904789312
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030060
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003005e
Entity.point[1].v=8003005d
Entity.actVisible=0
AddEntity

Entity.h.v=80030061
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030049
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030062
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030063
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003004c
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030064
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030065
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030066
Entity.normal.v=80030067
Entity.distance.v=80030068
Entity.actVisible=0
AddEntity

Entity.h.v=80030066
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=0
AddEntity

Entity.h.v=80030067
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030066
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030068
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030069
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003006a
Entity.normal.v=8003006b
Entity.distance.v=8003006c
Entity.actVisible=0
AddEntity

Entity.h.v=8003006a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003006b
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003006a
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003006c
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003006d
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006a
Entity.point[1].v=80030066
Entity.actVisible=0
AddEntity

Entity.h.v=8003006e
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003006f
Entity.point[1].v=80030070
Entity.actVisible=0
AddEntity

Entity.h.v=8003006f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=0
AddEntity

Entity.h.v=80030070
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=0
AddEntity

Entity.h.v=80030071
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030072
Entity.point[1].v=80030073
Entity.actVisible=0
AddEntity

Entity.h.v=80030072
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030073
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=80030074
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actNormal.vx=0.00000000000000000222
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030075
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030072
Entity.point[1].v=8003006f
Entity.actVisible=0
AddEntity

Entity.h.v=80030076
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030073
Entity.point[1].v=80030070
Entity.actVisible=0
AddEntity

Entity.h.v=80030077
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030078
Entity.normal.v=80030080
Entity.distance.v=80030081
Entity.actVisible=0
AddEntity

Entity.h.v=80030078
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actVisible=0
AddEntity

Entity.h.v=8003007a
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003007b
Entity.normal.v=80030082
Entity.distance.v=80030083
Entity.actVisible=0
AddEntity

Entity.h.v=8003007b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-25.00000000000000000000
Entity.actPoint.y=0.29620854689095227341
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003007e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003007b
Entity.point[1].v=80030078
Entity.actVisible=0
AddEntity

Entity.h.v=80030080
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030078
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030081
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030082
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003007b
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030083
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030084
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030085
Entity.normal.v=80030086
Entity.distance.v=80030087
Entity.actVisible=0
AddEntity

Entity.h.v=80030085
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actVisible=0
AddEntity

Entity.h.v=80030086
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030085
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030087
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=80030088
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030089
Entity.normal.v=8003008a
Entity.distance.v=8003008b
Entity.actVisible=0
AddEntity

Entity.h.v=80030089
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.00000000000000000000
Entity.actPoint.y=0.29620854689095216239
Entity.actPoint.z={2:.20f}
Entity.actVisible=0
AddEntity

Entity.h.v=8003008a
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030089
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003008b
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=0
AddEntity

Entity.h.v=8003008c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030089
Entity.point[1].v=80030085
Entity.actVisible=0
AddEntity

Constraint.h.v=00000001
Constraint.type=61
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00040000
Constraint.ptB.v=00060000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000002
Constraint.type=61
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00050000
Constraint.ptB.v=00070000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000004
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00040000
Constraint.ptB.v=00080002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000005
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00050000
Constraint.ptB.v=00080003
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000006
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00070000
Constraint.ptB.v=00090002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000007
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00060000
Constraint.ptB.v=00090003
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000008
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00040000
Constraint.ptB.v=000a0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000000a
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00060000
Constraint.ptB.v=000a0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000000b
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00050000
Constraint.ptB.v=000b0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000000d
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00070000
Constraint.ptB.v=000b0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000000e
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=000c0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000000f
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=000d0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000010
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=000d0000
Constraint.entityB.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000013
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00090000
Constraint.entityB.v=000a0000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000015
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00080000
Constraint.entityB.v=000a0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000016
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=000e0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000017
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000e0002
Constraint.ptB.v=00090001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000019
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={3:.20f}
Constraint.entityA.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-5.09830810966708813936
Constraint.disp.offset.y=9.47880779284906793691
Constraint.disp.offset.z=-3.68020959143254078327
AddConstraint

Constraint.h.v=0000001a
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={1:.20f}
Constraint.entityA.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-8.94716488393469155938
Constraint.disp.offset.y=0.19736393126326531866
AddConstraint

Constraint.h.v=0000001b
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={0:.20f}
Constraint.ptA.v=000e0001
Constraint.ptB.v=000e0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=0.19736393126326531866
Constraint.disp.offset.y=9.40768072354897633147
AddConstraint

Constraint.h.v=0000001c
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00080000
Constraint.entityB.v=000b0000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001d
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=000f0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001e
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=00100001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001f
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={4:.20f}
Constraint.entityA.v=000f0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=3.12800519818063449407
Constraint.disp.offset.y=2.63807667316439253824
AddConstraint

Constraint.h.v=00000020
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00100000
Constraint.entityB.v=000f0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
""".format(length, width, thickness, drilling, joint)
