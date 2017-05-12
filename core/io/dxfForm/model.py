# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf
from math import *

CosineTheoremAngle = lambda a, b, c: degrees(acos((b**2+c**2-a**2)/(2*b*c)))
CosineTheoremSide = lambda alpha, b, c: b**2+c**2-2*b*c*cos(alpha)

def dxfModel(file_name, Link, Chain, LinkWidth=8, ChainWidth=8, interval=2, drilling=6):
    Anchor = [0, 0]
    mechanism = dxf.drawing(file_name)
    for e in Link:
        name = 'Line{}'.format(Link.index(e))
        block = dxf.block(name=name)
        radius = LinkWidth/2
        block.add(dxf.line((0, radius), (e.len, radius)))
        block.add(dxf.line((0, -radius), (e.len, -radius)))
        block.add(dxf.circle(drilling/2, (0, 0)))
        block.add(dxf.circle(drilling/2, (e.len, 0)))
        block.add(dxf.arc(radius, (0, 0), 90., 270.))
        block.add(dxf.arc(radius, (e.len, 0), 270., 90.))
        mechanism.blocks.add(block)
        blockref = dxf.insert(blockname=name, insert=tuple(Anchor))
        mechanism.add(blockref)
        Anchor[1] += LinkWidth+interval
    for e in Chain:
        name = 'Chain{}'.format(Chain.index(e))
        block = dxf.block(name=name)
        radius = ChainWidth/2
        a, b, c = sorted([e.p1p2, e.p2p3, e.p1p3], reverse=True)
        alpha = CosineTheoremAngle(b, a, c)
        beta = CosineTheoremAngle(c, a, b)
        garma = CosineTheoremAngle(a, b, c)
        p1 = (0, 0)
        p2 = (a, 0)
        p3 = (c*cos(radians(alpha)), c*sin(radians(alpha)))
        f0 = (0, -radius)
        f1 = (a, -radius)
        f2 = (a+radius*cos(radians(90.-beta)), radius*sin(radians(90.-beta)))
        f3 = (f2[0]-b*cos(radians(beta)), f2[1]+b*sin(radians(beta)))
        f4 = (-radius*cos(radians(90.-alpha)), radius*sin(radians(90.-alpha)))
        f5 = (f4[0]+c*cos(radians(alpha)), f4[1]+c*sin(radians(alpha)))
        block.add(dxf.arc(radius, p3, 90.-beta, alpha+90.))
        block.add(dxf.line(f2, f3))
        block.add(dxf.line(f4, f5))
        block.add(dxf.circle(drilling/2, p1))
        block.add(dxf.circle(drilling/2, p2))
        block.add(dxf.circle(drilling/2, p3))
        block.add(dxf.line(f0, f1))
        block.add(dxf.arc(radius, p1, alpha+90., 270.))
        block.add(dxf.arc(radius, p2, 270., 90.-beta))
        mechanism.blocks.add(block)
        blockref = dxf.insert(blockname=name, insert=tuple(Anchor))
        mechanism.add(blockref)
        Anchor[1] += ChainWidth+interval+p3[1]
    mechanism.save()
