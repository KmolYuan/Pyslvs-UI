# -*- coding: utf-8 -*-
from .sketch import slvs2D

def slvsAssembly(Point, Line, Chain):
    script = slvs2D(Point, Line, Chain)
    return script
