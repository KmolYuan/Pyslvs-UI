# -*- coding: utf-8 -*-
from ..QtModules import *
from .listProcess import Lists, Designs
import datetime
now = datetime.datetime.now()
from sys import argv #See argv

class File():
    def __init__(self, FileState):
        self.FileState = FileState
        self.resetAllList()
    
    def resetAllList(self):
        self.Lists = Lists(self.FileState)
        self.Designs = Designs(self.FileState)
        self.Script = str()
        self.Stack = 0
        self.form = {
            'fileName':QFileInfo("[New Workbook]"),
            'description':str(),
            'author':'Anonymous',
            'lastTime':'%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute),
            'changed':False}
    def updateTime(self): self.form['lastTime'] = "%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)
    def updateAuthorDescription(self, author, description):
        self.form['author'] = author
        self.form['description'] = description
    
    #Check, Read, Write, Reset
    def check(self, data):
        n1 = len([e for e, x in enumerate(data) if x=='_info_'])==4
        n2 = len([e for e, x in enumerate(data) if x=='_table_'])==9
        n3 = len([e for e, x in enumerate(data) if x=='_design_'])==2
        n4 = len([e for e, x in enumerate(data) if x=='_path_'])==3
        return n1 and n2 and n3 and n4
    def read(self, fileName, data, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        if '--file-data' in argv or '-F' in argv: print(data)
        errorInfo = list()
        #info
        infoIndex = [e for e, x in enumerate(data) if '_info_' in x]
        try: author = data[infoIndex[0]:infoIndex[1]+1][1].replace('"', '')
        except:
            author = str()
            errorInfo.append('Author Information')
        try: description = '\n'.join(data[infoIndex[1]:infoIndex[2]+1][1:-1])[1:-1]
        except:
            description = str()
            errorInfo.append('Description Information')
        try: lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except:
            lastTime = '%d/%d/%d %d:%d'%(now.year, now.month, now.day, now.hour, now.minute)
            errorInfo.append('Date Information')
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[7]:tableIndex[8]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Lists.editTable(Parameter, 'n', False, li[i+1], li[i+2])
        except: errorInfo.append('Parameter')
        try:
            li = data[tableIndex[0]:tableIndex[1]]
            li2 = data[tableIndex[1]:tableIndex[2]]
            if (len(li)-1)%4==0 and (len(li2)-1)%4==0:
                for i in range(1, len(li), 4):
                    self.Lists.editTable(Point, 'Point', False, li[i+1], li[i+2], li[i+3]=='True',
                        styleTable=Point_Style, color=li2[i+1], ringsize=li2[i+2], ringcolor=li2[i+3].replace(",", ""))
        except: errorInfo.append('Point')
        try:
            li = data[tableIndex[2]:tableIndex[3]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lists.editTable(Link, 'Line', False, li[i+1], li[i+2], li[i+3])
        except: errorInfo.append('Link')
        try:
            li = data[tableIndex[3]:tableIndex[4]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Lists.editTable(Chain, 'Chain', False, li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6])
        except: errorInfo.append('Chain')
        try:
            li = data[tableIndex[4]:tableIndex[5]]
            if (len(li)-1)%7==0:
                for i in range(1, len(li), 7): self.Lists.editTable(Shaft, 'Shaft', False, li[i+1], li[i+2], li[i+3], li[i+4], li[i+5], li[i+6]=='True')
        except: errorInfo.append('Shaft')
        try:
            li = data[tableIndex[5]:tableIndex[6]]
            if (len(li)-1)%4==0:
                for i in range(1, len(li), 4): self.Lists.editTable(Slider, 'Slider', False, li[i+1], li[i+2], li[i+3])
        except: errorInfo.append('Slider')
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%5==0:
                for i in range(1, len(li), 5): self.Lists.editTable(Rod, 'Rod', False, li[i+1], li[i+2], li[i+3], li[i+4])
        except: errorInfo.append('Rod')
        #design
        designIndex = [e for e, x in enumerate(data) if '_design_' in x]
        try:
            li = data[designIndex[0]+1:designIndex[1]]
            if len(li)>0 and len(li)%6==0:
                directions = [dict(zip([e.split(':')[0] for e in li[i:i+6]], [e.split(':')[1] for e in li[i:i+6]]))
                    for i in range(0, len(li), 6)]
                directions = [{
                    k:((float(v.split('@')[0]), float(v.split('@')[1])) if '@' in v else float(v) if '.' in v else int(v) if v.isdigit() else v if 'P' in v else v=='True')
                    for k, v in e.items()} for e in directions]
                self.Designs.addDirections(directions)
        except: errorInfo.append('Design')
        #path
        try:
            pathIndex = [e for e, x in enumerate(data) if '_path_' in x]
            li = data[pathIndex[0]+1:pathIndex[1]]
            runList = li
            li = data[pathIndex[1]+1:pathIndex[2]]
            shaftList = [int(e) for e in li]
            li = data[pathIndex[2]+1::]
            path = list()
            path_e = list()
            for i in range(0, len(li)):
                if '+' in li[i]:
                    path.append(path_e)
                    path_e = list()
                else: path_e.append(float(li[i]))
            if path: self.Lists.setPath([path], runList, shaftList)
        except: errorInfo.append('Path')
        if errorInfo: print("The following content(s) contain errors:\n+ {{{}}}".format(', '.join(errorInfo)))
        else: print("Successful loaded contents.")
        self.Stack = self.FileState.index()
        self.form['fileName'] = QFileInfo(fileName)
        self.form['author'] = author
        self.form['description'] = description
        self.form['lastTime'] = lastTime
    
    def write(self, fileName, writer, Point, Point_Style, Link, Chain, Shaft, Slider, Rod, Parameter):
        self.Stack = self.FileState.index()
        #info
        self.form['fileName'] = QFileInfo(fileName)
        writer.writerows([
            ['_info_'], [self.form['author'] if self.form['author']!=str() else 'Anonymous'],
            ['_info_'], [self.form['description']],
            ['_info_'], ["%d/%d/%d %d:%d"%(now.year, now.month, now.day, now.hour, now.minute)], ["_info_"]])
        #table
        self.CSV_write(writer, Point, 4, init=1)
        self.CSV_write(writer, Point_Style, 4, init=1)
        self.CSV_write(writer, Link, 4)
        self.CSV_write(writer, Chain, 7)
        self.CSV_write(writer, Shaft, 7)
        self.CSV_write(writer, Slider, 4)
        self.CSV_write(writer, Rod, 5)
        self.CSV_write(writer, Parameter, 3)
        writer.writerow(['_table_'])
        #design
        writer.writerow(['_design_'])
        directions = [['{}:{}\t'.format(k, '{}@{}'.format(v[0], v[1]) if type(v)==tuple else v) for k, v in e.items()]
            for e in self.Designs.TSDirections]
        for e in directions: writer.writerow([p.replace('\t', '') if e.index(p)==len(e)-1 else p for p in e])
        writer.writerow(['_design_'])
        #path
        writer.writerow(['_path_'])
        if self.Lists.runList:
            rowdata = list()
            for i in range(len(self.Lists.runList)):
                if i == len(self.Lists.runList)-1: rowdata.append(str(self.Lists.runList[i]))
                else: rowdata.append(str(self.Lists.runList[i])+'\t')
            writer.writerow(rowdata)
        writer.writerow(['_path_'])
        if self.Lists.shaftList:
            writer.writerow(self.Lists.shaftList)
        writer.writerow(['_path_'])
        if self.Lists.data:
            for i in range(len(self.Lists.data[0])):
                rowdata = list()
                for j in range(len(self.Lists.data[0][i])): rowdata.append(str(self.Lists.data[0][i][j])+'\t')
                rowdata.append('+')
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
        self.Lists.clearPath()
        self.resetAllList()
    
    def CSV_write(self, writer, table, k, init=0):
        writer.writerow(['_table_'])
        for row in range(init, table.rowCount()):
            rowdata = list()
            for column in range(k):
                item = table.item(row, column)
                cellWidget = table.cellWidget(row, column)
                ending = str() if column==k-1 else '\t'
                if not item is None:
                    if item.text()==str(): content = str(item.checkState()!=Qt.Unchecked)
                    else: content = item.text()
                    rowdata.append(content+ending)
                elif cellWidget: rowdata.append(cellWidget.currentText()+ending)
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
        Result = self.Designs.result[row]
        #A-C-B-C-E
        Anum = Point.rowCount()+0
        Dnum = Point.rowCount()+1
        Bnum = Point.rowCount()+2
        Cnum = Point.rowCount()+3
        Enum = Point.rowCount()+4
        for i in range(1, len(data)): self.Lists.editTable(Point, 'Point', False, str(data[i]['x']), str(data[i]['y']), i<3,
            styleTable=Point_Style, color='Blue' if i<3 else 'Green', ringsize='10' if i<3 else '5', ringcolor='Blue' if i<3 else 'Green')
        self.Lists.editTable(Chain, 'Chain', False, "Point{}".format(Bnum), "Point{}".format(Cnum), "Point{}".format(Enum),
            str(Result['L1']), str(Result['L4']), str(Result['L3']))
        self.Lists.editTable(Link, 'Line', False, "Point{}".format(Anum), "Point{}".format(Bnum), str(Result['L0']))
        self.Lists.editTable(Link, 'Line', False, "Point{}".format(Dnum), "Point{}".format(Cnum), str(Result['L2']))
        self.Lists.editTable(Shaft, 'Shaft', False, "Point{}".format(Anum), "Point{}".format(Bnum), "0", "360", "0", False)
        print("Generate Result Merged.")
