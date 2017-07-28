# -*- coding: utf-8 -*-

def slvsChain(length1, length2, length3, width=8, thickness=5, drilling=6, joint=0, type=0):
    if type==0:
        return"""±²³SolveSpaceREVa


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
    1 00050000 1002
    2 00050001 1002
    3 00050002 1002
    4 00050000 1001
    5 00050001 1001
    6 00050002 1001
    7 00050000 1004
    8 00050001 1003
    9 00050002 1003
    10 00070000 1002
    11 00070001 1002
    12 00070002 1002
    13 00070000 1001
    14 00070001 1001
    15 00070002 1001
    16 00070000 1004
    17 00070001 1003
    18 00070002 1003
    19 00080000 1002
    20 00080001 1002
    21 00080002 1002
    22 00080003 1002
    23 00080020 1002
    24 00080000 1001
    25 00080001 1001
    26 00080002 1001
    27 00080003 1001
    28 00080020 1001
    29 00080001 1003
    30 00080002 1003
    31 00080003 1003
    32 00090000 1002
    33 00090001 1002
    34 00090002 1002
    35 00090003 1002
    36 00090020 1002
    37 00090000 1001
    38 00090001 1001
    39 00090002 1001
    40 00090003 1001
    41 00090020 1001
    42 00090001 1003
    43 00090002 1003
    44 00090003 1003
    45 000a0000 1002
    46 000a0001 1002
    47 000a0020 1002
    48 000a0040 1002
    49 000a0000 1001
    50 000a0001 1001
    51 000a0020 1001
    52 000a0040 1001
    53 000a0001 1003
    54 000b0000 1002
    55 000b0001 1002
    56 000b0020 1002
    57 000b0040 1002
    58 000b0000 1001
    59 000b0001 1001
    60 000b0020 1001
    61 000b0040 1001
    62 000b0001 1003
    63 80020000 1002
    64 80020000 1001
    65 80020001 1002
    66 80020002 1002
    67 80020001 1001
    68 80020002 1001
    69 80020002 1003
    70 00000000 1001
    71 00000000 1002
    72 000c0000 1002
    73 000c0001 1002
    74 000c0002 1002
    75 000c0000 1001
    76 000c0001 1001
    77 000c0002 1001
    78 000c0000 1004
    79 000c0001 1003
    80 000c0002 1003
    81 00040000 1002
    82 00040000 1001
    83 00040000 1003
    84 00050000 1003
    85 00060000 1002
    86 00060000 1001
    87 00060000 1003
    88 00070000 1003
    89 000a0002 1002
    90 000a0002 1001
    91 000a0000 1004
    92 000a0002 1003
    93 000b0002 1002
    94 000b0002 1001
    95 000b0000 1004
    96 000b0002 1003
    97 000c0020 1002
    98 000c0040 1002
    99 000c0020 1001
    100 000c0040 1001
    101 000d0000 1002
    102 000d0001 1002
    103 000d0020 1002
    104 000d0040 1002
    105 000d0000 1001
    106 000d0001 1001
    107 000d0020 1001
    108 000d0040 1001
    109 000d0001 1003
    110 000e0000 1002
    111 000e0001 1002
    112 000e0002 1002
    113 000e0000 1001
    114 000e0001 1001
    115 000e0002 1001
    116 000e0000 1004
    117 000e0001 1003
    118 000e0002 1003
    119 000f0000 1002
    120 000f0001 1002
    121 000f0002 1002
    122 000f0000 1001
    123 000f0001 1001
    124 000f0002 1001
    125 000f0000 1004
    126 000f0001 1003
    127 000f0002 1003
    128 000f0020 1002
    129 000f0040 1002
    130 000f0020 1001
    131 000f0040 1001
    132 00100000 1002
    133 00100001 1002
    134 00100002 1002
    135 00100000 1001
    136 00100001 1001
    137 00100002 1001
    138 00100000 1004
    139 00100001 1003
    140 00100002 1003
    141 00110000 1002
    142 00110001 1002
    143 00110002 1002
    144 00110000 1001
    145 00110001 1001
    146 00110002 1001
    147 00110000 1004
    148 00110001 1003
    149 00110002 1003
    150 00120000 1002
    151 00120001 1002
    152 00120002 1002
    153 00120003 1002
    154 00120020 1002
    155 00120000 1001
    156 00120001 1001
    157 00120002 1001
    158 00120003 1001
    159 00120020 1001
    160 00120001 1003
    161 00120002 1003
    162 00120003 1003
    163 00130000 1002
    164 00130001 1002
    165 00130002 1002
    166 00130000 1001
    167 00130001 1001
    168 00130002 1001
    169 00130000 1004
    170 00130001 1003
    171 00130002 1003
    172 00140000 1002
    173 00140001 1002
    174 00140002 1002
    175 00140000 1001
    176 00140001 1001
    177 00140002 1001
    178 00140000 1004
    179 00140001 1003
    180 00140002 1003
    181 00150000 1002
    182 00150001 1002
    183 00150020 1002
    184 00150040 1002
    185 00150000 1001
    186 00150001 1001
    187 00150020 1001
    188 00150040 1001
    189 00150001 1003
    190 00160000 1002
    191 00160001 1002
    192 00160020 1002
    193 00160040 1002
    194 00160000 1001
    195 00160001 1001
    196 00160020 1001
    197 00160040 1001
    198 00160001 1003
    199 00170000 1002
    200 00170001 1002
    201 00170020 1002
    202 00170040 1002
    203 00170000 1001
    204 00170001 1001
    205 00170020 1001
    206 00170040 1001
    207 00170001 1003
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
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=00040011
Param.val=6.74450749427472739939
AddParam

Param.h.v.=00050010
Param.val=-19.70634229120273772651
AddParam

Param.h.v.=00050011
Param.val=2.48417038524008404465
AddParam

Param.h.v.=00060010
Param.val=25.78517679176048460477
AddParam

Param.h.v.=00060011
Param.val=6.74450749427472739939
AddParam

Param.h.v.=00070010
Param.val=28.65363405388995943213
AddParam

Param.h.v.=00070011
Param.val=-0.04331476249428499459
AddParam

Param.h.v.=00080010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=00080011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00080013
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=00080014
Param.val=6.74450749427472739939
AddParam

Param.h.v.=00080016
Param.val=-19.70634229120273772651
AddParam

Param.h.v.=00080017
Param.val=2.48417038524008404465
AddParam

Param.h.v.=00090010
Param.val=25.78517679176048460477
AddParam

Param.h.v.=00090011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00090013
Param.val=28.65363405388995943213
AddParam

Param.h.v.=00090014
Param.val=-0.04331476249428499459
AddParam

Param.h.v.=00090016
Param.val=25.78517679176048460477
AddParam

Param.h.v.=00090017
Param.val=6.74450749427472739939
AddParam

Param.h.v.=000a0010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=000a0011
Param.val=6.74450749427472739939
AddParam

Param.h.v.=000a0013
Param.val=25.78517679176048460477
AddParam

Param.h.v.=000a0014
Param.val=6.74450749427472739939
AddParam

Param.h.v.=000c0010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=000c0011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=000c0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000d0010
Param.val=25.78517679176048460477
AddParam

Param.h.v.=000d0011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=000d0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000e0010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=000e0011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=000e0013
Param.val=25.78517679176048460477
AddParam

Param.h.v.=000e0014
Param.val=2.74450749427472695530
AddParam

Param.h.v.=000f0010
Param.val=-13.10494369016723048560
AddParam

Param.h.v.=000f0011
Param.val=-37.27047131243146793622
AddParam

Param.h.v.=000f0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=00100010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=00100011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00100013
Param.val=-13.10494369016723048560
AddParam

Param.h.v.=00100014
Param.val=-37.27047131243146793622
AddParam

Param.h.v.=00110010
Param.val=-13.10494369016723048560
AddParam

Param.h.v.=00110011
Param.val=-37.27047131243146793622
AddParam

Param.h.v.=00110013
Param.val=25.78517679176048460477
AddParam

Param.h.v.=00110014
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00120010
Param.val=-13.10494369016723048560
AddParam

Param.h.v.=00120011
Param.val=-37.27047131243146793622
AddParam

Param.h.v.=00120013
Param.val=-17.09646277313044393509
AddParam

Param.h.v.=00120014
Param.val=-37.53080842146611217913
AddParam

Param.h.v.=00120016
Param.val=-10.23648642803775388188
AddParam

Param.h.v.=00120017
Param.val=-40.05829356920047956692
AddParam

Param.h.v.=00130010
Param.val=-19.70634229120273772651
AddParam

Param.h.v.=00130011
Param.val=2.48417038524008404465
AddParam

Param.h.v.=00130013
Param.val=-17.09646277313044393509
AddParam

Param.h.v.=00130014
Param.val=-37.53080842146611217913
AddParam

Param.h.v.=00140010
Param.val=-10.23648642803775388188
AddParam

Param.h.v.=00140011
Param.val=-40.05829356920047956692
AddParam

Param.h.v.=00140013
Param.val=28.65363405388995943213
AddParam

Param.h.v.=00140014
Param.val=-0.04331476249428499459
AddParam

Param.h.v.=00150010
Param.val=-15.71482320823952427702
AddParam

Param.h.v.=00150011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00150040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=00160010
Param.val=25.78517679176048460477
AddParam

Param.h.v.=00160011
Param.val=2.74450749427472695530
AddParam

Param.h.v.=00160040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=00170010
Param.val=-13.10494369016723048560
AddParam

Param.h.v.=00170011
Param.val=-37.27047131243146793622
AddParam

Param.h.v.=00170040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=80030000
AddParam

Param.h.v.=80030001
AddParam

Param.h.v.=80030002
Param.val=-2.50000000000000000000
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
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=00000011
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=00000012
Request.type=500
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000013
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000014
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000015
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000016
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000017
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
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=00050000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actVisible=1
AddEntity

Entity.h.v=00060000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=00070000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
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
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00080002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=00080003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
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
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00090002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actVisible=1
AddEntity

Entity.h.v=00090003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
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
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=000a0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
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
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
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
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
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
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=000e0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
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
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
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
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00100000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00100001
Entity.point[1].v=00100002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00100001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00100002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=00110000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00110001
Entity.point[1].v=00110002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00110001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=00110002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00120000
Entity.type=14000
Entity.construction=0
Entity.point[0].v=00120001
Entity.point[1].v=00120002
Entity.point[2].v=00120003
Entity.normal.v=00120020
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00120001
Entity.type=2001
Entity.construction=1
Entity.workplane.v=80020000
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=00120002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actVisible=1
AddEntity

Entity.h.v=00120003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actVisible=1
AddEntity

Entity.h.v=00120020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00120001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00130000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=00130001
Entity.point[1].v=00130002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00130001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actVisible=1
AddEntity

Entity.h.v=00130002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actVisible=1
AddEntity

Entity.h.v=00140000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=00140001
Entity.point[1].v=00140002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00140001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actVisible=1
AddEntity

Entity.h.v=00140002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actVisible=1
AddEntity

Entity.h.v=00150000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=00150001
Entity.normal.v=00150020
Entity.distance.v=00150040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00150001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00150020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00150001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00150040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00160000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=00160001
Entity.normal.v=00160020
Entity.distance.v=00160040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00160001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=00160020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00160001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00160040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00170000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=00170001
Entity.normal.v=00170020
Entity.distance.v=00170040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00170001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=00170020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00170001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00170040
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
Entity.actVisible=0
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
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actVisible=1
AddEntity

Entity.h.v=80030004
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003000a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actVisible=1
AddEntity

Entity.h.v=8003000d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030013
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030014
Entity.point[1].v=80030015
Entity.point[2].v=80030016
Entity.normal.v=80030017
Entity.actVisible=1
AddEntity

Entity.h.v=80030014
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030015
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=80030016
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actVisible=1
AddEntity

Entity.h.v=80030017
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030014
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030018
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030019
Entity.point[1].v=8003001a
Entity.point[2].v=8003001b
Entity.normal.v=8003001c
Entity.actVisible=1
AddEntity

Entity.h.v=80030019
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001c
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030019
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001d
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030019
Entity.point[1].v=80030014
Entity.actVisible=1
AddEntity

Entity.h.v=8003001e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003001a
Entity.point[1].v=80030015
Entity.actVisible=1
AddEntity

Entity.h.v=8003001f
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003001b
Entity.point[1].v=80030016
Entity.actVisible=1
AddEntity

Entity.h.v=80030020
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030021
Entity.point[1].v=80030022
Entity.point[2].v=80030023
Entity.normal.v=80030024
Entity.actVisible=1
AddEntity

Entity.h.v=80030021
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030022
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actVisible=1
AddEntity

Entity.h.v=80030023
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=80030024
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030021
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030025
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030026
Entity.point[1].v=80030027
Entity.point[2].v=80030028
Entity.normal.v=80030029
Entity.actVisible=1
AddEntity

Entity.h.v=80030026
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030027
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030028
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030029
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030026
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003002a
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030026
Entity.point[1].v=80030021
Entity.actVisible=1
AddEntity

Entity.h.v=8003002b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030027
Entity.point[1].v=80030022
Entity.actVisible=1
AddEntity

Entity.h.v=8003002c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030028
Entity.point[1].v=80030023
Entity.actVisible=1
AddEntity

Entity.h.v=8003002d
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003002e
Entity.point[1].v=80030059
Entity.actVisible=1
AddEntity

Entity.h.v=8003002e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=80030031
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030032
Entity.point[1].v=8003005a
Entity.actVisible=1
AddEntity

Entity.h.v=80030032
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030035
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030032
Entity.point[1].v=8003002e
Entity.actVisible=1
AddEntity

Entity.h.v=80030041
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030042
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030042
Entity.type=2010
Entity.construction=1
Entity.actVisible=1
AddEntity

Entity.h.v=80030043
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030044
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030044
Entity.type=2010
Entity.construction=1
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030045
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030044
Entity.point[1].v=80030042
Entity.actVisible=1
AddEntity

Entity.h.v=80030046
Entity.type=5000
Entity.construction=0
Entity.point[0].v=80030044
Entity.actPoint.z=-5.00000000000000000000
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030047
Entity.type=5000
Entity.construction=0
Entity.point[0].v=80030042
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030048
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030049
Entity.normal.v=80030061
Entity.distance.v=80030062
Entity.actVisible=1
AddEntity

Entity.h.v=80030049
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=8003004b
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003004c
Entity.normal.v=80030063
Entity.distance.v=80030064
Entity.actVisible=1
AddEntity

Entity.h.v=8003004c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003004f
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003004c
Entity.point[1].v=80030049
Entity.actVisible=1
AddEntity

Entity.h.v=80030051
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=80030052
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030053
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030052
Entity.point[1].v=80030051
Entity.actVisible=1
AddEntity

Entity.h.v=80030054
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030004
Entity.point[1].v=80030001
Entity.actVisible=1
AddEntity

Entity.h.v=80030055
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=80030056
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030057
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030056
Entity.point[1].v=80030055
Entity.actVisible=1
AddEntity

Entity.h.v=80030058
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003000d
Entity.point[1].v=8003000a
Entity.actVisible=1
AddEntity

Entity.h.v=80030059
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actVisible=1
AddEntity

Entity.h.v=8003005a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=6.74450749427472739939
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003005b
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=6.74450749427472739939
Entity.actNormal.vy=-1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003005c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003005a
Entity.point[1].v=80030059
Entity.actVisible=1
AddEntity

Entity.h.v=80030061
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030049
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030062
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030063
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003004c
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030064
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030065
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030066
Entity.normal.v=80030067
Entity.distance.v=80030068
Entity.actVisible=1
AddEntity

Entity.h.v=80030066
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030067
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030066
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030068
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030069
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003006a
Entity.normal.v=8003006b
Entity.distance.v=8003006c
Entity.actVisible=1
AddEntity

Entity.h.v=8003006a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003006b
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003006a
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003006c
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003006d
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006a
Entity.point[1].v=80030066
Entity.actVisible=1
AddEntity

Entity.h.v=8003006e
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003006f
Entity.point[1].v=80030070
Entity.actVisible=1
AddEntity

Entity.h.v=8003006f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030070
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030071
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030072
Entity.point[1].v=80030073
Entity.actVisible=1
AddEntity

Entity.h.v=80030072
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030073
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030074
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actNormal.vy=-1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030075
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030072
Entity.point[1].v=8003006f
Entity.actVisible=1
AddEntity

Entity.h.v=80030076
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030073
Entity.point[1].v=80030070
Entity.actVisible=1
AddEntity

Entity.h.v=80030077
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030078
Entity.normal.v=80030080
Entity.distance.v=80030081
Entity.actVisible=1
AddEntity

Entity.h.v=80030078
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=8003007a
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003007b
Entity.normal.v=80030082
Entity.distance.v=80030083
Entity.actVisible=1
AddEntity

Entity.h.v=8003007b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003007e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003007b
Entity.point[1].v=80030078
Entity.actVisible=1
AddEntity

Entity.h.v=80030080
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030078
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030081
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030082
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003007b
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030083
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030084
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030085
Entity.point[1].v=80030086
Entity.actVisible=1
AddEntity

Entity.h.v=80030085
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030086
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=80030087
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030088
Entity.point[1].v=80030089
Entity.actVisible=1
AddEntity

Entity.h.v=80030088
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030089
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008a
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actNormal.vx=-0.99787977074080314033
Entity.actNormal.vy=-0.06508427725866069991
Entity.actVisible=1
AddEntity

Entity.h.v=8003008b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030088
Entity.point[1].v=80030085
Entity.actVisible=1
AddEntity

Entity.h.v=8003008c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030089
Entity.point[1].v=80030086
Entity.actVisible=1
AddEntity

Entity.h.v=8003008d
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003008e
Entity.point[1].v=8003008f
Entity.actVisible=1
AddEntity

Entity.h.v=8003008e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=8003008f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=80030090
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030091
Entity.point[1].v=80030092
Entity.actVisible=1
AddEntity

Entity.h.v=80030091
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030092
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030093
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actNormal.vx=0.71711431553236915093
Entity.actNormal.vy=-0.69695556419225301870
Entity.actVisible=1
AddEntity

Entity.h.v=80030094
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030091
Entity.point[1].v=8003008e
Entity.actVisible=1
AddEntity

Entity.h.v=80030095
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030092
Entity.point[1].v=8003008f
Entity.actVisible=1
AddEntity

Entity.h.v=80030096
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030097
Entity.point[1].v=80030098
Entity.point[2].v=80030099
Entity.normal.v=8003009a
Entity.actVisible=1
AddEntity

Entity.h.v=80030097
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=80030098
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actVisible=1
AddEntity

Entity.h.v=80030099
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actVisible=1
AddEntity

Entity.h.v=8003009a
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030097
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003009b
Entity.type=14000
Entity.construction=0
Entity.point[0].v=8003009c
Entity.point[1].v=8003009d
Entity.point[2].v=8003009e
Entity.normal.v=8003009f
Entity.actVisible=1
AddEntity

Entity.h.v=8003009c
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003009d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003009e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003009f
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003009c
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a0
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003009c
Entity.point[1].v=80030097
Entity.actVisible=1
AddEntity

Entity.h.v=800300a1
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003009d
Entity.point[1].v=80030098
Entity.actVisible=1
AddEntity

Entity.h.v=800300a2
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003009e
Entity.point[1].v=80030099
Entity.actVisible=1
AddEntity

Entity.h.v=800300a3
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a4
Entity.point[1].v=800300a5
Entity.actVisible=1
AddEntity

Entity.h.v=800300a4
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actVisible=1
AddEntity

Entity.h.v=800300a5
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actVisible=1
AddEntity

Entity.h.v=800300a6
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a7
Entity.point[1].v=800300a8
Entity.actVisible=1
AddEntity

Entity.h.v=800300a7
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a8
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-17.09646277313044393509
Entity.actPoint.y=-37.53080842146611217913
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a9
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-19.70634229120273772651
Entity.actPoint.y=2.48417038524008404465
Entity.actNormal.vx=-0.99787977074080314033
Entity.actNormal.vy=-0.06508427725866069991
Entity.actVisible=1
AddEntity

Entity.h.v=800300aa
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a7
Entity.point[1].v=800300a4
Entity.actVisible=1
AddEntity

Entity.h.v=800300ab
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a8
Entity.point[1].v=800300a5
Entity.actVisible=1
AddEntity

Entity.h.v=800300ac
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300ad
Entity.point[1].v=800300ae
Entity.actVisible=1
AddEntity

Entity.h.v=800300ad
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actVisible=1
AddEntity

Entity.h.v=800300ae
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actVisible=1
AddEntity

Entity.h.v=800300af
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300b0
Entity.point[1].v=800300b1
Entity.actVisible=1
AddEntity

Entity.h.v=800300b0
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b1
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=28.65363405388995943213
Entity.actPoint.y=-0.04331476249428499459
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b2
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-10.23648642803775388188
Entity.actPoint.y=-40.05829356920047956692
Entity.actNormal.vx=0.71711431553236915093
Entity.actNormal.vy=-0.69695556419225290767
Entity.actVisible=1
AddEntity

Entity.h.v=800300b3
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300b0
Entity.point[1].v=800300ad
Entity.actVisible=1
AddEntity

Entity.h.v=800300b4
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300b1
Entity.point[1].v=800300ae
Entity.actVisible=1
AddEntity

Entity.h.v=800300b5
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300b6
Entity.normal.v=800300b7
Entity.distance.v=800300b8
Entity.actVisible=1
AddEntity

Entity.h.v=800300b6
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=800300b7
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300b6
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b8
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b9
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300ba
Entity.normal.v=800300bb
Entity.distance.v=800300bc
Entity.actVisible=1
AddEntity

Entity.h.v=800300ba
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-15.71482320823952427702
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300bb
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300ba
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300bc
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300bd
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300ba
Entity.point[1].v=800300b6
Entity.actVisible=1
AddEntity

Entity.h.v=800300be
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300bf
Entity.normal.v=800300c0
Entity.distance.v=800300c1
Entity.actVisible=1
AddEntity

Entity.h.v=800300bf
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actVisible=1
AddEntity

Entity.h.v=800300c0
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300bf
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c1
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c2
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300c3
Entity.normal.v=800300c4
Entity.distance.v=800300c5
Entity.actVisible=1
AddEntity

Entity.h.v=800300c3
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=25.78517679176048460477
Entity.actPoint.y=2.74450749427472695530
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c4
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300c3
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c5
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c6
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300c3
Entity.point[1].v=800300bf
Entity.actVisible=1
AddEntity

Entity.h.v=800300c7
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300c8
Entity.normal.v=800300c9
Entity.distance.v=800300ca
Entity.actVisible=1
AddEntity

Entity.h.v=800300c8
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actVisible=1
AddEntity

Entity.h.v=800300c9
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300c8
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300ca
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300cb
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300cc
Entity.normal.v=800300cd
Entity.distance.v=800300ce
Entity.actVisible=1
AddEntity

Entity.h.v=800300cc
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-13.10494369016723048560
Entity.actPoint.y=-37.27047131243146793622
Entity.actPoint.z=-5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300cd
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300cc
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300ce
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300cf
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300cc
Entity.point[1].v=800300c8
Entity.actVisible=1
AddEntity

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

Constraint.h.v=00000009
Constraint.type=80
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=000a0000
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
Constraint.valA={5:.20f}
Constraint.entityA.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-9.01890181250750622155
Constraint.disp.offset.y=11.04383810660871567677
Constraint.disp.offset.z=-3.68020959143254078327
AddConstraint

Constraint.h.v=0000001a
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=000f0000
Constraint.entityB.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001b
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=00100001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001c
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=00100002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001d
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=00110001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001e
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=00110002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000021
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120001
Constraint.ptB.v=000f0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000022
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00050000
Constraint.ptB.v=00130001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000023
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120002
Constraint.ptB.v=00130002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000024
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120003
Constraint.ptB.v=00140001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000025
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00070000
Constraint.ptB.v=00140002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000027
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00140000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000028
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00090000
Constraint.entityB.v=00140000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000029
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00080000
Constraint.entityB.v=00130000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002a
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00130000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002b
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={3:.20f}
Constraint.entityA.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-3.32058710682528834823
Constraint.disp.offset.y=16.11409832259986885106
AddConstraint

Constraint.h.v=0000002c
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00090000
Constraint.entityB.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002d
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002e
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={2:.20f}
Constraint.ptA.v=00110001
Constraint.ptB.v=00110002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-5.32859227014708825010
Constraint.disp.offset.y=-0.28026317408186379732
AddConstraint

Constraint.h.v=0000002f
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={1:.20f}
Constraint.ptA.v=000e0001
Constraint.ptB.v=000e0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=0.78731741997557069812
Constraint.disp.offset.y=-4.33024580986564622265
AddConstraint

Constraint.h.v=00000030
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={0:.20f}
Constraint.ptA.v=00100001
Constraint.ptB.v=00100002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=4.83275228128854550391
Constraint.disp.offset.y=0.86071372213670971352
AddConstraint

Constraint.h.v=00000031
Constraint.type=30
Constraint.group.v=00000003
Constraint.valA={4:.20f}
Constraint.ptA.v=80030027
Constraint.ptB.v=80030022
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=3.22796824770711721087
Constraint.disp.offset.y=-0.53331959218224300745
Constraint.disp.offset.z=0.00000000000000000312
AddConstraint

Constraint.h.v=00000032
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=00150001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000033
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=00160001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000034
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=00170001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000035
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={6:.20f}
Constraint.entityA.v=00150000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-8.46993744303738083090
Constraint.disp.offset.y=-3.54354525678094534058
AddConstraint

Constraint.h.v=00000036
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00150000
Constraint.entityB.v=00160000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000037
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00170000
Constraint.entityB.v=00150000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint
""".format(length1, length2, length3, width, thickness, drilling, joint)
    elif type==1:
        return"""±²³SolveSpaceREVa


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
    1 00040000 1002
    2 00040000 1001
    3 00040000 1003
    4 00050000 1002
    5 00050000 1001
    6 00050000 1003
    7 00060000 1002
    8 00060000 1001
    9 00060000 1003
    10 00070000 1002
    11 00070000 1001
    12 00070000 1003
    13 00080000 1002
    14 00080001 1002
    15 00080002 1002
    16 00080003 1002
    17 00080020 1002
    18 00080000 1001
    19 00080001 1001
    20 00080002 1001
    21 00080003 1001
    22 00080020 1001
    23 00080001 1003
    24 00080002 1003
    25 00080003 1003
    26 00090000 1002
    27 00090001 1002
    28 00090002 1002
    29 00090003 1002
    30 00090020 1002
    31 00090000 1001
    32 00090001 1001
    33 00090002 1001
    34 00090003 1001
    35 00090020 1001
    36 00090001 1003
    37 00090002 1003
    38 00090003 1003
    39 000a0000 1002
    40 000a0001 1002
    41 000a0002 1002
    42 000a0000 1001
    43 000a0001 1001
    44 000a0002 1001
    45 000a0000 1004
    46 000a0001 1003
    47 000a0002 1003
    48 000c0000 1002
    49 000c0001 1002
    50 000c0020 1002
    51 000c0040 1002
    52 000c0000 1001
    53 000c0001 1001
    54 000c0020 1001
    55 000c0040 1001
    56 000c0001 1003
    57 000d0000 1002
    58 000d0001 1002
    59 000d0020 1002
    60 000d0040 1002
    61 000d0000 1001
    62 000d0001 1001
    63 000d0020 1001
    64 000d0040 1001
    65 000d0001 1003
    66 000e0000 1002
    67 000e0001 1002
    68 000e0002 1002
    69 000e0000 1001
    70 000e0001 1001
    71 000e0002 1001
    72 000e0000 1004
    73 000e0001 1003
    74 000e0002 1003
    75 000f0000 1002
    76 000f0001 1002
    77 000f0020 1002
    78 000f0040 1002
    79 000f0000 1001
    80 000f0001 1001
    81 000f0020 1001
    82 000f0040 1001
    83 000f0001 1003
    84 00100000 1002
    85 00100001 1002
    86 00100002 1002
    87 00100000 1001
    88 00100001 1001
    89 00100002 1001
    90 00100000 1004
    91 00100001 1003
    92 00100002 1003
    93 00120000 1002
    94 00120001 1002
    95 00120002 1002
    96 00120003 1002
    97 00120020 1002
    98 00120000 1001
    99 00120001 1001
    100 00120002 1001
    101 00120003 1001
    102 00120020 1001
    103 00120001 1003
    104 00120002 1003
    105 00120003 1003
    106 00130000 1002
    107 00130001 1002
    108 00130002 1002
    109 00130000 1001
    110 00130001 1001
    111 00130002 1001
    112 00130000 1004
    113 00130001 1003
    114 00130002 1003
    115 00140000 1002
    116 00140001 1002
    117 00140002 1002
    118 00140000 1001
    119 00140001 1001
    120 00140002 1001
    121 00140000 1004
    122 00140001 1003
    123 00140002 1003
    124 00150000 1002
    125 00150001 1002
    126 00150002 1002
    127 00150000 1001
    128 00150001 1001
    129 00150002 1001
    130 00150000 1004
    131 00150001 1003
    132 00150002 1003
    133 00160000 1002
    134 00160001 1002
    135 00160002 1002
    136 00160003 1002
    137 00160020 1002
    138 00160000 1001
    139 00160001 1001
    140 00160002 1001
    141 00160003 1001
    142 00160020 1001
    143 00160001 1003
    144 00160002 1003
    145 00160003 1003
    146 00170000 1002
    147 00170001 1002
    148 00170002 1002
    149 00170000 1001
    150 00170001 1001
    151 00170002 1001
    152 00170000 1004
    153 00170001 1003
    154 00170002 1003
    155 00180000 1002
    156 00180001 1002
    157 00180002 1002
    158 00180000 1001
    159 00180001 1001
    160 00180002 1001
    161 00180000 1004
    162 00180001 1003
    163 00180002 1003
    164 00190000 1002
    165 00190001 1002
    166 00190002 1002
    167 00190000 1001
    168 00190001 1001
    169 00190002 1001
    170 00190000 1004
    171 00190001 1003
    172 00190002 1003
    173 001a0000 1002
    174 001a0001 1002
    175 001a0020 1002
    176 001a0040 1002
    177 001a0000 1001
    178 001a0001 1001
    179 001a0020 1001
    180 001a0040 1001
    181 001a0001 1003
    182 001b0000 1002
    183 001b0001 1002
    184 001b0020 1002
    185 001b0040 1002
    186 001b0000 1001
    187 001b0001 1001
    188 001b0020 1001
    189 001b0040 1001
    190 001b0001 1003
    191 001c0000 1002
    192 001c0001 1002
    193 001c0020 1002
    194 001c0040 1002
    195 001c0000 1001
    196 001c0001 1001
    197 001c0020 1001
    198 001c0040 1001
    199 001c0001 1003
    200 80020000 1002
    201 80020000 1001
    202 80020001 1002
    203 80020002 1002
    204 80020001 1001
    205 80020002 1001
    206 80020002 1003
    207 00000000 1001
    208 00000000 1002
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
Param.val=-0.00000000000000000000
AddParam

Param.h.v.=00040011
Param.val=4.00000000000000000000
AddParam

Param.h.v.=00050010
Param.val=-3.96464864053683907485
AddParam

Param.h.v.=00050011
Param.val=0.53062336651281793998
AddParam

Param.h.v.=00060010
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00060011
Param.val=4.00000000000000000000
AddParam

Param.h.v.=00070010
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00070011
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00080010
AddParam

Param.h.v.=00080011
AddParam

Param.h.v.=00080013
Param.val=-0.00000000000000000000
AddParam

Param.h.v.=00080014
Param.val=4.00000000000000000000
AddParam

Param.h.v.=00080016
Param.val=-3.96464864053683907485
AddParam

Param.h.v.=00080017
Param.val=0.53062336651281793998
AddParam

Param.h.v.=00090010
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00090011
Param.val=0.00000000000000019308
AddParam

Param.h.v.=00090013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00090014
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00090016
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00090017
Param.val=4.00000000000000000000
AddParam

Param.h.v.=000a0010
Param.val=-0.00000000000000000000
AddParam

Param.h.v.=000a0011
Param.val=4.00000000000000000000
AddParam

Param.h.v.=000a0013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=000a0014
Param.val=4.00000000000000000000
AddParam

Param.h.v.=000c0010
AddParam

Param.h.v.=000c0011
AddParam

Param.h.v.=000c0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000d0010
Param.val=49.00000000000000000000
AddParam

Param.h.v.=000d0011
Param.val=0.00000000000000019308
AddParam

Param.h.v.=000d0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=000e0010
AddParam

Param.h.v.=000e0011
AddParam

Param.h.v.=000e0013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=000e0014
Param.val=0.00000000000000019308
AddParam

Param.h.v.=000f0010
Param.val=-4.86846938775510462705
AddParam

Param.h.v.=000f0011
Param.val=-36.37565127692549538097
AddParam

Param.h.v.=000f0040
Param.val=3.00000000000000000000
AddParam

Param.h.v.=00100010
AddParam

Param.h.v.=00100011
AddParam

Param.h.v.=00100013
Param.val=-4.86846938775510462705
AddParam

Param.h.v.=00100014
Param.val=-36.37565127692549538097
AddParam

Param.h.v.=00120010
Param.val=-4.86846938775510462705
AddParam

Param.h.v.=00120011
Param.val=-36.37565127692549538097
AddParam

Param.h.v.=00120013
Param.val=-8.83311802829194370190
AddParam

Param.h.v.=00120014
Param.val=-35.84502791041267499850
AddParam

Param.h.v.=00120016
Param.val=-0.90382074721826555219
AddParam

Param.h.v.=00120017
Param.val=-36.90627464343831576343
AddParam

Param.h.v.=00130010
Param.val=-3.96464864053683907485
AddParam

Param.h.v.=00130011
Param.val=0.53062336651281793998
AddParam

Param.h.v.=00130013
Param.val=-8.83311802829194370190
AddParam

Param.h.v.=00130014
Param.val=-35.84502791041267499850
AddParam

Param.h.v.=00140010
Param.val=3.50031182891143277658
AddParam

Param.h.v.=00140011
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00140013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00140014
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00150010
Param.val=3.50031182891143277658
AddParam

Param.h.v.=00150011
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00150013
Param.val=-0.90382074721826555219
AddParam

Param.h.v.=00150014
Param.val=-36.90627464343831576343
AddParam

Param.h.v.=00160010
Param.val=29.75265054574717993319
AddParam

Param.h.v.=00160011
Param.val=-34.00000000000000000000
AddParam

Param.h.v.=00160013
Param.val=29.75265054574717993319
AddParam

Param.h.v.=00160014
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00160016
Param.val=0.01778574172088896038
AddParam

Param.h.v.=00160017
Param.val=-30.02032475115386489506
AddParam

Param.h.v.=00170010
Param.val=29.75265054574717993319
AddParam

Param.h.v.=00170011
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00170013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00170014
Param.val=-4.00000000000000000000
AddParam

Param.h.v.=00180010
Param.val=0.01778574172088896038
AddParam

Param.h.v.=00180011
Param.val=-30.02032475115386489506
AddParam

Param.h.v.=00180013
Param.val=-0.90382074721826555219
AddParam

Param.h.v.=00180014
Param.val=-36.90627464343831576343
AddParam

Param.h.v.=00190010
Param.val=-4.86846938775510462705
AddParam

Param.h.v.=00190011
Param.val=-36.37565127692549538097
AddParam

Param.h.v.=00190013
Param.val=49.00000000000000000000
AddParam

Param.h.v.=00190014
Param.val=0.00000000000000019308
AddParam

Param.h.v.=001a0010
AddParam

Param.h.v.=001a0011
AddParam

Param.h.v.=001a0040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=001b0010
Param.val=-4.86846938775510462705
AddParam

Param.h.v.=001b0011
Param.val=-36.37565127692549538097
AddParam

Param.h.v.=001b0040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=001c0010
Param.val=49.00000000000000000000
AddParam

Param.h.v.=001c0011
Param.val=0.00000000000000019308
AddParam

Param.h.v.=001c0040
Param.val=1.00000000000000000000
AddParam

Param.h.v.=40000033
Param.val=0.57697843154707628699
AddParam

Param.h.v.=40000037
Param.val=0.79074052086119261951
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
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=00000012
Request.type=500
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000013
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000014
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=00000015
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=00000016
Request.type=500
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000017
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000018
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=00000019
Request.type=200
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=1
AddRequest

Request.h.v=0000001a
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000001b
Request.type=400
Request.workplane.v=80020000
Request.group.v=00000002
Request.construction=0
AddRequest

Request.h.v=0000001c
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
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00050000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actVisible=1
AddEntity

Entity.h.v=00060000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00070000
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
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
Entity.actVisible=1
AddEntity

Entity.h.v=00080002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00080003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
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
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=00090002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00090003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
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
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=000a0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
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
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
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
Entity.actVisible=1
AddEntity

Entity.h.v=000e0002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
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
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
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
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00100000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00100001
Entity.point[1].v=00100002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00100001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00100002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=00120000
Entity.type=14000
Entity.construction=0
Entity.point[0].v=00120001
Entity.point[1].v=00120002
Entity.point[2].v=00120003
Entity.normal.v=00120020
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00120001
Entity.type=2001
Entity.construction=1
Entity.workplane.v=80020000
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=00120002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actVisible=1
AddEntity

Entity.h.v=00120003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=00120020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00120001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00130000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=00130001
Entity.point[1].v=00130002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00130001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actVisible=1
AddEntity

Entity.h.v=00130002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actVisible=1
AddEntity

Entity.h.v=00140000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00140001
Entity.point[1].v=00140002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00140001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00140002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00150000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00150001
Entity.point[1].v=00150002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00150001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00150002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=00160000
Entity.type=14000
Entity.construction=0
Entity.point[0].v=00160001
Entity.point[1].v=00160002
Entity.point[2].v=00160003
Entity.normal.v=00160020
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00160001
Entity.type=2001
Entity.construction=1
Entity.workplane.v=80020000
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-34.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00160002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00160003
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actVisible=1
AddEntity

Entity.h.v=00160020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=00160001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00170000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=00170001
Entity.point[1].v=00170002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00170001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00170002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=00180000
Entity.type=11000
Entity.construction=0
Entity.point[0].v=00180001
Entity.point[1].v=00180002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00180001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actVisible=1
AddEntity

Entity.h.v=00180002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=00190000
Entity.type=11000
Entity.construction=1
Entity.point[0].v=00190001
Entity.point[1].v=00190002
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=00190001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=00190002
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=001a0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=001a0001
Entity.normal.v=001a0020
Entity.distance.v=001a0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=001a0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=001a0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=001a0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=001a0040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=001b0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=001b0001
Entity.normal.v=001b0020
Entity.distance.v=001b0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=001b0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=001b0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=001b0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=001b0040
Entity.type=4000
Entity.construction=0
Entity.workplane.v=80020000
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=001c0000
Entity.type=13000
Entity.construction=0
Entity.point[0].v=001c0001
Entity.normal.v=001c0020
Entity.distance.v=001c0040
Entity.workplane.v=80020000
Entity.actVisible=1
AddEntity

Entity.h.v=001c0001
Entity.type=2001
Entity.construction=0
Entity.workplane.v=80020000
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=001c0020
Entity.type=3001
Entity.construction=0
Entity.point[0].v=001c0001
Entity.workplane.v=80020000
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=001c0040
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
Entity.actVisible=0
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
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030002
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030003
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030002
Entity.point[1].v=80030001
Entity.actVisible=1
AddEntity

Entity.h.v=80030004
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actVisible=1
AddEntity

Entity.h.v=80030005
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030006
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030005
Entity.point[1].v=80030004
Entity.actVisible=1
AddEntity

Entity.h.v=80030007
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030008
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030009
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030008
Entity.point[1].v=80030007
Entity.actVisible=1
AddEntity

Entity.h.v=8003000a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003000b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003000c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003000b
Entity.point[1].v=8003000a
Entity.actVisible=1
AddEntity

Entity.h.v=8003000d
Entity.type=14000
Entity.construction=0
Entity.point[0].v=8003000e
Entity.point[1].v=8003000f
Entity.point[2].v=80030010
Entity.normal.v=80030011
Entity.actVisible=1
AddEntity

Entity.h.v=8003000e
Entity.type=2010
Entity.construction=1
Entity.actVisible=1
AddEntity

Entity.h.v=8003000f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030010
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actVisible=1
AddEntity

Entity.h.v=80030011
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003000e
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030012
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030013
Entity.point[1].v=80030014
Entity.point[2].v=80030015
Entity.normal.v=80030016
Entity.actVisible=1
AddEntity

Entity.h.v=80030013
Entity.type=2010
Entity.construction=1
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030014
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030015
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030016
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030013
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030017
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030013
Entity.point[1].v=8003000e
Entity.actVisible=1
AddEntity

Entity.h.v=80030018
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030014
Entity.point[1].v=8003000f
Entity.actVisible=1
AddEntity

Entity.h.v=80030019
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030015
Entity.point[1].v=80030010
Entity.actVisible=1
AddEntity

Entity.h.v=8003001a
Entity.type=14000
Entity.construction=0
Entity.point[0].v=8003001b
Entity.point[1].v=8003001c
Entity.point[2].v=8003001d
Entity.normal.v=8003001e
Entity.actVisible=1
AddEntity

Entity.h.v=8003001b
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=8003001c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001e
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003001b
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003001f
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030020
Entity.point[1].v=80030021
Entity.point[2].v=80030022
Entity.normal.v=80030023
Entity.actVisible=1
AddEntity

Entity.h.v=80030020
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030021
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030022
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030023
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030020
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030024
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030020
Entity.point[1].v=8003001b
Entity.actVisible=1
AddEntity

Entity.h.v=80030025
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030021
Entity.point[1].v=8003001c
Entity.actVisible=1
AddEntity

Entity.h.v=80030026
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030022
Entity.point[1].v=8003001d
Entity.actVisible=1
AddEntity

Entity.h.v=80030027
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030028
Entity.point[1].v=80030029
Entity.actVisible=1
AddEntity

Entity.h.v=80030028
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030029
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003002a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003002b
Entity.point[1].v=8003002c
Entity.actVisible=1
AddEntity

Entity.h.v=8003002b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003002c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003002d
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-0.00000000000000000000
Entity.actPoint.y=4.00000000000000000000
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003002e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003002b
Entity.point[1].v=80030028
Entity.actVisible=1
AddEntity

Entity.h.v=8003002f
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003002c
Entity.point[1].v=80030029
Entity.actVisible=1
AddEntity

Entity.h.v=80030030
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030031
Entity.normal.v=80030032
Entity.distance.v=80030033
Entity.actVisible=1
AddEntity

Entity.h.v=80030031
Entity.type=2010
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=80030032
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030031
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030033
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030034
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030035
Entity.normal.v=80030036
Entity.distance.v=80030037
Entity.actVisible=1
AddEntity

Entity.h.v=80030035
Entity.type=2010
Entity.construction=0
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030036
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030035
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030037
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030038
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030035
Entity.point[1].v=80030031
Entity.actVisible=1
AddEntity

Entity.h.v=80030039
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003003a
Entity.normal.v=8003003b
Entity.distance.v=8003003c
Entity.actVisible=1
AddEntity

Entity.h.v=8003003a
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=8003003b
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003003a
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003003c
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003003d
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003003e
Entity.normal.v=8003003f
Entity.distance.v=80030040
Entity.actVisible=1
AddEntity

Entity.h.v=8003003e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003003f
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003003e
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030040
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030041
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003003e
Entity.point[1].v=8003003a
Entity.actVisible=1
AddEntity

Entity.h.v=80030042
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030043
Entity.point[1].v=80030044
Entity.actVisible=1
AddEntity

Entity.h.v=80030043
Entity.type=2010
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=80030044
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=80030045
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030046
Entity.point[1].v=80030047
Entity.actVisible=1
AddEntity

Entity.h.v=80030046
Entity.type=2010
Entity.construction=0
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030047
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030048
Entity.type=5001
Entity.construction=1
Entity.actNormal.vx=-0.00000000000000000394
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030049
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030046
Entity.point[1].v=80030043
Entity.actVisible=1
AddEntity

Entity.h.v=8003004a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030047
Entity.point[1].v=80030044
Entity.actVisible=1
AddEntity

Entity.h.v=8003004b
Entity.type=13000
Entity.construction=0
Entity.point[0].v=8003004c
Entity.normal.v=8003004d
Entity.distance.v=8003004e
Entity.actVisible=1
AddEntity

Entity.h.v=8003004c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=8003004d
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003004c
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003004e
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003004f
Entity.type=13000
Entity.construction=0
Entity.point[0].v=80030050
Entity.normal.v=80030051
Entity.distance.v=80030052
Entity.actVisible=1
AddEntity

Entity.h.v=80030050
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030051
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030050
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030052
Entity.type=4001
Entity.construction=0
Entity.actDistance=3.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030053
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030050
Entity.point[1].v=8003004c
Entity.actVisible=1
AddEntity

Entity.h.v=80030054
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030055
Entity.point[1].v=80030056
Entity.actVisible=1
AddEntity

Entity.h.v=80030055
Entity.type=2010
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=80030056
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=80030057
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030058
Entity.point[1].v=80030059
Entity.actVisible=1
AddEntity

Entity.h.v=80030058
Entity.type=2010
Entity.construction=0
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030059
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003005a
Entity.type=5001
Entity.construction=1
Entity.actNormal.vx=0.99116216013420976871
Entity.actNormal.vy=-0.13265584162820448499
Entity.actVisible=1
AddEntity

Entity.h.v=8003005b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030058
Entity.point[1].v=80030055
Entity.actVisible=1
AddEntity

Entity.h.v=8003005c
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030059
Entity.point[1].v=80030056
Entity.actVisible=1
AddEntity

Entity.h.v=8003005d
Entity.type=14000
Entity.construction=0
Entity.point[0].v=8003005e
Entity.point[1].v=8003005f
Entity.point[2].v=80030060
Entity.normal.v=80030061
Entity.actVisible=1
AddEntity

Entity.h.v=8003005e
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=8003005f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actVisible=1
AddEntity

Entity.h.v=80030060
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=80030061
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003005e
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030062
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030063
Entity.point[1].v=80030064
Entity.point[2].v=80030065
Entity.normal.v=80030066
Entity.actVisible=1
AddEntity

Entity.h.v=80030063
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030064
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030065
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030066
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030063
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030067
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030063
Entity.point[1].v=8003005e
Entity.actVisible=1
AddEntity

Entity.h.v=80030068
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030064
Entity.point[1].v=8003005f
Entity.actVisible=1
AddEntity

Entity.h.v=80030069
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030065
Entity.point[1].v=80030060
Entity.actVisible=1
AddEntity

Entity.h.v=8003006a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006b
Entity.point[1].v=8003006c
Entity.actVisible=1
AddEntity

Entity.h.v=8003006b
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actVisible=1
AddEntity

Entity.h.v=8003006c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actVisible=1
AddEntity

Entity.h.v=8003006d
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006e
Entity.point[1].v=8003006f
Entity.actVisible=1
AddEntity

Entity.h.v=8003006e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003006f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-8.83311802829194370190
Entity.actPoint.y=-35.84502791041267499850
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030070
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=-3.96464864053683907485
Entity.actPoint.y=0.53062336651281793998
Entity.actNormal.vx=0.99116216013420976871
Entity.actNormal.vy=-0.13265584162820448499
Entity.actVisible=1
AddEntity

Entity.h.v=80030071
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006e
Entity.point[1].v=8003006b
Entity.actVisible=1
AddEntity

Entity.h.v=80030072
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003006f
Entity.point[1].v=8003006c
Entity.actVisible=1
AddEntity

Entity.h.v=80030073
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030074
Entity.point[1].v=80030075
Entity.actVisible=1
AddEntity

Entity.h.v=80030074
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030075
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030076
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030077
Entity.point[1].v=80030078
Entity.actVisible=1
AddEntity

Entity.h.v=80030077
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030078
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030079
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003007a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030077
Entity.point[1].v=80030074
Entity.actVisible=1
AddEntity

Entity.h.v=8003007b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030078
Entity.point[1].v=80030075
Entity.actVisible=1
AddEntity

Entity.h.v=8003007c
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003007d
Entity.point[1].v=8003007e
Entity.actVisible=1
AddEntity

Entity.h.v=8003007d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003007e
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=8003007f
Entity.type=11000
Entity.construction=1
Entity.point[0].v=80030080
Entity.point[1].v=80030081
Entity.actVisible=1
AddEntity

Entity.h.v=80030080
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030081
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030082
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=3.50031182891143277658
Entity.actPoint.y=-4.00000000000000000000
Entity.actNormal.vx=0.99116216013420965769
Entity.actNormal.vy=-0.13265584162820445724
Entity.actVisible=1
AddEntity

Entity.h.v=80030083
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030080
Entity.point[1].v=8003007d
Entity.actVisible=1
AddEntity

Entity.h.v=80030084
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030081
Entity.point[1].v=8003007e
Entity.actVisible=1
AddEntity

Entity.h.v=80030085
Entity.type=14000
Entity.construction=0
Entity.point[0].v=80030086
Entity.point[1].v=80030087
Entity.point[2].v=80030088
Entity.normal.v=80030089
Entity.actVisible=1
AddEntity

Entity.h.v=80030086
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-34.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030087
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030088
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actVisible=1
AddEntity

Entity.h.v=80030089
Entity.type=3010
Entity.construction=0
Entity.point[0].v=80030086
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008a
Entity.type=14000
Entity.construction=0
Entity.point[0].v=8003008b
Entity.point[1].v=8003008c
Entity.point[2].v=8003008d
Entity.normal.v=8003008e
Entity.actVisible=1
AddEntity

Entity.h.v=8003008b
Entity.type=2010
Entity.construction=1
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-34.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008e
Entity.type=3010
Entity.construction=0
Entity.point[0].v=8003008b
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=8003008f
Entity.type=11000
Entity.construction=1
Entity.point[0].v=8003008b
Entity.point[1].v=80030086
Entity.actVisible=1
AddEntity

Entity.h.v=80030090
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003008c
Entity.point[1].v=80030087
Entity.actVisible=1
AddEntity

Entity.h.v=80030091
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003008d
Entity.point[1].v=80030088
Entity.actVisible=1
AddEntity

Entity.h.v=80030092
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030093
Entity.point[1].v=80030094
Entity.actVisible=1
AddEntity

Entity.h.v=80030093
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030094
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030095
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030096
Entity.point[1].v=80030097
Entity.actVisible=1
AddEntity

Entity.h.v=80030096
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030097
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=-4.00000000000000000000
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030098
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=29.75265054574717993319
Entity.actPoint.y=-4.00000000000000000000
Entity.actNormal.vy=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=80030099
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030096
Entity.point[1].v=80030093
Entity.actVisible=1
AddEntity

Entity.h.v=8003009a
Entity.type=11000
Entity.construction=0
Entity.point[0].v=80030097
Entity.point[1].v=80030094
Entity.actVisible=1
AddEntity

Entity.h.v=8003009b
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003009c
Entity.point[1].v=8003009d
Entity.actVisible=1
AddEntity

Entity.h.v=8003009c
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actVisible=1
AddEntity

Entity.h.v=8003009d
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actVisible=1
AddEntity

Entity.h.v=8003009e
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003009f
Entity.point[1].v=800300a0
Entity.actVisible=1
AddEntity

Entity.h.v=8003009f
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a0
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-0.90382074721826555219
Entity.actPoint.y=-36.90627464343831576343
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a1
Entity.type=5001
Entity.construction=0
Entity.actPoint.x=0.01778574172088896038
Entity.actPoint.y=-30.02032475115386489506
Entity.actNormal.vx=0.99116216013420965769
Entity.actNormal.vy=-0.13265584162820437397
Entity.actVisible=1
AddEntity

Entity.h.v=800300a2
Entity.type=11000
Entity.construction=0
Entity.point[0].v=8003009f
Entity.point[1].v=8003009c
Entity.actVisible=1
AddEntity

Entity.h.v=800300a3
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a0
Entity.point[1].v=8003009d
Entity.actVisible=1
AddEntity

Entity.h.v=800300a4
Entity.type=11000
Entity.construction=1
Entity.point[0].v=800300a5
Entity.point[1].v=800300a6
Entity.actVisible=1
AddEntity

Entity.h.v=800300a5
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=800300a6
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=800300a7
Entity.type=11000
Entity.construction=1
Entity.point[0].v=800300a8
Entity.point[1].v=800300a9
Entity.actVisible=1
AddEntity

Entity.h.v=800300a8
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300a9
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300aa
Entity.type=5001
Entity.construction=1
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actNormal.vx=-0.55962540426039231178
Entity.actNormal.vy=0.82874568288854000286
Entity.actVisible=1
AddEntity

Entity.h.v=800300ab
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a8
Entity.point[1].v=800300a5
Entity.actVisible=1
AddEntity

Entity.h.v=800300ac
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300a9
Entity.point[1].v=800300a6
Entity.actVisible=1
AddEntity

Entity.h.v=800300ad
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300ae
Entity.normal.v=800300af
Entity.distance.v=800300b0
Entity.actVisible=1
AddEntity

Entity.h.v=800300ae
Entity.type=2010
Entity.construction=0
Entity.actVisible=1
AddEntity

Entity.h.v=800300af
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300ae
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b0
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b1
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300b2
Entity.normal.v=800300b3
Entity.distance.v=800300b4
Entity.actVisible=1
AddEntity

Entity.h.v=800300b2
Entity.type=2010
Entity.construction=0
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b3
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300b2
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b4
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b5
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300b2
Entity.point[1].v=800300ae
Entity.actVisible=1
AddEntity

Entity.h.v=800300b6
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300b7
Entity.normal.v=800300b8
Entity.distance.v=800300b9
Entity.actVisible=1
AddEntity

Entity.h.v=800300b7
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actVisible=1
AddEntity

Entity.h.v=800300b8
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300b7
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300b9
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300ba
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300bb
Entity.normal.v=800300bc
Entity.distance.v=800300bd
Entity.actVisible=1
AddEntity

Entity.h.v=800300bb
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=-4.86846938775510462705
Entity.actPoint.y=-36.37565127692549538097
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300bc
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300bb
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300bd
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300be
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300bb
Entity.point[1].v=800300b7
Entity.actVisible=1
AddEntity

Entity.h.v=800300bf
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300c0
Entity.normal.v=800300c1
Entity.distance.v=800300c2
Entity.actVisible=1
AddEntity

Entity.h.v=800300c0
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actVisible=1
AddEntity

Entity.h.v=800300c1
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300c0
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c2
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c3
Entity.type=13000
Entity.construction=0
Entity.point[0].v=800300c4
Entity.normal.v=800300c5
Entity.distance.v=800300c6
Entity.actVisible=1
AddEntity

Entity.h.v=800300c4
Entity.type=2010
Entity.construction=0
Entity.actPoint.x=49.00000000000000000000
Entity.actPoint.y=0.00000000000000019308
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c5
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300c4
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c6
Entity.type=4001
Entity.construction=0
Entity.actDistance=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300c7
Entity.type=11000
Entity.construction=0
Entity.point[0].v=800300c4
Entity.point[1].v=800300c0
Entity.actVisible=1
AddEntity

Entity.h.v=800300ca
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300cb
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300cb
Entity.type=2010
Entity.construction=1
Entity.actVisible=1
AddEntity

Entity.h.v=800300cc
Entity.type=3010
Entity.construction=0
Entity.point[0].v=800300cd
Entity.actNormal.w=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300cd
Entity.type=2010
Entity.construction=1
Entity.actPoint.z=5.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300ce
Entity.type=11000
Entity.construction=1
Entity.point[0].v=800300cd
Entity.point[1].v=800300cb
Entity.actVisible=1
AddEntity

Entity.h.v=800300cf
Entity.type=5000
Entity.construction=0
Entity.point[0].v=800300cd
Entity.actPoint.z=5.00000000000000000000
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=1
AddEntity

Entity.h.v=800300d0
Entity.type=5000
Entity.construction=0
Entity.point[0].v=800300cb
Entity.actNormal.vz=1.00000000000000000000
Entity.actVisible=1
AddEntity

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

Constraint.h.v=00000009
Constraint.type=80
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=000a0000
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

Constraint.h.v=00000018
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={1:.20}
Constraint.ptA.v=000a0001
Constraint.ptB.v=000a0002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.y=-4.98379740810769344961
Constraint.disp.offset.z=0.76399943691950611413
AddConstraint

Constraint.h.v=00000019
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={5:.20f}
Constraint.entityA.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-9.01890181250750622155
Constraint.disp.offset.y=11.04383810660871567677
Constraint.disp.offset.z=-3.68020959143254078327
AddConstraint

Constraint.h.v=0000001a
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=000f0000
Constraint.entityB.v=000c0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001b
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=00100001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001c
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=00100002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000001f
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={0:.20f}
Constraint.ptA.v=00100001
Constraint.ptB.v=00100002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-4.69733188510273169669
Constraint.disp.offset.y=-3.37162121231044098479
AddConstraint

Constraint.h.v=00000021
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120001
Constraint.ptB.v=000f0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000022
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00050000
Constraint.ptB.v=00130001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000023
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120002
Constraint.ptB.v=00130002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000029
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00080000
Constraint.entityB.v=00130000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002a
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00130000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002b
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={3:.20f}
Constraint.entityA.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-3.11365811149568294525
Constraint.disp.offset.y=17.32341022105662275976
AddConstraint

Constraint.h.v=0000002c
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00090000
Constraint.entityB.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002d
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00080000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002e
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00070000
Constraint.ptB.v=00140002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000002f
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00140001
Constraint.ptB.v=00150001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000030
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00120003
Constraint.ptB.v=00150002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000031
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00170001
Constraint.ptB.v=00160002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000032
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00170002
Constraint.ptB.v=00070000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000033
Constraint.type=42
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00170001
Constraint.entityA.v=00140000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000034
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00160000
Constraint.entityB.v=00170000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000035
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00180001
Constraint.ptB.v=00160003
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000036
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00180002
Constraint.ptB.v=00120003
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000037
Constraint.type=42
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00180001
Constraint.entityA.v=00150000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000038
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00160000
Constraint.entityB.v=00180000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000003a
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00120000
Constraint.entityB.v=00180000
Constraint.other=1
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000003b
Constraint.type=123
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00090000
Constraint.entityB.v=00140000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000003c
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=00190001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000003d
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=00190002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=0000003e
Constraint.type=30
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={2:.20f}
Constraint.ptA.v=00190001
Constraint.ptB.v=00190002
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=3.73536235296541008211
Constraint.disp.offset.y=-3.95879071986783115378
Constraint.disp.offset.z=1.95135864628764998940
AddConstraint

Constraint.h.v=0000003f
Constraint.type=121
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00150000
Constraint.entityB.v=00130000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000040
Constraint.type=121
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=00140000
Constraint.entityB.v=000a0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000041
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00080001
Constraint.ptB.v=00010001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000042
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00010001
Constraint.ptB.v=001a0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000043
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=000f0001
Constraint.ptB.v=001b0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000044
Constraint.type=20
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.ptA.v=00090001
Constraint.ptB.v=001c0001
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000045
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={6:.20f}
Constraint.entityA.v=001a0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-7.41251620232965446888
Constraint.disp.offset.y=-1.83320293175894821758
AddConstraint

Constraint.h.v=00000046
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=001c0000
Constraint.entityB.v=001a0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000047
Constraint.type=130
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.entityA.v=001a0000
Constraint.entityB.v=001b0000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
AddConstraint

Constraint.h.v=00000048
Constraint.type=90
Constraint.group.v=00000002
Constraint.workplane.v=80020000
Constraint.valA={7:.20f}
Constraint.entityA.v=00160000
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-14.95102433075455294897
Constraint.disp.offset.y=17.78054050240756822632
Constraint.disp.offset.z=2.26760264068503314405
AddConstraint

Constraint.h.v=00000049
Constraint.type=30
Constraint.group.v=00000003
Constraint.valA={4:.20f}
Constraint.ptA.v=80030005
Constraint.ptB.v=80030004
Constraint.other=0
Constraint.other2=0
Constraint.reference=0
Constraint.disp.offset.x=-2.37670997726732746713
Constraint.disp.offset.y=1.59155860994034004108
AddConstraint
""".format(length1, length3, length2, width, thickness, drilling, joint, width/2)
