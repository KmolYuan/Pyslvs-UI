# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ..warning.contradict_value import contradict_show
from ..calculation.canvasView import DynamicCanvas

class Points():
    def __init__(self):
        self.list = [{'x':0, 'y':0, 'fix':True, 'cx':0, 'cy':0}]
        self.style = [{'cen':'Red', 'ring':10, 'color':'Red'}]
    
    def editTable(self, table, name, x, y, fixed, edit):
        rowPosition = int(name.replace("Point", ""))
        if not edit: table.insertRow(rowPosition)
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(x))
        table.setItem(rowPosition, 2, QTableWidgetItem(y))
        checkbox = QTableWidgetItem("")
        checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        if fixed: checkbox.setCheckState(Qt.Checked)
        else: checkbox.setCheckState(Qt.Unchecked)
        table.setItem(rowPosition, 3, checkbox)
        self.update(table)
        if not edit: print("Add Point"+str(rowPosition)+".")
        else: print("Edit Point"+str(rowPosition)+".")

    def styleAdd(self, table, name, color, ringsize, ringcolor):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        color_combobox = QComboBox(table)
        DC = DynamicCanvas()
        for i in range(len(DC.re_Color)): color_combobox.insertItem(i, DC.re_Color[i])
        color_combobox.setCurrentIndex(color_combobox.findText(color))
        table.setCellWidget(rowPosition, 1, color_combobox)
        table.setItem(rowPosition, 1, QTableWidgetItem("Green"))
        ring_size = QTableWidgetItem(ringsize)
        ring_size.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, ring_size)
        color_combobox.setCurrentIndex(color_combobox.findText(ringcolor))
        table.setCellWidget(rowPosition, 3, color_combobox)
        print("Add Point Style for Point"+str(rowPosition)+".")

    def deleteTable(self, tablePoint, tableStyle, tableLine, tableChain, tableShaft, tableSlider, tableRod, dlg):
        for i in range(tableLine.rowCount()):
            if (dlg.Point.currentText() == tableLine.item(i, 1).text()) or (dlg.Point.currentText() == tableLine.item(i, 2).text()):
                tableLine.removeRow(i)
                for j in range(i, tableLine.rowCount()): tableLine.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
                break
        for i in range(tableChain.rowCount()):
            if (dlg.Point.currentText() == tableChain.item(i, 1).text()) or (dlg.Point.currentText() == tableChain.item(i, 2).text()):
                tableChain.removeRow(i)
                for j in range(i, tableChain.rowCount): tableChain.setItem(j, 0, QTableWidgetItem("Chain"+str(j)))
                break
        for i in range(tableShaft.rowCount()):
            if (dlg.Point.currentText() == tableShaft.item(i, 1).text()) or (dlg.Point.currentText() == tableShaft.item(i, 2).text()):
                tableShaft.removeRow(i)
                for j in range(i, tableShaft.rowCount()): tableShaft.setItem(j, 0, QTableWidgetItem("Shaft"+str(j)))
                break
        for i in range(tableSlider.rowCount()):
            if (dlg.Point.currentText() == tableSlider.item(i, 1).text()):
                tableSlider.removeRow(i)
                for j in range(i, tableSlider.rowCount()): tableSlider.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
                break
        for i in range(tableRod.rowCount()):
            if (dlg.Point.currentText() == tableRod.item(i, 1).text()) or (dlg.Point.currentText() == tableRod.item(i, 2).text()):
                tableRod.removeRow(i)
                for j in range(i, tableRod.rowCount()): tableRod.setItem(j, 0, QTableWidgetItem("Rod"+str(j)))
                break
        for i in range(1, tablePoint.rowCount()):
            if (dlg.Entity.currentText() == tablePoint.item(i, 0).text()):
                tablePoint.removeRow(i)
                tableStyle.removeRow(i)
                for j in range(i, tablePoint.rowCount()): tablePoint.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
                for j in range(i, tablePoint.rowCount()): tableStyle.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
                break
        self.update(tablePoint)
    
    def coverageCoordinate(self, table, row):
        coordinate = table.item(row, 4).text()[1:-1].split(', ')
        x = QTableWidgetItem(coordinate[0])
        y = QTableWidgetItem(coordinate[1])
        table.setItem(row, 1, x)
        table.setItem(row, 2, y)
        self.update(table)

    def styleFix(self, table, name, fix):
        rowPosition = int(name.replace("Point", ""))
        if fix: fix_set = QTableWidgetItem("10")
        else: fix_set = QTableWidgetItem("5")
        fix_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, fix_set)
    
    def currentPos(self, table, result):
        for i in range(table.rowCount()):
            digit = QTableWidgetItem("("+str(result[i]['x'])+", "+str(result[i]['y'])+")")
            digit.setToolTip("("+str(result[i]['x'])+", "+str(result[i]['y'])+")")
            table.setItem(i, 4, digit)
        self.update(table)
    
    def update(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'x':0, 'y':0, 'fix':False, 'cx':0, 'cy':0}
            k['x'] = float(table.item(i, 1).text())
            k['y'] = float(table.item(i, 2).text())
            k['fix'] = bool(table.item(i, 3).checkState())
            try:
                k['cx'] = float(table.item(i, 4).text().replace("(", "").replace(")", "").split(", ")[0])
                k['cy'] = float(table.item(i, 4).text().replace("(", "").replace(")", "").split(", ")[1])
            except: pass
            list += [k]
        self.list = list
    
    def updateStyle(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'cen':'Green', 'ring':5, 'color':'Green'}
            k['cen'] = table.item(i, 1).text()
            k['ring'] = int(table.item(i, 2).text())
            k['color'] = table.cellWidget(i, 3).currentText()
            list += [k]
        self.style = list

class Lines():
    def __init__(self):
        self.list = []
    
    def editTable(self, table, name, start, end, len, edit):
        rowPosition = int(name.replace("Line", ""))
        if not edit: table.insertRow(rowPosition)
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(start))
        table.setItem(rowPosition, 2, QTableWidgetItem(end))
        table.setItem(rowPosition, 3, QTableWidgetItem(len))
        self.update(table)
        if not edit: print("Add a link, Line "+str(rowPosition)+".")
        else: print("Edit a link, Line "+str(rowPosition)+".")
    
    def deleteTable(self, tableLine, tableSlider, dlg):
        for i in range(tableSlider.rowCount()):
            if (dlg.Entity.currentText() == tableSlider.item(i, 2).text()):
                tableSlider.removeRow(i)
                for j in range(i, table3.rowCount()): tableSlider.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
                break
        for i in range(tableLine.rowCount()):
            if (dlg.Entity.currentText() == tableLine.item(i, 0).text()):
                tableLine.removeRow(i)
                for j in range(i, table1.rowCount()): tableLine.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
                break
        self.update(tableLine)
    
    def repeatedCheck(self, table, first, second):
        n = False
        for i in range(table.rowCount()):
            case1 = (table.item(i, 1).text()==first)and(table.item(i, 2).text()==second)
            case2 = (table.item(i, 2).text()==first)and(table.item(i, 1).text()==second)
            if case1 or case2:
                n = True
                dlg = contradict_show()
                dlg.show()
                if dlg.exec_(): break
        return n
    
    def update(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'start':0, 'end':0, 'len':0}
            k['start'] = int(table.item(i, 1).text().replace("Point", ""))
            k['end'] = int(table.item(i, 2).text().replace("Point", ""))
            k['len'] = float(table.item(i, 3).text())
            list += [k]
        self.list = list

class Chains():
    def __init__(self):
        self.list = []
    
    def editTable(self, table, name, p1, p2, p3, a, b, c, edit):
        rowPosition = int(name.replace("Chain", ""))
        if not edit: table.insertRow(rowPosition)
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(p1))
        table.setItem(rowPosition, 2, QTableWidgetItem(p2))
        table.setItem(rowPosition, 3, QTableWidgetItem(p3))
        table.setItem(rowPosition, 4, QTableWidgetItem(a))
        table.setItem(rowPosition, 5, QTableWidgetItem(b))
        table.setItem(rowPosition, 6, QTableWidgetItem(c))
        self.update(table)
        if not edit: print("Add a Triangle Chain, Line "+str(rowPosition)+".")
        else: print("Edit a Triangle Chain, Line "+str(rowPosition)+".")
    
    def update(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'p1':0, 'p2':0, 'p3':0, 'p1p2':0, 'p2p3':0, 'p1p3':0}
            k['p1'] = int(table.item(i, 1).text().replace("Point", ""))
            k['p2'] = int(table.item(i, 2).text().replace("Point", ""))
            k['p3'] = int(table.item(i, 3).text().replace("Point", ""))
            k['p1p2'] = float(table.item(i, 4).text())
            k['p2p3'] = float(table.item(i, 5).text())
            k['p1p3'] = float(table.item(i, 6).text())
            list += [k]
        self.list = list

class Shafts():
    def __init__(self):
        self.list = []
    
    def editTable(self, table, name, center, references, start, end, demo_angle, edit):
        rowPosition = int(name.replace("Shaft", ""))
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        if not edit: table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(center))
        table.setItem(rowPosition, 2, QTableWidgetItem(references))
        table.setItem(rowPosition, 3, QTableWidgetItem(start))
        table.setItem(rowPosition, 4, QTableWidgetItem(end))
        if demo_angle: table.setItem(rowPosition, 5, QTableWidgetItem(demo_angle))
        self.update(table)
        if not edit: print("Set the Point to new Shaft.")
        else: print("Set the Point to selected Shaft.")
    
    def setDemo(self, table, index, angle):
        table.setItem(index, 5, QTableWidgetItem(str(angle)))
        self.update(table)
    
    def update(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'cen':0, 'ref':0, 'start':0, 'end':0, 'demo':0}
            k['cen'] = int(table.item(i, 1).text().replace("Point", ""))
            k['ref'] = int(table.item(i, 2).text().replace("Point", ""))
            k['start'] = float(table.item(i, 3).text())
            k['end'] = float(table.item(i, 4).text())
            try: k['demo'] = float(table.item(i, 5).text())
            except: pass
            list += [k]
        self.list = list

class Sliders():
    def __init__(self):
        self.list = []
    
    def editTable(self, table, name, center, references, edit):
        rowPosition = int(name.replace("Slider", ""))
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        if not edit: table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(center))
        table.setItem(rowPosition, 2, QTableWidgetItem(references))
        self.update(table)
        if not edit: print("Set the Point to new Slider.")
        else: print("Set the Point to selected Slider.")
    
    def update(self, table):
        list = []
        for i in range(table.rowCount()):
            k = {'cen':0, 'ref':0}
            k['cen'] = int(table.item(i, 1).text().replace("Point", ""))
            k['ref'] = int(table.item(i, 2).text().replace("Line", ""))
            list += [k]
        self.list = list

class Rods():
    def __init__(self):
        self.list = []
    
    def editTable(self, table, name, start, end, min, max, edit):
        rowPosition = int(name.replace("Rod", ""))
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        if not edit: table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(start))
        table.setItem(rowPosition, 2, QTableWidgetItem(end))
        table.setItem(rowPosition, 3, QTableWidgetItem(min))
        table.setItem(rowPosition, 4, QTableWidgetItem(max))
        if not edit: print("Set the Point to new Rod.")
        else: print("Set the Point to selected Rod.")
    
    def update(self, table):
        list = []
        for i in range(table_rod.rowCount()):
            k = {'cen':0, 'start':0, 'end':0, 'pos':0}
            k['cen'] = int(table.item(i, 1).text().replace("Point", ""))
            k['start'] = int(table.item(i, 2).text().replace("Line", ""))
            k['end'] = int(table.item(i, 3).text().replace("Line", ""))
            k['pos'] = float(table.item(i, 4).text())
            list += [k]
        self.list = list

class Path():
    def __init__(self):
        self.data = []
        self.runList = []
    
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

class Parameters():
    def __init__(self):
        self.list = []
    
    def editTable(self, table):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        name_set = 0
        existNum = []
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
    
    def deleteTable(self, table):
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
            self.update(table)
        except: pass
    
    def update(self, table):
        try:
            list = []
            for i in range(table.rowCount()):
                k = {int(table.item(i, 0).text().replace('n', '')):float(table.item(i, 1).text())}
                list += [k]
            self.list = list
        except: pass
