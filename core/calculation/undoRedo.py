# -*- coding: utf-8 -*-
from .__init__ import *

class FileState():
    def __init__(self):
        self.list = []
        self.index = 0
        self.maxRecord = 15
    
    def newStep(self, cmd):
        self.list = self.list[0:self.index]
        self.list.append(cmd)
        self.index += 1
        self.maxDel()
    
    def undo(self):
        self.index -= 1
        return self.list[self.index]
    
    def redo(self):
        self.index += 1
        return self.list[self.index]
    
    def maxDel(self):
        if len(self.list)>self.maxRecord:
            self.list.pop(0)
    
    def setMax(self, val):
        self.maxRecord = val
        self.maxDel()

class FileCommand():
    def record(self, File, Point, Style, Line, Chain, Shaft, Slider, Rod, Parameter):
        self.File = File
        self.Point = Point
        self.Style = Style
        self.Line = Line
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        self.Parameter = Parameter
