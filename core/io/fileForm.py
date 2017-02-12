# -*- coding: utf-8 -*-
from .modules import *
from .listProcess import *
now = datetime.datetime.now()

class File():
    def __init__(self, FileState):
        self.form = {
            'fileName':QFileInfo("[New Workbook]"),
            'description':'',
            'author':'anonymous',
            'lastTime':'%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute),
            'changed':False,
            }
        self.FileState = FileState
        self.resetAllList()
    
    def resetAllList(self):
        self.Lists = Lists(self.FileState)
        self.Path = Path(self.FileState)
        self.PathSolvingReqs = PathSolvingReqs(self.FileState)
    
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
        try: author = data[infoIndex[0]:infoIndex[1]+1][1].replace('"', '')
        except: author = ''
        try: description = data[infoIndex[1]:infoIndex[2]+1][1].replace('"', '')
        except: description = ''
        try: lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except: lastTime = '%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute)
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[0]:tableIndex[1]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lists.editTable(Point, 'Point', False, *[li[i+1], li[i+2], li[i+3]=='True'])
        except: pass
        try:
            li = data[tableIndex[1]:tableIndex[2]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lists.styleAdd(Point_Style, *[li[i+1], li[i+2], li[i+3].replace(",", "")])
        except: pass
        try:
            li = data[tableIndex[2]:tableIndex[3]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lists.editTable(Link, 'Line', False, *[li[i+1], li[i+2], li[i+3]])
        except: pass
        try:
            li = data[tableIndex[3]:tableIndex[4]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Lists.editTable(Chain, 'Chain', False, *[li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6]])
        except: pass
        try:
            li = data[tableIndex[4]:tableIndex[5]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Lists.editTable(Shaft, 'Shaft', False, *[li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6]=='True'])
        except: pass
        try:
            li = data[tableIndex[5]:tableIndex[6]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 3): self.Lists.editTable(Slider, 'Slider', False, *[li[i+1], li[i+2], li[i+3]])
        except: pass
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%5==0:
                for i in range(1, len(li), 5): self.Lists.editTable(Rod, 'Rod', False, *[li[i+1], li[i+2], li[i+3], li[i+4]])
        except: pass
        try:
            li = data[tableIndex[7]:tableIndex[8]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Lists.editTable(Parameter, 'Parameter', False, *[li[i+1], li[i+2]])
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
        self.form['fileName'] = QFileInfo(fileName)
        self.form['author'] = author
        self.form['description'] = description
        self.form['lastTime'] = lastTime
    
    def write(self, fileName, writer, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        self.form['fileName'] = QFileInfo(fileName)
        writer.writerows([
            ["_info_"], [self.form['author']] if self.form['author']!='' else ['anonymous'],
            ["_info_"], [self.form['description']],
            ["_info_"], ["%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)], ["_info_"]])
        self.CSV_write(writer, Point, 4, init=1)
        self.CSV_write(writer, Point_Style, 4, init=1)
        self.CSV_write(writer, Link, 4)
        self.CSV_write(writer, Chain, 7)
        self.CSV_write(writer, Shaft, 7)
        self.CSV_write(writer, Slider, 4)
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
    
    def CSV_write(self, writer, table, k, init=0):
        writer.writerow(["_table_"])
        for row in range(init, table.rowCount()):
            rowdata = []
            for column in range(k):
                item = table.item(row, column)
                cellWidget = table.cellWidget(row, column)
                if not item is None:
                    if item.text()=='': content = "False" if item.checkState()==False else "True"
                    else: content = item.text()
                    rowdata += [content+('' if column==k-1 else '\t')]
                elif cellWidget: rowdata += [cellWidget.currentText()]
            writer.writerow(rowdata)
    
    def Obstacles_Exclusion(self):
        table_point = self.Lists.PointList
        table_line = self.Lists.LineList
        table_chain = self.Lists.ChainList
        table_shaft = self.Lists.ShaftList
        table_slider = self.Lists.SliderList
        table_rod = self.Lists.RodList
        for i in range(len(table_line)):
            a = table_line[i]['start']
            b = table_line[i]['end']
            case1 = table_point[a]['x']==table_point[b]['x']
            case2 = table_point[a]['y']==table_point[b]['y']
            if case1 and case2:
                if b==0: table_point[a]['x'] += 0.01
                else: table_point[b]['x'] += 0.01
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
        Result = self.PathSolvingReqs.result[row]
        #A-C-B-C-E
        Anum = Point.rowCount()+0
        Dnum = Point.rowCount()+1
        Bnum = Point.rowCount()+2
        Cnum = Point.rowCount()+3
        Enum = Point.rowCount()+4
        for i in range(1, len(data)):
            self.Lists.editTable(Point, 'Point', False, *[str(data[i]['x']), str(data[i]['y']), i<3])
            self.Lists.styleAdd(Point_Style, 'Green', '10' if i<3 else '5', 'Blue' if i<3 else 'Green')
        self.Lists.editTable(Chain, 'Chain', False,
            *["Point{}".format(Bnum), "Point{}".format(Cnum), "Point{}".format(Enum),
            str(Result['L1']), str(Result['L4']), str(Result['L3'])])
        self.Lists.editTable(Link, 'Line', False, *["Point{}".format(Anum), "Point{}".format(Bnum), str(Result['L0'])])
        self.Lists.editTable(Link, 'Line', False, *["Point{}".format(Dnum), "Point{}".format(Cnum), str(Result['L2'])])
        self.Lists.editTable(Shaft, 'Shaft', False, *["Point{}".format(Anum), "Point{}".format(Bnum), "0", "360", "0", False])
        print("Generate Result Merged.")
    
    def lineNodeReversion(self, tablePoint, row):
        start = self.Lists.PointList[self.Lists.LinesList[row]['start']]
        end = self.Lists.PointList[self.Lists.LinesList[row]['end']]
        if end['fix']==False:
            x = str(end['x'])
            y = str(end['y']-2*(end['y']-start['y']))
            self.Lists.editTable(tablePoint, 'Point', False, *[x, y, False, self.Lists.LinesList[row]['end']])
        elif start['fix']==False:
            x = str(start['x'])
            y = str(start['y']-2*(start['y']-end['y']))
            self.Lists.editTable(tablePoint, 'Point', False, *[x, y, False, self.Lists.LinesList[row]['start']])
