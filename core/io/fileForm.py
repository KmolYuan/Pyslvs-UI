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
    
    '''
    def Generate_Merge(self, row, startAngle, endAngle, answer, Paths, Point, Link, Chain, Shaft):
        if not (False in answer):
            Result = self.Designs.result[row]
            links_tag = Result['mechanismParams']['Link'].split(',')
            print('Mechanism:\n'+'\n'.join(["{}: {}".format(tag, Result[tag]) for tag in (['Ax', 'Ay', 'Dx', 'Dy']+links_tag)]))
            expression = Result['mechanismParams']['Expression'].split(',')
            expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
            expression_result = [exp[-1] for exp in expression_tag]
            for i, (x, y) in enumerate(answer):
                self.Lists.editTable(Point, False, round(x, 4), round(y, 4), i<2, 'Blue' if i<2 else 'Green' if i<len(answer)-1 else 'Brick-Red')
            Rnum = Point.rowCount()-len(expression_result)
            self.Lists.editTable(Link, False, "Point{}".format(Rnum-2), "Point{}".format(Rnum), str(Result['L0']))
            #exp = ('B', 'L2', 'L1', 'C', 'D')
            for i, exp in enumerate(expression_tag[1:]):
                p1 = -2 if exp[0]=='A' else expression_result.index(exp[0]) if exp[0] in expression_result else -1
                p2 = -2 if exp[3]=='A' else expression_result.index(exp[3]) if exp[3] in expression_result else -1
                p3 = -2 if exp[-1]=='A' else expression_result.index(exp[-1]) if exp[-1] in expression_result else -1
                self.Lists.editTable(Link, False, "Point{}".format(Rnum+p1), "Point{}".format(Rnum+p3), str(Result[exp[1]]))
                self.Lists.editTable(Link, False, "Point{}".format(Rnum+p2), "Point{}".format(Rnum+p3), str(Result[exp[2]]))
            self.Lists.editTable(Shaft, False, "Point{}".format(Rnum-2), "Point{}".format(Rnum), startAngle, endAngle, startAngle, False)
            print("Generate Result Merged. At: {} deg ~ {} deg.".format(startAngle, endAngle))
            return True
        else:
            return False
    '''
