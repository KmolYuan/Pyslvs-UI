# -*- coding: utf-8 -*-
from .__init__ import *

class FileCommand(QUndoCommand):
    def __init__(self, File):
        QUndoCommand.__init__(self)
        #Record File
        self.File = File
        #Recorded list
        self.Point = File.Points.list
        self.Lines = File.Lines.list
        self.Chains = File.Chains.list
        self.Shafts = File.Shafts.list
        self.Sliders = File.Sliders.list
        self.Rods = File.Rods.list
        self.Parameters = File.Parameters.list
        self.Path = File.Path.data
        self.runList = File.Path.runList
    
    def undo(self):
        self.File.Points.list = self.Point
        self.File.Lines.list = self.Lines
        self.File.Chains.list = self.Chains
        self.File.Shafts.list = self.Shafts
        self.File.Sliders.list = self.Sliders
        self.File.Rods.list = self.Rods
        self.File.Parameters.list = self.Parameters
        self.File.Path.data = self.Path
        self.File.Path.runList = self.runList
    
    def redo(self):
        self.File.Points.list = self.Point
        self.File.Lines.list = self.Lines
        self.File.Chains.list = self.Chains
        self.File.Shafts.list = self.Shafts
        self.File.Sliders.list = self.Sliders
        self.File.Rods.list = self.Rods
        self.File.Parameters.list = self.Parameters
        self.File.Path.data = self.Path
        self.File.Path.runList = self.runList
