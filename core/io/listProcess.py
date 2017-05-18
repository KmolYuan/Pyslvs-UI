# -*- coding: utf-8 -*-
from ..QtModules import *
from .elements import VPoint, VLine, VChain, VShaft, VSlider, VRod, VParameter
from collections import defaultdict
from math import sqrt, acos, degrees
from .undoRedo import (editTableCommand, deleteTableCommand, changePointNumCommand,
    setPathCommand, clearPathCommand, demoValueCommand, TSinitCommand)

class Lists:
    def __init__(self, FileState):
        #Lists
        self.PointList = [VPoint(fix=True)]
        self.LineList = list()
        self.ChainList = list()
        self.ShaftList = list()
        self.SliderList = list()
        self.RodList = list()
        self.ParameterList = defaultdict(lambda: 0., dict())
        #Path
        self.pathData = list()
        #FileState
        self.FileState = FileState
        #Cosine Theorem
        self.CosineTheoremAngle = lambda a, b, c: acos(float(b**2+c**2-a**2)/(float(2*b*c) if float(2*b*c)!=0 else 0.01))
        self.CosineTheoremAngleE = lambda a, b, c: acos(min(1, max(float(b**2+c**2-a**2)/(float(2*b*c) if float(2*b*c)!=0 else 0.01), -1)))
    
    def editTable(self, table, name, edit, *Args):
        isEdit = not edit is False
        rowPosition = edit if isEdit else table.rowCount()
        self.FileState.beginMacro("{}{} {{{}{}}}".format('Add' if not isEdit else 'Edit', ' parameter' if name=='n' else '', name, rowPosition))
        self.FileState.push(editTableCommand(table, name, edit, Args))
        if not isEdit: table.scrollToBottom()
        self.FileState.endMacro()
    
    def deleteTable(self, table, name, index, isRename=True):
        self.FileState.beginMacro("Delete {{{}{}}}".format(name, index))
        self.FileState.push(deleteTableCommand(table, name, index, isRename))
        self.FileState.endMacro()
    
    def deletePointTable(self, Point, Line, Chain, Shaft, Slider, Rod, pos):
        #Associated items
        n = False
        for paths in [e.paths for e in self.pathData]:
            for path in paths:
                if path.point>=pos: n = True
        if n: self.clearPath()
        for e in self.LineList:
            if pos in [e.start, e.end]: self.deleteTable(Line, 'Line', self.LineList.index(e))
        for e in self.ChainList:
            if pos in [e.p1, e.p2, e.p3]: self.deleteTable(Chain, 'Chain', self.ChainList.index(e))
        for e in self.ShaftList:
            if pos in [e.cen, e.ref]: self.deleteTable(Shaft, 'Shaft', self.ShaftList.index(e))
        for e in self.SliderList:
            if pos in [e.cen, e.start, e.end]: self.deleteTable(Slider, 'Slider', self.SliderList.index(e))
        for e in self.RodList:
            if pos in [e.cen, e.start, e.end]: self.deleteTable(Rod, 'Rod', self.RodList.index(e))
        #Change Number and Delete Point
        self.FileState.beginMacro("Delete {{Point{}}}".format(pos))
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, pos, lambda x, y: x>y, lambda x: x-1)
        self.FileState.push(deleteTableCommand(Point, 'Point', pos))
        self.FileState.endMacro()
    
    def ChangePoint(self, Line, Chain, Shaft, Slider, Rod, prv, next):
        self.FileState.beginMacro("Change {{Point{}}} to {{Point{}}}".format(prv, next))
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, prv, lambda x, y: x==y, lambda x: next)
        self.FileState.endMacro()
    
    def replacePoint(self, Line, Chain, Shaft, Slider, Rod, pos, Judgment, toNew):
        for e in self.LineList:
            row = self.LineList.index(e)
            if Judgment(e.start, pos): self.FileState.push(changePointNumCommand(Line, toNew(e.start), row, 1))
            if Judgment(e.end, pos): self.FileState.push(changePointNumCommand(Line, toNew(e.end), row, 2))
        for e in self.ChainList:
            row = self.ChainList.index(e)
            if Judgment(e.p1, pos): self.FileState.push(changePointNumCommand(Chain, toNew(e.p1), row, 1))
            if Judgment(e.p2, pos): self.FileState.push(changePointNumCommand(Chain, toNew(e.p2), row, 2))
            if Judgment(e.p3, pos): self.FileState.push(changePointNumCommand(Chain, toNew(e.p3), row, 3))
        for e in self.ShaftList:
            row = self.ShaftList.index(e)
            if Judgment(e.cen, pos): self.FileState.push(changePointNumCommand(Shaft, toNew(e.cen), row, 1))
            if Judgment(e.ref, pos): self.FileState.push(changePointNumCommand(Shaft, toNew(e.ref), row, 2))
        for e in self.SliderList:
            row = self.SliderList.index(e)
            if Judgment(e.cen, pos): self.FileState.push(changePointNumCommand(Slider, toNew(e.cen), row, 1))
            if Judgment(e.start, pos): self.FileState.push(changePointNumCommand(Slider, toNew(e.start), row, 2))
            if Judgment(e.end, pos): self.FileState.push(changePointNumCommand(Slider, toNew(e.end), row, 3))
        for e in self.RodList:
            row = self.RodList.index(e)
            if Judgment(e.cen, pos): self.FileState.push(changePointNumCommand(Rod, toNew(e.cen), row, 1))
            if Judgment(e.start, pos): self.FileState.push(changePointNumCommand(Rod, toNew(e.start), row, 2))
            if Judgment(e.end, pos): self.FileState.push(changePointNumCommand(Rod, toNew(e.end), row, 3))
    
    def deleteParameterTable(self, table, Point, Line, Chain, pos):
        self.FileState.beginMacro("Delete parameter {{n{}}}".format(pos))
        self.replaceDigit(Point, pos, 1, 2)
        self.replaceDigit(Line, pos, 3)
        self.replaceDigit(Chain, pos, 4, 5, 6)
        self.FileState.push(deleteTableCommand(table, 'n', table.currentRow(), False))
        self.FileState.endMacro()
    
    def replaceDigit(self, table, pos, *column):
        for row in range(table.rowCount()):
            for k in column:
                if table.item(row, k).text()=='n{}'.format(pos): self.FileState.push(changePointNumCommand(table, self.ParameterList[pos], row, k, 'n'))
    
    def batchMove(self, table, x, y, Points):
        self.FileState.beginMacro("Batch move {{{}}}".format(', '.join(['Point{}'.format(i) for i in Points])))
        for row in Points: self.FileState.push(editTableCommand(table, 'Point', row,
            [str(self.PointList[row].x+x), str(self.PointList[row].y+y), self.PointList[row].fix]))
        print("- Moved ({:+.2f}, {:+.2f})".format(x, y))
        self.FileState.endMacro()
    
    def updateAll(self, Point, Line, Chain, Shaft, Slider, Rod, Parameter):
        self.update(Parameter, 'Parameter')
        self.update(Point, 'Point')
        self.update(Line, 'Line')
        self.update(Chain, 'Chain')
        self.update(Shaft, 'Shaft')
        self.update(Slider, 'Slider')
        self.update(Rod, 'Rod')
    
    def update(self, table, name):
        lst = list() if name!='Parameter' else defaultdict(lambda: 0., dict())
        for i in range(table.rowCount()):
            if name=='Parameter':
                k = {int(table.item(i, 0).text().replace('n', '')):
                    VParameter(float(table.item(i, 1).text()), table.item(i, 2).text())}
            elif name=='Point':
                k = VPoint(self.toFloat(table.item(i, 1).text()),
                    self.toFloat(table.item(i, 2).text()),
                    bool(table.item(i, 3).checkState()),
                    table.item(i, 4).text())
                try: k.move(float(table.item(i, 5).text().replace('(', str()).replace(')', str()).split(', ')[0]),
                    float(table.item(i, 5).text().replace('(', str()).replace(')', str()).split(', ')[1]))
                except: pass
            elif name=='Line':
                k = VLine(int(table.item(i, 1).text().replace('Point', str())),
                    int(table.item(i, 2).text().replace('Point', str())),
                    self.toFloat(table.item(i, 3).text()))
            elif name=='Chain':
                k = VChain(int(table.item(i, 1).text().replace('Point', str())),
                    int(table.item(i, 2).text().replace('Point', str())),
                    int(table.item(i, 3).text().replace('Point', str())),
                    self.toFloat(table.item(i, 4).text()),
                    self.toFloat(table.item(i, 5).text()),
                    self.toFloat(table.item(i, 6).text()))
            elif name=='Shaft':
                k = VShaft(int(table.item(i, 1).text().replace('Point', str())),
                    int(table.item(i, 2).text().replace('Point', str())),
                    float(table.item(i, 3).text()),
                    float(table.item(i, 4).text()),
                    float(table.item(i, 5).text()))
            elif name=='Slider':
                k = VSlider(int(table.item(i, 1).text().replace('Point', str())),
                    int(table.item(i, 2).text().replace('Point', str())),
                    int(table.item(i, 3).text().replace('Point', str())))
            elif name=='Rod':
                k = VRod(int(table.item(i, 1).text().replace('Point', str())),
                    int(table.item(i, 2).text().replace('Point', str())),
                    int(table.item(i, 3).text().replace('Point', str())),
                    float(table.item(i, 4).text()))
            if name!='Parameter': lst.append(k)
            else: lst.update(k)
        if name=='Parameter': self.ParameterList = lst
        elif name=='Point': self.PointList = lst
        elif name=='Line': self.LineList = lst
        elif name=='Chain': self.ChainList = lst
        elif name=='Shaft': self.ShaftList = lst
        elif name=='Slider': self.SliderList = lst
        elif name=='Rod': self.RodList = lst
    
    def toFloat(self, p): return float(self.ParameterList[int(p.replace('n', ''))].val if 'n' in p else p)
    
    def coverageCoordinate(self, table):
        for i, e in enumerate(self.PointList[1:]):
            cx = e.cx if e.fix else float(round(e.cx))
            cy = e.cy if e.fix else float(round(e.cy))
            self.editTable(table, 'Point', i+1, cx, cy, e.fix)
    
    def currentPos(self, table, result):
        for i in range(table.rowCount()):
            name = "({}, {})".format(result[i]['x'], result[i]['y'])
            digit = QTableWidgetItem(name)
            digit.setToolTip(name)
            table.setItem(i, 5, digit)
        self.update(table, 'Point')
    
    def link2Shaft(self, table, row):
        cen = self.LineList[row].start
        ref = self.LineList[row].end
        self.editTable(table, 'Shaft', False, cen, ref, 0., 360., self.m(cen, ref), False)
    
    def setDemo(self, name, row, pos):
        if name=='Shaft': self.ShaftList[row].demo = pos
        elif name=='Rod': self.RodList[row].pos = pos
    def saveDemo(self, table, name, pos, row, column):
        self.FileState.beginMacro("Adjust demo {} {} {{{}{}}}".format('angle' if name=='Shaft' else 'position', pos, name, row))
        self.FileState.push(demoValueCommand(table, row, pos, column))
        print("- Moved to ({})".format(str(pos)+' deg' if name=='Shaft' else pos))
        self.FileState.endMacro()
    
    def setPath(self, path):
        self.FileState.beginMacro("Set {Path}")
        self.FileState.push(setPathCommand(self.pathData, path))
        self.FileState.endMacro()
    
    def clearPath(self):
        self.FileState.beginMacro("Clear {Path}")
        self.FileState.push(clearPathCommand(self.pathData))
        self.FileState.endMacro()
    
    def m(self, p1, p2):
        p1 = int(p1.replace('Point', '')) if type(p1)==str else p1
        p2 = int(p2.replace('Point', '')) if type(p2)==str else p2
        x1 = self.PointList[p1].cx
        y1 = self.PointList[p1].cy
        x2 = self.PointList[p2].cx
        y2 = self.PointList[p2].cy
        x = x2-x1
        y = y2-y1
        d = sqrt(x**2+y**2)
        try: angle = self.CosineTheoremAngle(y, x, d)
        except ValueError: angle = self.CosineTheoremAngleE(y, x, d)
        return '{:.02f}'.format(360.-degrees(angle) if y<0 else degrees(angle))

class Designs():
    def __init__(self, FileState):
        self.path = list()
        self.result = list()
        self.TSDirections = list()
        self.FileState = FileState
    
    def setPath(self, path): self.path = path
    def addResult(self, result): self.result = result
    def add(self, x, y): self.path.append({'x':x, 'y':y})
    def remove(self, pos): del self.path[pos]
    def removeResult(self, pos): del self.result[pos]
    def moveUP(self, row):
        if row>0 and len(self.path)>1:
            self.path.insert(row-1, {'x':self.path[row]['x'], 'y':self.path[row]['y']})
            del self.path[row+1]
    def moveDown(self, row):
        if row<len(self.path)-1 and len(self.path)>1:
            self.path.insert(row+2, {'x':self.path[row]['x'], 'y':self.path[row]['y']})
            del self.path[row]
    
    def setDirections(self, Direction):
        self.FileState.beginMacro("Input {TS Direction}")
        self.FileState.push(TSinitCommand(self.TSDirections, Direction))
        self.FileState.endMacro()
