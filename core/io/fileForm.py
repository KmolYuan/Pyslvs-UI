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

class Designs():
    __slots__ = ('path', 'result', 'TSDirections', 'FileState')
    
    def __init__(self, FileState):
        self.path = []
        self.result = []
        self.TSDirections = []
        self.FileState = FileState
    
    def setPath(self, path):
        self.path = path
    def addResult(self, result):
        self.result = result
    def add(self, x, y):
        self.path.append({'x':x, 'y':y})
    def remove(self, pos):
        del self.path[pos]
    def removeResult(self, pos):
        del self.result[pos]
    def moveUP(self, row):
        if row>0 and len(self.path)>1:
            self.path.insert(row-1, {'x':self.path[row]['x'], 'y':self.path[row]['y']})
            del self.path[row+1]
    def moveDown(self, row):
        if row<len(self.path)-1 and len(self.path)>1:
            self.path.insert(row+2, {'x':self.path[row]['x'], 'y':self.path[row]['y']})
            del self.path[row]
    
    def setDirections(self, direction):
        self.FileState.beginMacro("Input {TS Direction}")
        self.FileState.push(TSinitCommand(self.TSDirections, direction))
        self.FileState.endMacro()

class Form:
    __slots__ = ('fileName', 'description', 'author', 'lastTime', 'changed', 'Stack')
    
    def __init__(self):
        self.fileName = QFileInfo('[New Workbook]')
        self.description = ""
        self.author = 'Anonymous'
        self.lastTime = timeNow()
        self.changed = False
        self.Stack = 0

class File:
    __slots__ = ('FileState', 'args', 'pathData', 'Designs', 'Script', 'form')
    
    def __init__(self, FileState, args):
        self.FileState = FileState
        self.args = args
        self.resetAllList()
    
    def resetAllList(self):
        self.pathData = []
        self.Designs = Designs(self.FileState)
        self.Script = ""
        self.form = Form()
        self.FileState.clear()
    def updateTime(self):
        self.form.lastTime = timeNow()
    def updateAuthorDescription(self, author, description):
        self.form.author = author
        self.form.description = description
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
    '''
    def TS_Merge(self, answers, Point, Link, Chain, Slider):
        Pythagorean = lambda p1, p2: ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**(1/2)
        pNums = []
        for i, answer in enumerate(answers):
            pNum = dict()
            direction = self.Designs.TSDirections[i]
            #New Points
            for p in ['p1', 'p2', 'p3']:
                if type(direction.get(p))==tuple:
                    self.Lists.editTable(Point, False, direction.get(p)[0], direction.get(p)[1], False, 'Green')
                    pNum[p] = Point.rowCount()-1
            if len(answer)==2:
                self.Lists.editTable(Point, False, answer[0], answer[1], False, 'Green')
            elif len(answer)==3:
                if type(direction.get('p3'))==tuple:
                    self.Lists.editTable(Point, False, direction.p3[0], direction.p3[1], False, 'Green')
            pNum['answer'] = Point.rowCount()-1
            pNums.append(pNum)
            #Number of Points & Length of Sides
            p1 = int(direction.p1.replace('Point', '')) if type(direction.p1)==str else pNums[direction.p1]['answer'] if type(direction.p1)==int else pNum['p1']
            p2 = int(direction.p2.replace('Point', '')) if type(direction.p2)==str else pNums[direction.p2]['answer'] if type(direction.p2)==int else pNum['p2']
            if direction.Type in ['PLPP', 'PPP']:
                p3 = int(direction.p3.replace('Point', '')) if type(direction.p3)==str else pNums[direction.p3]['answer'] if type(direction.p3)==int else pNum['p3']
            if direction.Type in ['PLAP', 'PLLP', 'PLPP']:
                pA = pNum['answer']
            #Merge options
            table_points = self.Lists.PointList
            if direction.Type in ['PLAP', 'PLLP']:
                if direction.merge==1:
                    self.Lists.editTable(Link, False, p1, pA, str(direction.len1))
                elif direction.merge==2:
                    self.Lists.editTable(Link, False, p2, pA, str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
                elif direction.merge==3:
                    self.Lists.editTable(Chain, False, p1, pA, p2,
                        str(direction.len1),
                        str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))),
                        str(Pythagorean(table_points[p1], table_points[p2]))
                    )
                elif direction.merge==4:
                    self.Lists.editTable(Link, False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Link, False, p2, pA,
                        str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
            elif direction.Type=='PPP':
                if direction.merge==1:
                    self.Lists.editTable(Link, False, p1, p3, answer[2])
                elif direction.merge==2:
                    self.Lists.editTable(Link, False, p2, p3, answer[1])
                elif direction.merge==3:
                    self.Lists.editTable(Chain, False, p1, p2, p3, answer[0], answer[1], answer[2])
                elif direction.merge==4:
                    self.Lists.editTable(Link, False, p1, p3, answer[2])
                    self.Lists.editTable(Link, False, p2, p3, answer[1])
            elif direction.Type=='PLPP':
                if direction.merge==1:
                    self.Lists.editTable(Link, False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Slider, False, pA, p2, p3)
    '''
