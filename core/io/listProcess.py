# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.color import colorlist, colorName
from .undoRedo import *

class Lists():
    def __init__(self, FileState):
        #Lists
        self.PointList = [{'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0}]
        self.style = [{'cen':'Red', 'ring':10, 'color':'Red'}]
        self.LineList = list()
        self.ChainList = list()
        self.ShaftList = list()
        self.currentShaft = 0
        self.SliderList = list()
        self.RodList = list()
        self.ParameterList = list()
        #FileState
        self.FileState = FileState
    
    def editTable(self, table, name, edit, *Args):
        rowPosition = edit if edit else table.rowCount()
        if edit is False: table.insertRow(rowPosition)
        name_set = QTableWidgetItem("{}{}".format(name, rowPosition))
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        for i in range(len(Args)):
            if type(Args[i])==str: table.setItem(rowPosition, i+1, QTableWidgetItem(Args[i]))
            elif type(Args[i])==bool:
                checkbox = QTableWidgetItem("")
                checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                checkbox.setCheckState(Qt.Checked if Args[i] else Qt.Unchecked)
                table.setItem(rowPosition, i+1, checkbox)
        self.update(table, name)
        print(("Add" if edit is False else "Edit")+" {}{}.".format(name, rowPosition))
    
    def styleAdd(self, table, color, ringsize, ringcolor="Green"):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        name_set = QTableWidgetItem("Point{}".format(rowPosition))
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        color_combobox = QComboBox(table)
        re_Color = colorName()
        for i in range(len(re_Color)): color_combobox.insertItem(i, re_Color[i])
        color_combobox.setCurrentIndex(color_combobox.findText(color))
        table.setCellWidget(rowPosition, 1, color_combobox)
        table.setItem(rowPosition, 1, QTableWidgetItem("Green"))
        ring_size = QTableWidgetItem(ringsize)
        ring_size.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, ring_size)
        color_combobox.setCurrentIndex(color_combobox.findText(ringcolor))
        table.setCellWidget(rowPosition, 3, color_combobox)
        print("Add Point Style for Point{}.".format(rowPosition))
    
    def update(self, table, name):
        lst = list()
        for i in range(table.rowCount()):
            if name=='Point':
                k = {'x':0, 'y':0, 'fix':False, 'cx':0, 'cy':0}
                k['x'] = float(table.item(i, 1).text())
                k['y'] = float(table.item(i, 2).text())
                k['fix'] = bool(table.item(i, 3).checkState())
                try:
                    k['cx'] = float(table.item(i, 4).text().replace('(', '').replace(')', '').split(', ')[0])
                    k['cy'] = float(table.item(i, 4).text().replace('(', '').replace(')', '').split(', ')[1])
                except: pass
            elif name=='Line':
                k = {'start':0, 'end':0, 'len':0}
                k['start'] = int(table.item(i, 1).text().replace('Point', ''))
                k['end'] = int(table.item(i, 2).text().replace('Point', ''))
                k['len'] = float(table.item(i, 3).text())
            elif name=='Chain':
                k = {'p1':0, 'p2':0, 'p3':0, 'p1p2':0, 'p2p3':0, 'p1p3':0}
                k['p1'] = int(table.item(i, 1).text().replace('Point', ''))
                k['p2'] = int(table.item(i, 2).text().replace('Point', ''))
                k['p3'] = int(table.item(i, 3).text().replace('Point', ''))
                k['p1p2'] = float(table.item(i, 4).text())
                k['p2p3'] = float(table.item(i, 5).text())
                k['p1p3'] = float(table.item(i, 6).text())
            elif name=='Shaft':
                k = {'cen':0, 'ref':0, 'start':0, 'end':0, 'demo':0}
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['ref'] = int(table.item(i, 2).text().replace('Point', ''))
                k['start'] = float(table.item(i, 3).text())
                k['end'] = float(table.item(i, 4).text())
                k['demo'] = float(table.item(i, 5).text())
                k['isParallelogram'] = bool(table.item(i, 6).checkState())
            elif name=='Slider':
                k = {'cen':0, 'start':0, 'end':0}
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['start'] = int(table.item(i, 2).text().replace('Point', ''))
                k['end'] = int(table.item(i, 3).text().replace('Point', ''))
            elif name=='Rod':
                k = {'cen':0, 'start':0, 'end':0, 'pos':0}
                k['cen'] = int(table.item(i, 1).text().replace('Point', ''))
                k['start'] = int(table.item(i, 2).text().replace('Point', ''))
                k['end'] = int(table.item(i, 3).text().replace('Point', ''))
                k['pos'] = float(table.item(i, 4).text())
            elif name=='Parameter':
                try:
                    k = {int(table.item(i, 0).text().replace('n', '')):float(table.item(i, 1).text())}
                except: pass
            lst += [k]
        if name=='Point': self.PointList = lst
        elif name=='Line': self.LineList = lst
        elif name=='Chain': self.ChainList = lst
        elif name=='Shaft': self.ShaftList = lst
        elif name=='Slider': self.SliderList = lst
        elif name=='Rod': self.RodList = lst
        elif name=='Parameter': self.ParameterList = lst
    
    def updateStyle(self, table):
        lst = list()
        for i in range(table.rowCount()):
            k = {'cen':'Green', 'ring':5, 'color':'Green'}
            k['cen'] = table.item(i, 1).text()
            k['ring'] = int(table.item(i, 2).text())
            k['color'] = table.cellWidget(i, 3).currentText()
            lst += [k]
        self.style = l
    
    def deletePointTable(self, tablePoint, tableStyle, tableLine, tableChain, tableShaft, tableSlider, tableRod, pos):
        for i in range(tableLine.rowCount()):
            if (pos == tableLine.item(i, 1).text()) or (pos == tableLine.item(i, 2).text()):
                tableLine.removeRow(i)
                for j in range(i, tableLine.rowCount()): tableLine.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
                break
        for i in range(tableChain.rowCount()):
            if (pos == tableChain.item(i, 1).text()) or (pos == tableChain.item(i, 2).text()):
                tableChain.removeRow(i)
                for j in range(i, tableChain.rowCount): tableChain.setItem(j, 0, QTableWidgetItem("Chain"+str(j)))
                break
        for i in range(tableShaft.rowCount()):
            if (pos == tableShaft.item(i, 1).text()) or (pos == tableShaft.item(i, 2).text()):
                tableShaft.removeRow(i)
                for j in range(i, tableShaft.rowCount()): tableShaft.setItem(j, 0, QTableWidgetItem("Shaft"+str(j)))
                break
        for i in range(tableSlider.rowCount()):
            if (pos == tableSlider.item(i, 1).text()):
                tableSlider.removeRow(i)
                for j in range(i, tableSlider.rowCount()): tableSlider.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
                break
        for i in range(tableRod.rowCount()):
            if (pos == tableRod.item(i, 1).text()) or (pos == tableRod.item(i, 2).text()):
                tableRod.removeRow(i)
                for j in range(i, tableRod.rowCount()): tableRod.setItem(j, 0, QTableWidgetItem("Rod"+str(j)))
                break
        for i in range(1, tablePoint.rowCount()):
            if (pos == tablePoint.item(i, 0).text()):
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
    
    def setup(self, table, data, Run_list):
        for i in range(len(data)):
            nPath = data[i]
            for j in range(0, len(nPath), 2):
                X_path = nPath[j]
                Y_path = nPath[j+1]
                for k in range(len(X_path)-1):
                    table.insertRow(table.rowCount())
                    table.setItem(table.rowCount()-1, 0, QTableWidgetItem(Run_list[int(j/2)]))
                    table.setItem(table.rowCount()-1, 1, QTableWidgetItem(str(X_path[k])))
                    table.setItem(table.rowCount()-1, 2, QTableWidgetItem(str(Y_path[k])))
    
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
