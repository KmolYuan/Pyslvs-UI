# -*- coding: utf-8 -*-
from .modules import *
from ..panel.delete import deleteDlg
from .undoRedo import (
    editTableCommand, styleAddCommand, deleteTableCommand,
    setPathCommand)

class Lists():
    def __init__(self, FileState):
        #Lists
        self.PointList = [{'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0}]
        self.LineList = list()
        self.ChainList = list()
        self.ShaftList = list()
        self.currentShaft = 0
        self.SliderList = list()
        self.RodList = list()
        self.ParameterList = list()
        #FileState
        self.FileState = FileState
    
    def editTable(self, table, name, edit, *Args, **Style):
        rowPosition = edit if edit else table.rowCount()
        self.FileState.beginMacro("{} {{{}{}}}".format('Add' if edit==False else 'Edit', name, rowPosition))
        self.FileState.push(editTableCommand(table, name, edit, Args))
        print("{} {{{}{}}}.".format("Add" if edit is False else "Edit", name, rowPosition))
        if name=='Point' and edit==False:
            rowPosition = Style['styleTable'].rowCount()
            self.FileState.push(styleAddCommand(Style))
            print("- Add style of {{Point{}}}.".format(rowPosition))
        self.FileState.endMacro()
        self.update(table, name)
    
    def deleteTable(self, table, name, index):
        self.FileState.beginMacro("Delete {{{}{}}}".format(name, index))
        self.FileState.push(deleteTableCommand(table, name, index))
        self.FileState.endMacro()
        self.update(table, name)
    
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
    
    def deletePointTable(self, tablePoint, tableStyle, tableLine, tableChain, tableShaft, tableSlider, tableRod, pos):
        for i in range(tableLine.rowCount()):
            if (pos==tableLine.item(i, 1).text()) or (pos==tableLine.item(i, 2).text()):
                tableLine.removeRow(i)
                for j in range(i, tableLine.rowCount()): tableLine.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
                break
        for i in range(tableChain.rowCount()):
            if (pos==tableChain.item(i, 1).text()) or (pos==tableChain.item(i, 2).text()):
                tableChain.removeRow(i)
                for j in range(i, tableChain.rowCount): tableChain.setItem(j, 0, QTableWidgetItem("Chain"+str(j)))
                break
        for i in range(tableShaft.rowCount()):
            if (pos==tableShaft.item(i, 1).text()) or (pos==tableShaft.item(i, 2).text()):
                tableShaft.removeRow(i)
                for j in range(i, tableShaft.rowCount()): tableShaft.setItem(j, 0, QTableWidgetItem("Shaft"+str(j)))
                break
        for i in range(tableSlider.rowCount()):
            if (pos==tableSlider.item(i, 1).text()):
                tableSlider.removeRow(i)
                for j in range(i, tableSlider.rowCount()): tableSlider.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
                break
        for i in range(tableRod.rowCount()):
            if (pos==tableRod.item(i, 1).text()) or (pos==tableRod.item(i, 2).text()):
                tableRod.removeRow(i)
                for j in range(i, tableRod.rowCount()): tableRod.setItem(j, 0, QTableWidgetItem("Rod"+str(j)))
                break
        for i in range(1, tablePoint.rowCount()):
            if (pos==tablePoint.item(i, 0).text()):
                tablePoint.removeRow(i)
                tableStyle.removeRow(i)
                for j in range(i, tablePoint.rowCount()): tablePoint.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
                for j in range(i, tablePoint.rowCount()): tableStyle.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
                break
        self.update(tablePoint, "Point")
    
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
    
    def setDemo(self, table, index, angle):
        table.setItem(index, 5, QTableWidgetItem(str(angle)))
        self.ShaftList[index]['demo'] = angle
    
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

class Path():
    def __init__(self, FileState):
        self.data = list()
        self.runList = list()
        self.shaftList = list()
        self.FileState = FileState
    
    def setPath(self, path, runList, shaftList):
        self.FileState.beginMacro("Set {Path}")
        self.FileState.push(setPathCommand(self.data, self.runList, self.shaftList, path, runList, shaftList))
        print("Set {Path}")
        self.FileState.endMacro()
    
    def shaftChange(self, prv, next):
        try: self.shaftList[self.shaftList.index(prv)] = 'next'
        except: pass
        try: self.shaftList[self.shaftList.index(next)] = 'prv'
        except: pass
        for i in range(len(self.shaftList)):
            if self.shaftList[i]=='next': self.shaftList[i] = next
            if self.shaftList[i]=='prv': self.shaftList[i] = prv

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
