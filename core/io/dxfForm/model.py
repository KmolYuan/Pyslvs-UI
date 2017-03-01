# -*- coding: utf-8 -*-
from dxfwrite import DXFEngine as dxf

def dxfModel(file_name, Link, Chain, LinkWidth, ChainWidth, interval):
    Anchor = (0, 0)
    mechanism = dxf.drawing(file_name)
    for e in Link:
        name = 'Line{}'.format(Link.index(e))
        block = dxf.block(name=name)
        #TODO: Link Model
        mechanism.block.add(block)
        blockref = dxf.insert(blockname=name, insert=Anchor)
        mechanism.add(blockref)
        Anchor[1] += (LinkWidth+interval)/2
    Anchor[0] += (LinkWidth+interval)/2
    for e in Chain:
        name = 'Chain{}'.format(Link.index(e))
        block = dxf.block(name=name)
        #TODO: Chain Model
        mechanism.block.add(block)
        blockref = dxf.insert(blockname=name, insert=Anchor)
        mechanism.add(blockref)
        Anchor[1] += (ChainWidth+interval)/2
    mechanism.save()
