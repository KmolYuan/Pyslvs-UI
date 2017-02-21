# -*- coding: utf-8 -*-
from .modules import *
from ..dialog.delete import deleteDlg
from .undoRedo import (
    editTableCommand, addStyleCommand, deleteTableCommand, deleteStyleCommand, changePointNumCommand,
    setPathCommand, clearPathCommand, shaftChangeCommand, demoValueCommand)

class Lists():
    def __init__(self, FileState):
        #Lists
        self.PointList = [{'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0}]
        self.LineList = list()
        self.ChainList = list()
        self.ShaftList = list()
        self.SliderList = list()
        self.RodList = list()
        self.ParameterList = list()
        self.data = list()
        self.runList = list()
        self.shaftList = list()
        #FileState
        self.FileState = FileState
    
    def editTable(self, table, name, edit, *Args, **Style):
        isEdit = edit is False
        rowPosition = edit if not isEdit else table.rowCount()
        call = "{} {{{}{}}}".format('Add' if isEdit else 'Edit', name, rowPosition)
        self.FileState.beginMacro(call)
        self.FileState.push(editTableCommand(table, name, edit, Args))
        print(call)
        if name=='Point' and isEdit:
            rowPosition = Style['styleTable'].rowCount()
            self.FileState.push(addStyleCommand(**Style))
            print("- Add style of {{Point{}}}".format(rowPosition))
        if isEdit: table.scrollToBottom()
        self.FileState.endMacro()
    
    def deleteTable(self, table, name, index):
        self.FileState.beginMacro("Delete {{{}{}}}".format(name, index))
        self.FileState.push(deleteTableCommand(table, name, index))
        print("Delete {{{}{}}}".format(name, index))
        self.FileState.endMacro()
    
    def deletePointTable(self, Point, Style, Line, Chain, Shaft, Slider, Rod, Parameter, pos):
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
        call = "Delete {{Point{}}}".format(pos)
        self.FileState.beginMacro(call)
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, pos, lambda x, y: x>y, lambda x: x-1)
        self.FileState.push(deleteStyleCommand(Style, pos))
        self.FileState.push(deleteTableCommand(Point, 'Point', pos))
        print(call)
        self.FileState.endMacro()
    
    def ChangePoint(self, Line, Chain, Shaft, Slider, Rod, prv, next):
        call = "Change {{Point{}}} to {{Point{}}}".format(prv, next)
        self.FileState.beginMacro(call)
        self.replacePoint(Line, Chain, Shaft, Slider, Rod, prv, lambda x, y: x==y, lambda x: next)
        print(call)
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
        call = "Batch move {{{}}}".format(', '.join(['Point{}'.format(i) for i in Points]))
        self.FileState.beginMacro(call)
        for row in Points: self.FileState.push(editTableCommand(table, 'Point', row,
            [str(self.PointList[row]['x']+x), str(self.PointList[row]['y']+y), self.PointList[row]['fix']]))
        print(call)
        print("- Moved ({:+.2f}, {:+.2f})".format(x, y))
        self.FileState.endMacro()
    
    def update(self, table, name):
        lst = list()
        for i in range(table.rowCount()):
            if name=='Point':
                k = dict()
                k['x'] = float(table.item(i, 1).text())
                k['y'] = float(table.item(i, 2).text())
                k['fix'] = bool(table.item(i, 3).checkState())
                try:
                    k['cx'] = float(table.item(i, 4).text().replace('(', '').replace(')', '').split(', ')[0])
                    k['cy'] = float(table.item(i, 4).text().replace('(', '').replace(')', '').split(', ')[1])
                except: pass
            elif name=='Line':
                k = dict()
                k['start'] = int(table.item(i, 1).text().replace('Point', ''))
                k['end'] = int(table.item(i, 2).text().replace('Point', ''))
                k['len'] = float(table.item(i, 3).text())
            elif name=='Chain':
                k = dict()
                k['p1'] = int(table.item(i, 1).text().replace('Point', ''))
                k['p2'] = int(table.item(i, 2).text().replace('Point', ''))
                k['p3'] = int(table.item(i, 3).text().replace('Point', ''))
                k['p1p2'] = float(table.item(i, 4).text())
                k['p2p3'] = float(table.item(i, 5).text())
                k['p1p3'] = float(table.item(i, 6).text())
            elif name=='Shaft':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['ref'] = int(table.item(i, 2).text().replace('Point', ''))
                k['start'] = float(table.item(i, 3).text())
                k['end'] = float(table.item(i, 4).text())
                k['demo'] = float(table.item(i, 5).text())
                k['isParallelogram'] = bool(table.item(i, 6).checkState())
            elif name=='Slider':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['start'] = int(table.item(i, 2).text().replace('Point', ''))
                k['end'] = int(table.item(i, 3).text().replace('Point', ''))
            elif name=='Rod':
                k = dict()
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['start'] = int(table.item(i, 2).text().replace('Point', ''))
                k['end'] = int(table.item(i, 3).text().replace('Point', ''))
                k['pos'] = float(table.item(i, 4).text())
            elif name=='Parameter':
                try:
                    k = {int(table.item(i, 0).text().replace('n', '')):float(table.item(i, 1).text())}
                except: pass
            lst.append(k)
        if name=='Point': self.PointList = lst
        elif name=='Line': self.LineList = lst
        elif name=='Chain': self.ChainList = lst
        elif name=='Shaft': self.ShaftList = lst
        elif name=='Slider': self.SliderList = lst
        elif name=='Rod': self.RodList = lst
        elif name=='Parameter': self.ParameterList = lst
    
    def updateAll(self, Point, Line, Chain, Shaft, Slider, Rod, Parameter):
        self.update(Point, 'Point')
        self.update(Line, 'Line')
        self.update(Chain, 'Chain')
        self.update(Shaft, 'Shaft')
        self.update(Slider, 'Slider')
        self.update(Rod, 'Rod')
        self.update(Parameter, 'Parameter')
    
    def coverageCoordinate(self, table, row):
        coordinate = table.item(row, 4).text()[1:-1].split(', ')
        x = QTableWidgetItem(coordinate[0])
        y = QTableWidgetItem(coordinate[1])
        table.setItem(row, 1, x)
        table.setItem(row, 2, y)
        self.update(table, "Point")
    
    def styleFix(self, table, fix, edit):
        rowPosition = edit
        if fix: fix_set = QTableWidgetItem("10")
        else: fix_set = QTableWidgetItem("5")
        fix_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, fix_set)
    
    def currentPos(self, table, result):
        for i in range(table.rowCount()):
            digit = QTableWidgetItem("("+str(result[i]['x'])+", "+str(result[i]['y'])+")")
            digit.setToolTip("("+str(result[i]['x'])+", "+str(result[i]['y'])+")")
            table.setItem(i, 4, digit)
        self.update(table, "Point")
    
    def setDemo(self, name, row, pos):
        if name=='Shaft': self.ShaftList[row]['demo'] = pos
        elif name=='Rod': self.RodList[row]['pos'] = pos
    def saveDemo(self, table, name, pos, row, column):
        call = "Adjust demo {} {{{}{}}}".format('angle' if name=='Shaft' else 'position', name, row)
        self.FileState.beginMacro(call)
        self.FileState.push(demoValueCommand(table, row, pos, column))
        print(call)
        print("- Moved to ({})".format(str(pos)+' deg' if name=='Shaft' else pos))
        self.FileState.endMacro()
    
    def editParameterTable(self, table):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        name_set = 0
        existNum = list()
        for k in range(rowPosition): existNum += [int(table.item(k, 0).text().replace('n', ''))]
        for i in reversed(range(len(existNum)+1)):
            if not i in existNum: name_set = i
        name_set = QTableWidgetItem('n'+str(name_set))
        name_set.setFlags(Qt.ItemIsEnabled)
        digit_set = QTableWidgetItem("0.0")
        digit_set.setFlags(Qt.ItemIsEnabled)
        commit_set = QTableWidgetItem("Not committed yet.")
        commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, digit_set)
        table.setItem(rowPosition, 2, commit_set)
        self.update(table)
    
    def deleteParameterTable(self, table):
        row = table.currentRow()
        try:
            table.insertRow(row-1)
            for i in range(2):
                name_set = QTableWidgetItem(table.item(row+1, i).text())
                name_set.setFlags(Qt.ItemIsEnabled)
                table.setItem(row-1, i, name_set)
            commit_set = QTableWidgetItem(table.item(row+1, 2).text())
            commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            table.setItem(row-1, 2, commit_set)
            table.removeRow(row+1)
            self.update(table, "Parameter")
        except: pass
    
    def setPath(self, path, runList, shaftList):
        call = "Set {Path}"
        self.FileState.beginMacro(call)
        self.FileState.push(setPathCommand(self.data, self.runList, self.shaftList, path, runList, shaftList))
        print(call)
        self.FileState.endMacro()
    
    def clearPath(self):
        call = "Clear {Path}"
        self.FileState.beginMacro(call)
        self.FileState.push(clearPathCommand(self.data, self.runList, self.shaftList))
        print(call)
        self.FileState.endMacro()
    
    def shaftChange(self, table, prv, next):
        call = "Change {{Shaft{}}} to {{Shaft{}}}".format(prv, next)
        self.FileState.beginMacro(call)
        self.FileState.push(shaftChangeCommand(self.shaftList, table, prv, next))
        print(call)
        self.FileState.endMacro()

class PathSolvingReqs():
    def __init__(self, FileState):
        self.list = list()
        self.result = list()
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
