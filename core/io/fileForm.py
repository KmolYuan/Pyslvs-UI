# -*- coding: utf-8 -*-
from .list_process import(Parameters, Path,
    Points, Lines, Chains, Shafts, Sliders, Rods)
#File Info
from ..info.fileInfo import fileInfo_show
from ..info.editFileInfo import editFileInfo_show
#Date
import datetime
now = datetime.datetime.now()

class File():
    def __init__(self):
        self.form = {
            'fileName':"[New Workbook]",
            'description':'',
            'author':'',
            'lastTime':'',
            'changed':False,
            }
        self.Points = Points()
        self.Lines = Lines()
        self.Chains = Chains()
        self.Shafts = Shafts()
        self.Sliders = Sliders()
        self.Rods = Rods()
        self.Parameters = Parameters()
        self.Path = Path()
    
    def setProperty(self):
        dlg = editFileInfo_show()
        self.form['lastTime'] = "%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)
        dlg.rename(self.form['fileName'], self.form['author'], self.form['description'], self.form['lastTime'])
        dlg.show()
        if dlg.exec_():
            self.form['author'] = dlg.authorName_input.text()
            self.form['description'] = dlg.descriptionText.toPlainText()
            print(self.form)
    
    #Check, Read, Wirte, Reset
    def check(self, data):
        n1 = len([e for e, x in enumerate(data) if x=='_info_'])==4
        n2 = len([e for e, x in enumerate(data) if x=='_table_'])==9
        n3 = len([e for e, x in enumerate(data) if x=='_path_'])==2
        return n1 and n2 and n3
    def read(self, fileName, data, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        #info
        infoIndex = [e for e, x in enumerate(data) if '_info_' in x]
        try: author = data[infoIndex[0]:infoIndex[1]+1][1]
        except: author = ''
        try: description = data[infoIndex[1]:infoIndex[2]+1][1]
        except: description = ''
        try: lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except: lastTime = ''
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[0]:tableIndex[1]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4):
                    fixed = li[i+3]=='Fixed'
                    self.Points.editTable(Point, li[i], li[i+1], li[i+2], fixed, False)
        except: pass
        try:
            li = data[tableIndex[1]:tableIndex[2]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Points.styleAdd(Point_Style, li[i], li[i+1], li[i+2], li[i+3])
        except: pass
        try:
            li = data[tableIndex[2]:tableIndex[3]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lines.editTable(Link, li[i], li[i+1], li[i+2], li[i+3], False)
        except: pass
        try:
            li = data[tableIndex[3]:tableIndex[4]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Chains.editTable(Chain, li[i], li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6], False)
        except: pass
        try:
            li = data[tableIndex[4]:tableIndex[5]]
            if (len(li)-1)%6==0:
                for i in range(1, len(li), 6): self.Shafts.editTable(Shaft, li[i], li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], False)
        except: pass
        try:
            li = data[tableIndex[5]:tableIndex[6]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Sliders.editTable(Slider, li[i], li[i+1], li[i+2], False)
        except: pass
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%5==0:
                for i in range(1, len(li), 5): self.Rods.editTable(Rod, li[i], li[i+1], li[i+2], li[i+3], li[i+4], False)
        except: pass
        try:
            li = data[tableIndex[7]:tableIndex[8]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Parameters.editTable(Parameter, li[i], li[i+1], li[i+2])
        except: pass
        #path
        pathIndex = [e for e, x in enumerate(data) if '_path_' in x]
        li = data[pathIndex[0]+1:pathIndex[1]]
        self.Path.runList = li
        li = data[pathIndex[1]+1::]
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
        dlg = fileInfo_show()
        dlg.rename(fileName, author, description, lastTime)
        dlg.show()
        if dlg.exec_(): pass
    def write(self, fileName, writer, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        self.form['fileName'] = fileName.split('/')[-1]
        writer.writerow(["_info_"])
        writer.writerow([self.form['author']])
        writer.writerow(["_info_"])
        writer.writerow([self.form['description']])
        writer.writerow(["_info_"])
        writer.writerow(["%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)])
        writer.writerow(["_info_"])
        writer.writerow(["_table_"])
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
        self.CSV_notebook(writer, Point_Style, 4, 1)
        self.CSV_notebook(writer, Link, 4)
        self.CSV_notebook(writer, Chain, 7)
        self.CSV_notebook(writer, Shaft, 6)
        self.CSV_notebook(writer, Slider, 3)
        self.CSV_notebook(writer, Rod, 5)
        self.CSV_notebook(writer, Parameter, 3)
        writer.writerow(["_table_"])
        writer.writerow(["_path_"])
        if self.Path.runList:
            rowdata = []
            for i in range(len(self.Path.runList)):
                if i == len(self.Path.runList)-1: rowdata += [str(self.Path.runList[i])]
                else: rowdata += [str(self.Path.runList[i])+'\t']
            writer.writerow(rowdata)
        writer.writerow(["_path_"])
        if self.Path.data:
            for i in range(len(self.Path.data[0])):
                rowdata = []
                for j in range(len(self.Path.data[0][i])): rowdata += [str(self.Path.data[0][i][j])+'\t']
                rowdata += ["+="]
                writer.writerow(rowdata)
    def reset(self, Point, Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        for i in reversed(range(1, Point.rowCount())): Point.removeRow(i)
        for i in reversed(range(1, Style.rowCount())): Style.removeRow(i)
        for i in reversed(range(0, Link.rowCount())): Link.removeRow(i)
        for i in reversed(range(0, Chain.rowCount())): Chain.removeRow(i)
        for i in reversed(range(0, Shaft.rowCount())): Shaft.removeRow(i)
        for i in reversed(range(0, Slider.rowCount())): Slider.removeRow(i)
        for i in reversed(range(0, Rod.rowCount())): Rod.removeRow(i)
        for i in reversed(range(0, Parameter.rowCount())): Parameter.removeRow(i)
    
    def CSV_notebook(self, writer, table, k, init=0):
        writer.writerow(["_table_"])
        for row in range(init, table.rowCount()):
            rowdata = []
            for column in range(table.columnCount()):
                if table.item(row, column) is not None:
                    if column==k-1: rowdata += [table.item(row, column).text()]
                    else: rowdata += [table.item(row, column).text()+'\t']
                elif table.cellWidget(row, column): rowdata += [table.cellWidget(row, column).currentText()]
            writer.writerow(rowdata)
