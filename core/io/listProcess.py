# -*- coding: utf-8 -*-
from ..QtModules import *
from collections import defaultdict
from ..dialog.delete import deleteDlg
from .undoRedo import (
    editTableCommand, addStyleCommand, deleteTableCommand, deleteStyleCommand, changePointNumCommand,
    setPathCommand, clearPathCommand, shaftChangeCommand, demoValueCommand, TSCommand)

class Lists():
    def __init__(self, FileState):
        #Lists
        self.PointList = [{'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0}]
        self.LineList = list()
        self.ChainList = list()
        self.ShaftList = list()
        self.SliderList = list()
        self.RodList = list()
        self.ParameterList = defaultdict(lambda: 0., dict())
        self.data = list()
        self.runList = list()
        self.shaftList = list()
        #FileState
        self.FileState = FileState
    
    def editTable(self, table, name, edit, *Args, **Style):
        isEdit = not edit is False
        rowPosition = edit if isEdit else table.rowCount()
        self.FileState.beginMacro("{}{} {{{}{}}}".format('Add' if not isEdit else 'Edit', ' parameter' if name=='n' else '', name, rowPosition))
        self.FileState.push(editTableCommand(table, name, edit, Args))
        if name=='Point' and not isEdit:
            rowPosition = Style['styleTable'].rowCount()
            self.FileState.push(addStyleCommand(**Style))
            print("- Add style of {{Point{}}}".format(rowPosition))
        if not isEdit: table.scrollToBottom()
        self.FileState.endMacro()
    
    def deleteTable(self, table, name, index, isRename=True):
        self.FileState.beginMacro("Delete {{{}{}}}".format(name, index))
        self.FileState.push(deleteTableCommand(table, name, index, isRename))
        self.FileState.endMacro()
    
    def deletePointTable(self, Point, Style, Line, Chain, Shaft, Slider, Rod, pos):
        #Associated items
        if 'Point{}'.format(pos) in self.runList: self.clearPath()
        for e in self.LineList:
            if pos in [e['start'], e['end']]: self.deleteTable(Line, 'Line', self.LineList.index(e))
        for e in self.ChainList:
            if pos in [e['p1'], e['p2'], e['p3']]: self.deleteTable(Chain, 'Chain', self.ChainList.index(e))
        for e in self.ShaftList:
            if pos in [e['cen'], e['ref']]: self.deleteTable(Shaft, 'Shaft', self.ShaftList.index(e))
        for e in self.SliderList:
            if pos in [e['cen'], e['start'], e['end']]: self.deleteTable(Slider, 'Slider', self.SliderList.index(e))
        for e in self.RodList:
            if pos in [e['cen'], e['start'], e['end']]: self.deleteTable(Rod, 'Rod', self.RodList.index(e))
        #Change Number and Delete Point
        self.FileState.beginMacro("Delete {{Point{}}}".format(pos))
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, pos, lambda x, y: x>y, lambda x: x-1)
        self.FileState.push(deleteStyleCommand(Style, pos))
        self.FileState.push(deleteTableCommand(Point, 'Point', pos))
        self.FileState.endMacro()
    
    def ChangePoint(self, Line, Chain, Shaft, Slider, Rod, prv, next):
        self.FileState.beginMacro("Change {{Point{}}} to {{Point{}}}".format(prv, next))
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, prv, lambda x, y: x==y, lambda x: next)
        self.FileState.endMacro()
    
    def replacePoint(self, Line, Chain, Shaft, Slider, Rod, pos, Judgment, toNew):
        for e in self.LineList:
            row = self.LineList.index(e)
            if Judgment(e['start'], pos): self.FileState.push(changePointNumCommand(Line, toNew(e['start']), row, 1))
            if Judgment(e['end'], pos): self.FileState.push(changePointNumCommand(Line, toNew(e['end']), row, 2))
        for e in self.ChainList:
            row = self.ChainList.index(e)
            if Judgment(e['p1'], pos): self.FileState.push(changePointNumCommand(Chain, toNew(e['p1']), row, 1))
            if Judgment(e['p2'], pos): self.FileState.push(changePointNumCommand(Chain, toNew(e['p2']), row, 2))
            if Judgment(e['p3'], pos): self.FileState.push(changePointNumCommand(Chain, toNew(e['p3']), row, 3))
        for e in self.ShaftList:
            row = self.ShaftList.index(e)
            if Judgment(e['cen'], pos): self.FileState.push(changePointNumCommand(Shaft, toNew(e['cen']), row, 1))
            if Judgment(e['ref'], pos): self.FileState.push(changePointNumCommand(Shaft, toNew(e['ref']), row, 2))
        for e in self.SliderList:
            row = self.SliderList.index(e)
            if Judgment(e['cen'], pos): self.FileState.push(changePointNumCommand(Slider, toNew(e['cen']), row, 1))
            if Judgment(e['start'], pos): self.FileState.push(changePointNumCommand(Slider, toNew(e['start']), row, 2))
            if Judgment(e['end'], pos): self.FileState.push(changePointNumCommand(Slider, toNew(e['end']), row, 3))
        for e in self.RodList:
            row = self.RodList.index(e)
            if Judgment(e['cen'], pos): self.FileState.push(changePointNumCommand(Rod, toNew(e['cen']), row, 1))
            if Judgment(e['start'], pos): self.FileState.push(changePointNumCommand(Rod, toNew(e['start']), row, 2))
            if Judgment(e['end'], pos): self.FileState.push(changePointNumCommand(Rod, toNew(e['end']), row, 3))
    
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
    
    def lineNodeReversion(self, table, row):
        start = self.PointList[self.LineList[row]['start']]
        end = self.PointList[self.LineList[row]['end']]
        if end['fix']==False:
            x = str(end['x'])
            y = str(end['y']-2*(end['y']-start['y']))
            self.editTable(table, 'Point', self.LineList[row]['end'], x, y, False)
        elif start['fix']==False:
            x = str(start['x'])
            y = str(start['y']-2*(start['y']-end['y']))
            self.editTable(table, 'Point', self.LineList[row]['start'], x, y, False)
    
    def batchMove(self, table, x, y, Points):
        self.FileState.beginMacro("Batch move {{{}}}".format(', '.join(['Point{}'.format(i) for i in Points])))
        for row in Points: self.FileState.push(editTableCommand(table, 'Point', row,
            [str(self.PointList[row]['x']+x), str(self.PointList[row]['y']+y), self.PointList[row]['fix']]))
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
        lst = list() if not name=='Parameter' else defaultdict(lambda: 0., dict())
        for i in range(table.rowCount()):
            if name=='Parameter': lst[int(table.item(i, 0).text().replace('n', ''))] = float(table.item(i, 1).text())
            elif name=='Point':
                k = dict()
                k['x'] = self.toFloat(table.item(i, 1).text())
                k['y'] = self.toFloat(table.item(i, 2).text())
                k['fix'] = bool(table.item(i, 3).checkState())
                try:
                    k['cx'] = float(table.item(i, 4).text().replace('(', str()).replace(')', str()).split(', ')[0])
                    k['cy'] = float(table.item(i, 4).text().replace('(', str()).replace(')', str()).split(', ')[1])
                except: pass
            elif name=='Line':
                k = dict()
                k['start'] = int(table.item(i, 1).text().replace('Point', str()))
                k['end'] = int(table.item(i, 2).text().replace('Point', str()))
                k['len'] = self.toFloat(table.item(i, 3).text())
            elif name=='Chain':
                k = dict()
                k['p1'] = int(table.item(i, 1).text().replace('Point', str()))
                k['p2'] = int(table.item(i, 2).text().replace('Point', str()))
                k['p3'] = int(table.item(i, 3).text().replace('Point', str()))
                k['p1p2'] = self.toFloat(table.item(i, 4).text())
                k['p2p3'] = self.toFloat(table.item(i, 5).text())
                k['p1p3'] = self.toFloat(table.item(i, 6).text())
            elif name=='Shaft':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', str()))
                k['ref'] = int(table.item(i, 2).text().replace('Point', str()))
                k['start'] = float(table.item(i, 3).text())
                k['end'] = float(table.item(i, 4).text())
                k['demo'] = float(table.item(i, 5).text())
                k['isParallelogram'] = bool(table.item(i, 6).checkState())
            elif name=='Slider':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', str()))
                k['start'] = int(table.item(i, 2).text().replace('Point', str()))
                k['end'] = int(table.item(i, 3).text().replace('Point', str()))
            elif name=='Rod':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', str()))
                k['start'] = int(table.item(i, 2).text().replace('Point', str()))
                k['end'] = int(table.item(i, 3).text().replace('Point', str()))
                k['pos'] = float(table.item(i, 4).text())
            if not name=='Parameter': lst.append(k)
        if name=='Parameter': self.ParameterList = lst
        elif name=='Point': self.PointList = lst
        elif name=='Line': self.LineList = lst
        elif name=='Chain': self.ChainList = lst
        elif name=='Shaft': self.ShaftList = lst
        elif name=='Slider': self.SliderList = lst
        elif name=='Rod': self.RodList = lst
    
    def toFloat(self, p): return self.ParameterList[int(p.replace('n', ''))] if 'n' in p else float(p)
    
    def coverageCoordinate(self, table, row):
        e = self.PointList[row]
        self.editTable(table, 'Point', row, str(e['cx']), str(e['cy']), e['fix'])
    
    def styleFix(self, table, fix, edit):
        rowPosition = edit
        if fix: fix_set = QTableWidgetItem('10')
        else: fix_set = QTableWidgetItem('5')
        fix_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, fix_set)
    
    def currentPos(self, table, result):
        for i in range(table.rowCount()):
            name = "({}, {})".format(result[i]['x'], result[i]['y'])
            digit = QTableWidgetItem(name)
            digit.setToolTip(name)
            table.setItem(i, 4, digit)
        self.update(table, 'Point')
    
    def setDemo(self, name, row, pos):
        if name=='Shaft': self.ShaftList[row]['demo'] = pos
        elif name=='Rod': self.RodList[row]['pos'] = pos
    def saveDemo(self, table, name, pos, row, column):
        self.FileState.beginMacro("Adjust demo {} {{{}{}}}".format('angle' if name=='Shaft' else 'position', name, row))
        self.FileState.push(demoValueCommand(table, row, pos, column))
        print("- Moved to ({})".format(str(pos)+' deg' if name=='Shaft' else pos))
        self.FileState.endMacro()
    
    def setPath(self, path, runList, shaftList):
        self.FileState.beginMacro("Set {Path}")
        self.FileState.push(setPathCommand(self.data, self.runList, self.shaftList, path, runList, shaftList))
        self.FileState.endMacro()
    
    def clearPath(self):
        self.FileState.beginMacro("Clear {Path}")
        self.FileState.push(clearPathCommand(self.data, self.runList, self.shaftList))
        self.FileState.endMacro()
    
    def shaftChange(self, table, prv, next):
        self.FileState.beginMacro("Change {{Shaft{}}} to {{Shaft{}}}".format(prv, next))
        self.FileState.push(shaftChangeCommand(self.shaftList, table, prv, next))
        self.FileState.endMacro()

class Designs():
    def __init__(self, FileState):
        self.list = list()
        self.result = list()
        self.TSDirections = list()
        self.FileState = FileState
    
    def add(self, x, y): self.list.append({'x':x, 'y':y})
    def remove(self, pos): del self.list[pos]
    def resultMerge(self, result): self.result += result
    def removeResult(self, pos): del self.result[pos]
    def moveUP(self, row):
        if row>0 and len(self.list)>1:
            self.list.insert(row-1, {'x':self.list[row]['x'], 'y':self.list[row]['y']})
            del self.list[row+1]
    def moveDown(self, row):
        if row<len(self.list)-1 and len(self.list)>1:
            self.list.insert(row+2, {'x':self.list[row]['x'], 'y':self.list[row]['y']})
            del self.list[row]
    
    def addDirections(self, Direction):
        self.FileState.beginMacro("TS Direction changed")
        self.FileState.push(TSCommand(self.TSDirections, Direction))
        self.FileState.endMacro()
