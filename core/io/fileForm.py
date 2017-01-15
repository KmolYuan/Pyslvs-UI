# -*- coding: utf-8 -*-
from .modules import *
from .listProcess import *
from .slvsType import SLVS_Code
now = datetime.datetime.now()

class File():
    def __init__(self):
        self.form = {
            'fileName':"[New Workbook]",
            'description':'',
            'author':'',
            'lastTime':'%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute),
            'changed':False,
            }
        self.resetAllList()
    
    def resetAllList(self):
        self.Points = Points()
        self.Lines = Lines()
        self.Chains = Chains()
        self.Shafts = Shafts()
        self.Sliders = Sliders()
        self.Rods = Rods()
        self.Parameters = Parameters()
        self.Path = Path()
        self.PathSolvingReqs = PathSolvingReqs()
    
    def updateTime(self):
        self.form['lastTime'] = "%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)
    
    #Check, Read, Write, Reset
    def check(self, data):
        n1 = len([e for e, x in enumerate(data) if x=='_info_'])==4
        n2 = len([e for e, x in enumerate(data) if x=='_table_'])==9
        n3 = len([e for e, x in enumerate(data) if x=='_path_'])==3
        return n1 and n2 and n3
    def read(self, fileName, data, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        if '--file-data' in argv: print(data)
        #info
        infoIndex = [e for e, x in enumerate(data) if '_info_' in x]
        try: author = data[infoIndex[0]:infoIndex[1]+1][1]
        except: author = ''
        try: description = data[infoIndex[1]:infoIndex[2]+1][1]
        except: description = ''
        try: lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except: lastTime = '%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute)
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[0]:tableIndex[1]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4):
                    fixed = li[i+3]=='Fixed'
                    self.Points.editTable(Point, li[i+1], li[i+2], fixed)
        except: pass
        try:
            li = data[tableIndex[1]:tableIndex[2]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Points.styleAdd(Point_Style, li[i+1], li[i+2], li[i+3].replace(",", ""))
        except: pass
        try:
            li = data[tableIndex[2]:tableIndex[3]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lines.editTable(Link, li[i+1], li[i+2], li[i+3])
        except: pass
        try:
            li = data[tableIndex[3]:tableIndex[4]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Chains.editTable(Chain, li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6])
        except: pass
        try:
            li = data[tableIndex[4]:tableIndex[5]]
            if (len(li)-1)%6==0:
                for i in range(1, len(li), 6): self.Shafts.editTable(Shaft, li[i+1], li[i+2], li[i+3], li[i+4], li[i+5])
        except: pass
        try:
            li = data[tableIndex[5]:tableIndex[6]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Sliders.editTable(Slider, li[i+1], li[i+2])
        except: pass
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%5==0:
                for i in range(1, len(li), 5): self.Rods.editTable(Rod, li[i+1], li[i+2], li[i+3], li[i+4])
        except: pass
        try:
            li = data[tableIndex[7]:tableIndex[8]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Parameters.editTable(Parameter, li[i+1], li[i+2])
        except: pass
        #path
        pathIndex = [e for e, x in enumerate(data) if '_path_' in x]
        li = data[pathIndex[0]+1:pathIndex[1]]
        self.Path.runList = li
        li = data[pathIndex[1]+1:pathIndex[2]]
        self.Path.shaftList = [int(e) for e in li]
        li = data[pathIndex[2]+1::]
        path = []
        path_e = []
        for i in range(0, len(li)):
            if '+' in li[i]:
                path += [path_e]
                path_e = []
            else: path_e += [float(li[i])]
        self.Path.data = [path]
        self.form['fileName'] = fileName.split('/')[-1]
        self.form['author'] = author
        self.form['description'] = description
        self.form['lastTime'] = lastTime
    
    def write(self, fileName, writer, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        self.form['fileName'] = fileName.split('/')[-1]
        writer.writerows([
            ["_info_"], [self.form['author']],
            ["_info_"], [self.form['description']],
            ["_info_"], ["%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)],
            ["_info_"], ["_table_"]])
        for row in range(1, Point.rowCount()):
            rowdata = []
            for column in range(Point.columnCount()-1):
                item = Point.item(row, column)
                if item is not None:
                    if (item.checkState()==False) and (item.text()==''): rowdata += ["noFixedFixed"]
                    else:
                        if item.text()=='': rowdata += ["Fixed"]
                        else: rowdata += [item.text()+'\t']
            writer.writerow(rowdata)
        self.CSV_write(writer, Point_Style, 4, 1)
        self.CSV_write(writer, Link, 4)
        self.CSV_write(writer, Chain, 7)
        self.CSV_write(writer, Shaft, 6)
        self.CSV_write(writer, Slider, 3)
        self.CSV_write(writer, Rod, 5)
        self.CSV_write(writer, Parameter, 3)
        writer.writerow(["_table_"])
        writer.writerow(["_path_"])
        if self.Path.runList:
            rowdata = []
            for i in range(len(self.Path.runList)):
                if i == len(self.Path.runList)-1: rowdata += [str(self.Path.runList[i])]
                else: rowdata += [str(self.Path.runList[i])+'\t']
            writer.writerow(rowdata)
        writer.writerow(["_path_"])
        if self.Path.shaftList:
            writer.writerow(self.Path.shaftList)
        writer.writerow(["_path_"])
        if self.Path.data:
            for i in range(len(self.Path.data[0])):
                rowdata = []
                for j in range(len(self.Path.data[0][i])): rowdata += [str(self.Path.data[0][i][j])+'\t']
                rowdata += ["+="]
                writer.writerow(rowdata)
    def reset(self, Point, Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        for i in reversed(range(0, Rod.rowCount())): Rod.removeRow(i)
        for i in reversed(range(0, Slider.rowCount())): Slider.removeRow(i)
        for i in reversed(range(0, Shaft.rowCount())): Shaft.removeRow(i)
        for i in reversed(range(0, Chain.rowCount())): Chain.removeRow(i)
        for i in reversed(range(0, Link.rowCount())): Link.removeRow(i)
        for i in reversed(range(1, Point.rowCount())): Point.removeRow(i)
        for i in reversed(range(1, Style.rowCount())): Style.removeRow(i)
        for i in reversed(range(0, Parameter.rowCount())): Parameter.removeRow(i)
        self.resetAllList()
    
    def writeSlvsFile(self, fileName):
        code = SLVS_Code(self.Points.list, self.Lines.list, self.Chains.list, self.Sliders.list, self.Rods.list)
        with open(fileName, 'w', encoding="iso-8859-15", newline="") as f:
                f.write(code)
    
    def CSV_write(self, writer, table, k, init=0):
        writer.writerow(["_table_"])
        for row in range(init, table.rowCount()):
            rowdata = []
            for column in range(table.columnCount()):
                if table.item(row, column) is not None:
                    if column==k-1: rowdata += [table.item(row, column).text()]
                    else: rowdata += [table.item(row, column).text()+'\t']
                elif table.cellWidget(row, column): rowdata += [table.cellWidget(row, column).currentText()]
            writer.writerow(rowdata)
    
    def Obstacles_Exclusion(self):
        table_point = self.Points.list
        table_line = self.Lines.list
        table_chain = self.Chains.list
        table_shaft = self.Shafts.list
        table_slider = self.Sliders.list
        table_rod = self.Rods.list
        for i in range(len(table_line)):
            a = table_line[i]['start']
            b = table_line[i]['end']
            case1 = table_point[a]['x']==table_point[b]['x']
            case2 = table_point[a]['y']==table_point[b]['y']
            if case1 and case2:
                if b == 0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
        for i in range(len(table_chain)):
            a = table_chain[i]['p1']
            b = table_chain[i]['p2']
            c = table_chain[i]['p3']
            if table_point[a]['x']==table_point[b]['x'] and table_point[a]['y']==table_point[b]['y']:
                if b==0: table_point[a]['x'] += 0.01
                else: table_point[b]['x'] += 0.01
            if table_point[b]['x']==table_point[c]['x'] and table_point[b]['y']==table_point[c]['y']:
                if c==0: table_point[b]['y'] += 0.01
                else: table_point[c]['y'] += 0.01
            if table_point[a]['x']==table_point[c]['x'] and table_point[a]['y']==table_point[c]['y']:
                if c==0: table_point[a]['y'] += 0.01
                else: table_point[c]['y'] += 0.01
        return table_point, table_line, table_chain, table_shaft, table_slider, table_rod
    
    def Generate_Merge(self, row, data, Point, Point_Style, Link, Chain, Shaft):
        for i in range(len(data)):
            self.Points.editTable(Point, data[i]['x'], data[i]['y'], i<2)
            self.Points.styleAdd(Point_Style, 'Green', '10' if i<2 else '5', 'Blue' if i<2 else 'Green')
        self.Chains.editTable(Chain, li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6])
