# -*- coding: utf-8 -*-
from .slvsForm_2d import slvs2D

def slvsAssembly(Point, Line, Chain):
    script = slvs2D(Point, Line, Chain)
    return script
