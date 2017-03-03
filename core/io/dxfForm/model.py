# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf
from math import *

def dxfModel(file_name, Link, Chain, LinkWidth=8, ChainWidth=8, LinkType=0, ChainType=0, interval=2, drilling=6):
    Anchor = [0, 0]
    mechanism = dxf.drawing(file_name)
    for e in Link:
        name = 'Line{}'.format(Link.index(e))
        block = dxf.block(name=name)
        radius = LinkWidth/2
        if LinkType==0:
            block.add(dxf.arc(radius, (0, 0), 90., 270.))
            block.add(dxf.arc(radius, (e['len'], 0), 270., 90.))
            block.add(dxf.line((0, radius), (e['len'], radius)))
            block.add(dxf.line((0, -radius), (e['len'], -radius)))
            block.add(dxf.circle(drilling/2, (0, 0)))
            block.add(dxf.circle(drilling/2, (e['len'], 0)))
        mechanism.blocks.add(block)
        blockref = dxf.insert(blockname=name, insert=tuple(Anchor))
        mechanism.add(blockref)
        Anchor[1] += LinkWidth+interval
    for e in Chain:
        name = 'Chain{}'.format(Chain.index(e))
        block = dxf.block(name=name)
        radius = ChainWidth/2
        alpha = CosineTheorem(e['p2p3'], e['p1p2'], e['p1p3'])
        beta = CosineTheorem(e['p1p3'], e['p1p2'], e['p2p3'])
        garma = CosineTheorem(e['p1p2'], e['p2p3'], e['p1p3'])
        if ChainType==0:
            p1 = (0, 0)
            p2 = (e['p1p2'], 0)
            p3 = (e['p1p3']*cos(radians(alpha)), e['p1p3']*sin(radians(alpha)))
            block.add(dxf.arc(radius, p1, alpha+90., 270.))
            block.add(dxf.arc(radius, p2, 270., 90.-beta))
            block.add(dxf.arc(radius, p3, 90.-beta, alpha+90.))
            f0 = (0, -radius)
            f1 = (e['p1p2'], -radius)
            f2 = (e['p1p2']+radius*cos(radians(90.-beta)), radius*sin(radians(90.-beta)))
            f3 = (f2[0]-e['p2p3']*cos(radians(beta)), f2[1]+e['p2p3']*sin(radians(beta)))
            f4 = (-radius*cos(radians(90.-alpha)), radius*sin(radians(90.-alpha)))
            f5 = (f4[0]+e['p1p3']*cos(radians(alpha)), f4[1]+e['p1p3']*sin(radians(alpha)))
            block.add(dxf.line(f0, f1))
            block.add(dxf.line(f2, f3))
            block.add(dxf.line(f4, f5))
            block.add(dxf.circle(drilling/2, p1))
            block.add(dxf.circle(drilling/2, p2))
            block.add(dxf.circle(drilling/2, p3))
        mechanism.blocks.add(block)
        blockref = dxf.insert(blockname=name, insert=tuple(Anchor))
        mechanism.add(blockref)
        Anchor[1] += ChainWidth+interval+p3[1]
    mechanism.save()

def CosineTheorem(a, b, c): return degrees(acos((b**2+c**2-a**2)/(2*b*c)))
