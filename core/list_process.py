from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .warning.contradict_value import contradict_show

def Points_list(table, name, x, y, fixed, edit):
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

def Points_style_fix(table, name, fix):
    rowPosition = int(name.replace("Point", ""))
    if fix: fix_set = QTableWidgetItem("10")
    else: fix_set = QTableWidgetItem("5")
    fix_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 2, fix_set)

def Links_list(table, name, start, end, l, edit):
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

def Chain_list(table, name, p1, p2, p3, a, b, c, edit):
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

def Shaft_list(table, name, center, references, start, end, demo_angle, edit):
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

def Slider_list(table, name, center, references, edit):
    rowPosition = int(name.replace("Slider", ""))
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    if not edit: table.insertRow(rowPosition)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(center))
    table.setItem(rowPosition, 2, QTableWidgetItem(references))
    if not edit: print("Set the Point to new Slider.")
    else: print("Set the Point to selected Slider.")

def Rod_list(table, name, start, end, min, max, edit):
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

def Points_style_add(table, name, color, ringsize, ringcolor):
    rowPosition = table.rowCount()
    table.insertRow(rowPosition)
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(color))
    ring_size = QTableWidgetItem(ringsize)
    ring_size.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 2, ring_size)
    table.setItem(rowPosition, 3, QTableWidgetItem(ringcolor))
    print("Add Point Style for Point"+str(rowPosition)+".")

def Point_list_delete(table1, table2, table3, table4, table5, table6, table7, dlg):
    for i in range(table3.rowCount()):
        if (dlg.Point.currentText() == table3.item(i, 1).text()) or (dlg.Point.currentText() == table3.item(i, 2).text()):
            table3.removeRow(i)
            for j in range(i, table3.rowCount()): table3.setItem(j, 0, QTableWidgetItem("Line"+str(j)))
            break
    for i in range(table4.rowCount()):
        if (dlg.Point.currentText() == table4.item(i, 1).text()) or (dlg.Point.currentText() == table4.item(i, 2).text()):
            table4.removeRow(i)
            for j in range(i, table4.rowCount): table4.setItem(j, 0, QTableWidgetItem("Chain"+str(j)))
            break
    for i in range(table5.rowCount()):
        if (dlg.Point.currentText() == table5.item(i, 1).text()) or (dlg.Point.currentText() == table5.item(i, 2).text()):
            table5.removeRow(i)
            for j in range(i, table5.rowCount()): table5.setItem(j, 0, QTableWidgetItem("Shaft"+str(j)))
            break
    for i in range(table6.rowCount()):
        if (dlg.Point.currentText() == table6.item(i, 1).text()):
            table6.removeRow(i)
            for j in range(i, table6.rowCount()): table6.setItem(j, 0, QTableWidgetItem("Slider"+str(j)))
            break
    for i in range(table7.rowCount()):
        if (dlg.Point.currentText() == table7.item(i, 1).text()) or (dlg.Point.currentText() == table7.item(i, 2).text()):
            table7.removeRow(i)
            for j in range(i, table7.rowCount()): table7.setItem(j, 0, QTableWidgetItem("Rod"+str(j)))
            break
    for i in range(1, table1.rowCount()):
        if (dlg.Point.currentText() == table1.item(i, 0).text()):
            table1.removeRow(i)
            table2.removeRow(i)
            for j in range(i, table1.rowCount()): table1.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
            for j in range(i, table1.rowCount()): table2.setItem(j, 0, QTableWidgetItem("Point"+str(j)))
            break

def Link_list_delete(table1, table2, dlg):
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

def One_list_delete(table, name, dlg):
    for i in range(table.rowCount()):
        if (dlg.Entity.currentText() == table.item(i, 0).text()):
            table.removeRow(i)
            for j in range(i, table.rowCount()): table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            break

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
        if dlg.exec_(): One_list_delete(table, name, dlg)

def Repeated_check_line(table, first, second):
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

def Reset_notebook(table, k):
    for i in reversed(range(k, table.rowCount())): table.removeRow(i)

def Point_setup(table, num, x, y):
    table.setItem(num, 4, QTableWidgetItem("("+str(x)+", "+str(y)+")"))

def Path_point_setup(table, data, Run_list):
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

def Parameter_management(table, name, val, commit):
    rowPosition = int(name.replace("n", ""))
    name_set = QTableWidgetItem(name)
    name_set.setFlags(Qt.ItemIsEnabled)
    table.insertRow(rowPosition)
    table.setItem(rowPosition, 0, name_set)
    table.setItem(rowPosition, 1, QTableWidgetItem(val))
    table.setItem(rowPosition, 2, QTableWidgetItem(commit))
