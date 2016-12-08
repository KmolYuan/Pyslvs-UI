# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ..warning.contradict_value import contradict_show
from ..calculation.canvas import DynamicCanvas

class Points():
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
    
    def coverageCoordinate(self, table, row):
        coordinate = table.item(row, 4).text()[1:-1].split(', ')
        x = QTableWidgetItem(coordinate[0])
        y = QTableWidgetItem(coordinate[1])
        table.setItem(row, 1, x)
        table.setItem(row, 2, y)

    def styleFix(self, table, name, fix):
        rowPosition = int(name.replace("Point", ""))
        if fix: fix_set = QTableWidgetItem("10")
        else: fix_set = QTableWidgetItem("5")
        fix_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 2, fix_set)
    
    def currentPos(self, table, num, x, y):
        digit = QTableWidgetItem("("+str(x)+", "+str(y)+")")
        digit.setToolTip("("+str(x)+", "+str(y)+")")
        table.setItem(num, 4, digit)

class Lines():
    def editTable(self, table, name, start, end, l, edit):
        rowPosition = int(name.replace("Line", ""))
        if not edit: table.insertRow(rowPosition)
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(start))
        table.setItem(rowPosition, 2, QTableWidgetItem(end))
        table.setItem(rowPosition, 3, QTableWidgetItem(l))
        if not edit: print("Add a link, Line "+str(rowPosition)+".")
        else: print("Edit a link, Line "+str(rowPosition)+".")
    
    def deleteTable(self, table1, table2, dlg):
        for i in range(table2.rowCount()):
            if (dlg.Entity.currentText() == table2.item(i, 2).text()):
                table2.removeRow(i)
                for j in range(i, table3.rowCount()): table3.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
                break
        for i in range(table1.rowCount()):
            if (dlg.Entity.currentText() == table1.item(i, 0).text()):
                table1.removeRow(i)
                for j in range(i, table1.rowCount()): table1.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
                break
    
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

class Chains():
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
        if not edit: print("Add a Triangle Chain, Line "+str(rowPosition)+".")
        else: print("Edit a Triangle Chain, Line "+str(rowPosition)+".")

class Shafts():
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
        if not edit: print("Set the Point to new Shaft.")
        else: print("Set the Point to selected Shaft.")

class Sliders():
    def editTable(self, table, name, center, references, edit):
        rowPosition = int(name.replace("Slider", ""))
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        if not edit: table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(center))
        table.setItem(rowPosition, 2, QTableWidgetItem(references))
        if not edit: print("Set the Point to new Slider.")
        else: print("Set the Point to selected Slider.")

class Rods():
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

class Parameters():
    def editTable(self, table, name, val, commit):
        rowPosition = int(name.replace("n", ""))
        name_set = QTableWidgetItem(name)
        name_set.setFlags(Qt.ItemIsEnabled)
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, name_set)
        table.setItem(rowPosition, 1, QTableWidgetItem(val))
        table.setItem(rowPosition, 2, QTableWidgetItem(commit.replace(",")))

class Path():
    def __init__(self):
        self.data = []
        self.runList = []

def Delete_dlg_set(table, icon, dlg, name, pos):
    if table.rowCount() <= 0:
        dlg = zero_show()
        dlg.show()
        if dlg.exec_(): pass
    else:
        for i in range(table.rowCount()):
            dlg.Entity.insertItem(i, icon, table.item(i, 0).text())
        dlg.Entity.setCurrentIndex(pos)
        dlg.show()
        if dlg.exec_():
            for i in range(table.rowCount()):
                if (dlg.Entity.currentText() == table.item(i, 0).text()):
                    table.removeRow(i)
                    for j in range(i, table.rowCount()): table.setItem(j, 0, QTableWidgetItem(name+str(j)))
                    break
