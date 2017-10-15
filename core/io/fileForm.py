# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ..QtModules import *
import datetime
def timeNow():
    now = datetime.datetime.now()
    return "{:d}/{:d}/{:d} {:d}:{:d}".format(now.year, now.month, now.day, now.hour, now.minute)

class Designs:
    __slots__ = ('path', 'result', 'TSDirections')
    
    def __init__(self):
        self.path = []
        self.result = []
        self.TSDirections = []
    
    def setPath(self, path):
        self.path = path
    
    def addResult(self, result):
        self.result = result
    
    def add(self, x, y):
        self.path.append((x, y))
    
    def remove(self, pos):
        del self.path[pos]
    
    def removeResult(self, pos):
        del self.result[pos]
    
    def moveUP(self, row):
        if row>0 and len(self.path)>1:
            self.path.insert(row-1, (self.path[row]['x'], self.path[row]['y']))
            del self.path[row+1]
    
    def moveDown(self, row):
        if row<len(self.path)-1 and len(self.path)>1:
            self.path.insert(row+2, (self.path[row]['x'], self.path[row]['y']))
            del self.path[row]

#Use to record file main informations.
class File:
    __slots__ = (
        'FileState', 'args', 'pathData', 'Designs', 'Script',
        'fileName', 'description', 'author', 'lastTime', 'changed', 'Stack'
    )
    
    def __init__(self, FileState, args):
        self.FileState = FileState
        self.args = args
        self.resetAllList()
    
    def resetAllList(self):
        self.pathData = []
        self.Designs = Designs()
        self.Script = ""
        self.fileName = QFileInfo('[New Workbook]')
        self.description = ""
        self.author = 'Anonymous'
        self.lastTime = timeNow()
        self.changed = False
        self.Stack = 0
        self.FileState.clear()
    
    def setFileName(self, fileName):
        self.fileName = QFileInfo(fileName)
    
    def updateTime(self):
        self.lastTime = timeNow()
    
    def updateAuthorDescription(self, author, description):
        self.author = author
        self.description = description
