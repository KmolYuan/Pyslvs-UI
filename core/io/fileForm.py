# -*- coding: utf-8 -*-
from ..QtModules import *
from .elements import VPath, VPaths
from .listProcess import Lists, Designs
from xml.etree import ElementTree as ET
from xml.dom import minidom
import csv, datetime
def timeNow():
    now = datetime.datetime.now()
    return "{:d}/{:d}/{:d} {:d}:{:d}".format(now.year, now.month, now.day, now.hour, now.minute)
from ..kernel.pyslvs_triangle_solver.TS import solver, Direction

PATHSOLVINGTAG = ['time', 'Ax', 'Ay', 'Dx', 'Dy', 'L0', 'L1', 'L2', 'L3', 'L4',
    'AxMax', 'AyMax', 'DxMax', 'DyMax', 'LMax', 'AxMin', 'AyMin', 'DxMin', 'DyMin', 'LMin',
    'minAngle', 'maxAngle', 'maxGen', 'report']

class Form:
    def __init__(self):
        self.fileName = QFileInfo('[New Workbook]')
        self.description = str()
        self.author = 'Anonymous'
        self.lastTime = timeNow()
        self.changed = False
        self.Stack = 0

class File:
    def __init__(self, FileState, args):
        self.FileState = FileState
        self.args = args
        self.resetAllList()
    
    def resetAllList(self):
        self.Lists = Lists(self.FileState)
        self.Designs = Designs(self.FileState)
        self.Script = str()
        self.form = Form()
        self.FileState.clear()
    def updateTime(self): self.form.lastTime = timeNow()
    def updateAuthorDescription(self, author, description):
        self.form.author = author
        self.form.description = description
    
    #Check, Read, Write, Reset
    def check(self, fileName, data):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='':
            if type(data)!=list: suffix = 'xml'
            else: suffix = 'csv'
        print("Get: [{}]".format(fileName))
        try:
            if suffix=='xml':
                if bool(data)==False:
                    tree = ET.ElementTree(file=fileName)
                    data = tree.getroot()
                if self.args.file_data: ET.dump(data)
                n = data.tag=='pyslvs' and data.find('info')!=None
            elif suffix=='csv':
                if bool(data)==False:
                    with open(fileName, newline=str()) as stream:
                        reader = csv.reader(stream, delimiter=' ', quotechar='|')
                        for row in reader: data += ' '.join(row).split('\t,')
                if self.args.file_data: print(data)
                n = (len([e for e, x in enumerate(data) if x=='_info_'])==4 and
                    len([e for e, x in enumerate(data) if x=='_table_'])==8 and
                    len([e for e, x in enumerate(data) if x=='_design_'])==2)
            return n, data
        except: return False, list()
    def read(self, fileName, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml': errorInfo = self.readXMLMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        elif suffix=='csv': errorInfo = self.readCSVMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        elif suffix=='':
            if type(data)!=list: errorInfo = self.readXMLMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
            else: errorInfo = self.readCSVMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        self.form.Stack = self.FileState.index()
        self.form.fileName = QFileInfo(fileName)
        return errorInfo
    
    def readXMLMerge(self, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        errorInfo = list()
        #info
        info = data.find('info')
        try: author = info.find('author').text
        except:
            author = 'Anonymous'
            errorInfo.append('Author Information')
        try: description = info.find('description').text
        except:
            description = str()
            errorInfo.append('Description Information')
        try: lastTime = info.find('lastTime').text
        except:
            lastTime = timeNow()
            errorInfo.append('Date Information')
        self.form.author = author
        self.form.description = description
        self.form.lastTime = lastTime
        b = Point.rowCount()-1 #point base number
        #table
        for table in data.findall('table'):
            tableName = table.attrib['name']
            if tableName=='n':
                elements = table.findall('element')
                for element in elements:
                    try: self.Lists.editTable(Parameter, tableName, False, element.find('val').text, element.find('commit').text)
                    except: errorInfo.append('Parameter')
            elif tableName=='Point' and not 'Parameter' in errorInfo:
                elements = table.findall('element')
                for element in elements:
                    try: self.Lists.editTable(Point, tableName, False, element.find('x').text, element.find('y').text, element.find('fix').text=='True', element.find('color').text)
                    except: errorInfo.append(tableName)
            elif not 'Parameter' in errorInfo and not 'Point' in errorInfo:
                for tableTag, Qtable in zip(['Line', 'Chain', 'Shaft', 'Slider', 'Rod'], [Link, Chain, Shaft, Slider, Rod]):
                    if tableName==tableTag:
                        elements = table.findall('element')
                        for element in elements:
                            tableArgs = [self.pNumAdd(arg.text, b) if 'Point' in arg.text else arg.text for arg in element]
                            try: self.Lists.editTable(Qtable, tableTag, False, *tableArgs)
                            except: errorInfo.append(tableName)
        #design
        design = data.find('design')
        if design:
            directions = list()
            try:
                for direction in design.findall('direction'):
                    DirectionDict = dict()
                    for arg in direction:
                        v = arg.text
                        DirectionDict[arg.tag] = (
                            (round(float(v.split('@')[0]), 4), round(float(v.split('@')[1]), 4)) if '@' in v else
                            round(float(v), 4) if '.' in v else int(v) if v.isdigit() else v if 'P' in v else v=='True')
                    directions.append(Direction(**DirectionDict))
                self.Designs.setDirections(directions)
            except: errorInfo.append('Design')
        #path
        path = data.find('path')
        if path:
            pathdata = list()
            try:
                for shaft in path.findall('shaft'):
                    shaftIndex = int(shaft.attrib['name'].replace('Shaft', ''))
                    vpaths = list()
                    for point in shaft.findall('point'):
                        pointIndex = int(point.attrib['name'].replace('Point', ''))
                        dots = [tuple(round(float(val), 4) if '.' in val else False for val in dot.text.split('@')) for dot in point.findall('dot')]
                        vpaths.append(VPath(pointIndex, dots))
                    pathdata.append(VPaths(shaftIndex, vpaths))
                if pathdata: self.Lists.setPath(pathdata)
            except: errorInfo.append('Path')
        #algorithm
        algorithm = data.find('algorithm')
        if algorithm:
            results = list()
            try:
                for mechanism in algorithm.findall('mechanism'):
                    result = dict()
                    result['Algorithm'] = mechanism.find('Algorithm').text
                    result['path'] = tuple(tuple(round(float(val), 4) for val in dot.text.split('@')) for dot in mechanism.find('path').findall('dot'))
                    for tag in PATHSOLVINGTAG: result[tag] = round(float(mechanism.find(tag).text) if tag!='maxGen' else int(mechanism.find(tag).text), 4)
                    result['TimeAndFitness'] = [float(val.text) for val in mechanism.find('TimeAndFitness').findall('fitness')]
                    results.append(result)
                self.Designs.addResult(results)
            except: errorInfo.append('Algorithm')
        return errorInfo
    
    def readCSVMerge(self, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        errorInfo = list()
        #info
        infoIndex = [e for e, x in enumerate(data) if '_info_' in x]
        try: author = data[infoIndex[0]:infoIndex[1]+1][1].replace('"', '')
        except:
            author = 'Anonymous'
            errorInfo.append('Author Information')
        try:
            description = '\n'.join(data[infoIndex[1]:infoIndex[2]+1][1:-1])
            if '\n' in description: description = description[1:-1]
        except:
            description = str()
            errorInfo.append('Description Information')
        try: lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except:
            lastTime = timeNow()
            errorInfo.append('Date Information')
        self.form.author = author
        self.form.description = description
        self.form.lastTime = lastTime
        b = Point.rowCount()-1 #point base number
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3): self.Lists.editTable(Parameter, 'n', False, li[i+1], li[i+2])
            else: raise ValueError
        except: errorInfo.append('Parameter')
        if not 'Parameter' in errorInfo:
            try:
                li = data[tableIndex[0]:tableIndex[1]]
                if (len(li)-1)%5==0:
                    for i in range(1, len(li), 5): self.Lists.editTable(Point, 'Point', False, li[i+1], li[i+2], li[i+3]=='True', li[i+4])
                else: raise ValueError
            except: errorInfo.append('Point')
        if not 'Parameter' in errorInfo and not 'Point' in errorInfo:
            try:
                li = data[tableIndex[1]:tableIndex[2]]
                if (len(li)-1)%4==0:
                    for i in range(1, len(li), 4): self.Lists.editTable(Link, 'Line', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), li[i+3])
                else: raise ValueError
            except: errorInfo.append('Link')
            try:
                li = data[tableIndex[2]:tableIndex[3]]
                if (len(li)-1)%7==0:
                    for i in range(1, len(li), 7): self.Lists.editTable(Chain, 'Chain', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b), li[i+4], li[i+5], li[i+6])
                else: raise ValueError
            except: errorInfo.append('Chain')
            try:
                li = data[tableIndex[3]:tableIndex[4]]
                if (len(li)-1)%6==0:
                    for i in range(1, len(li), 6): self.Lists.editTable(Shaft, 'Shaft', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), li[i+3], li[i+4], li[i+5])
                else: raise ValueError
            except: errorInfo.append('Shaft')
            try:
                li = data[tableIndex[4]:tableIndex[5]]
                if (len(li)-1)%4==0:
                    for i in range(1, len(li), 4): self.Lists.editTable(Slider, 'Slider', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b))
                else: raise ValueError
            except: errorInfo.append('Slider')
            try:
                li = data[tableIndex[5]:tableIndex[6]]
                if (len(li)-1)%5==0:
                    for i in range(1, len(li), 5): self.Lists.editTable(Rod, 'Rod', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b), li[i+4])
                else: raise ValueError
            except: errorInfo.append('Rod')
        #design
        designIndex = [e for e, x in enumerate(data) if '_design_' in x]
        try:
            itemNum = 7
            li = data[designIndex[0]+1:designIndex[1]]
            if len(li)>0 and len(li)%itemNum==0:
                directions = list()
                for i in range(0, len(li), itemNum):
                    directionList = li[i:i+itemNum]
                    directionDict = dict()
                    for e in directionList:
                        kv = e.split(':')
                        val = (tuple(round(float(d), 4) for d in kv[1].split('@')) if '@' in kv[1] else
                            round(float(kv[1]), 4) if '.' in kv[1] else int(kv[1]) if kv[1].isdigit() else
                            kv[1] if 'P' in kv[1] else kv[1]=='True')
                        directionDict.update({kv[0]:val})
                    directions.append(Direction(**directionDict))
                self.Designs.setDirections(directions)
            elif len(li)%itemNum!=0: errorInfo.append('Design')
        except: errorInfo.append('Design')
        #path
        try:
            pathIndex = data.index('_path_')
            pathSTR = data[pathIndex+1:]
            pathdata = list()
            while pathSTR:
                shaft = int(pathSTR.pop(0).replace('Shaft', ''))
                paths = list()
                while not 'Shaft' in pathSTR[0] or bool(pathSTR):
                    point = int(pathSTR.pop(0))
                    path = list()
                    while '@' in pathSTR[0]:
                        path.append(tuple(False if e in ['None', 'False'] else round(float(e), 4) for e in pathSTR.pop(0).replace('\t', '').split('@')))
                        if len(pathSTR)==0: break
                    paths.append(VPath(point, path))
                    if len(pathSTR)==0: break
                pathdata.append(VPaths(shaft, paths))
            if pathdata: self.Lists.setPath(pathdata)
        except: errorInfo.append('Path')
        return errorInfo
    
    def pNumAdd(self, pointRef, base):
        if pointRef=='Point0': return 'Point0'
        else: return 'Point{}'.format(int(pointRef.replace('Point', ''))+base)
    
    def write(self, fileName):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml': self.writeXML(fileName)
        elif suffix=='csv' or suffix=='': self.writeCSV(fileName)
        self.form.Stack = self.FileState.index()
        self.form.fileName = QFileInfo(fileName)
    def writePathOnly(self, fileName):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml': self.writeXMLPathOnly(fileName)
        elif suffix=='csv' or suffix=='': self.writeCSVPathOnly(fileName)
    
    def writeXML(self, fileName):
        root = ET.Element('pyslvs')
        self.writeXMLInfo(root)
        self.writeXMLTable(root)
        self.writeXMLDesign(root)
        self.writeXMLPath(root)
        self.writeXMLAlgorithm(root)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
        with open(fileName, 'w') as f: f.write(xmlstr)
    def writeXMLPathOnly(self, fileName):
        root = ET.Element('pyslvs')
        self.writeXMLInfo(root)
        self.writeXMLPath(root)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
        with open(fileName, 'w') as f: f.write(xmlstr)
    
    def writeXMLInfo(self, root):
        info = ET.SubElement(root, 'info')
        ET.SubElement(info, 'author').text = self.form.author if self.form.author!=str() else 'Anonymous'
        ET.SubElement(info, 'description').text = self.form.description
        ET.SubElement(info, 'lastTime').text = timeNow()
    def writeXMLTable(self, root):
        self.writeTableXML(root, self.Lists.ParameterList)
        self.writeTableXML(root, self.Lists.PointList, 1)
        for List in [self.Lists.LineList, self.Lists.ChainList,
            self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList]: self.writeTableXML(root, List)
    def writeXMLDesign(self, root):
        if self.Designs.TSDirections: design = ET.SubElement(root, 'design')
        for e in self.Designs.TSDirections:
            direction = ET.SubElement(design, 'direction')
            for k, v in e.items().items(): ET.SubElement(direction, k).text = '{}@{}'.format(v[0], v[1]) if type(v)==tuple else str(v)
    def writeXMLPath(self, root):
        if self.Lists.pathData: path = ET.SubElement(root, 'path')
        for vpaths in self.Lists.pathData:
            shaft = ET.SubElement(path, 'shaft', name='Shaft{}'.format(vpaths.shaft))
            for vpath in vpaths.paths:
                point = ET.SubElement(shaft, 'point', name='Point{}'.format(vpath.point))
                for dot in vpath.path: ET.SubElement(point, 'dot').text = '{}@{}'.format(dot[0], dot[1])
    def writeXMLAlgorithm(self, root):
        if self.Designs.result: algorithm = ET.SubElement(root, 'algorithm')
        for result in self.Designs.result:
            mechanism = ET.SubElement(algorithm, 'mechanism')
            ET.SubElement(mechanism, 'Algorithm').text = str(result['Algorithm'])
            algorithm_path = ET.SubElement(mechanism, 'path')
            for dot in result['path']: ET.SubElement(algorithm_path, 'dot').text = '{}@{}'.format(dot[0], dot[1])
            for tag in PATHSOLVINGTAG: ET.SubElement(mechanism, tag).text = str(result[tag])
            algorithm_fitness = ET.SubElement(mechanism, 'TimeAndFitness')
            for fitness in result['TimeAndFitness']: ET.SubElement(algorithm_fitness, 'fitness').text = str(fitness)
    
    def writeCSV(self, fileName):
        with open(fileName, 'w', newline=str()) as stream:
            writer = csv.writer(stream)
            self.writeCSVInfo(writer)
            self.writeCSVTable(writer)
            self.writeCSVDesign(writer)
            self.writeCSVPath(writer)
    def writeCSVPathOnly(self, fileName):
        with open(fileName, 'w', newline=str()) as stream:
            writer = csv.writer(stream)
            self.writeCSVInfo(writer)
            for i in range(8): writer.writerow(['_table_'])
            for i in range(2): writer.writerow(['_design_'])
            self.writeCSVPath(writer)
    
    def writeCSVInfo(self, writer):
        writer.writerows([
            ['_info_'], [self.form.author if self.form.author!=str() else 'Anonymous'],
            ['_info_'], [self.form.description],
            ['_info_'], [timeNow()], ["_info_"]])
    def writeCSVTable(self, writer):
        self.writeTableCSV(writer, self.Lists.PointList, 1)
        for List in [self.Lists.LineList, self.Lists.ChainList,
            self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList,
            self.Lists.ParameterList]: self.writeTableCSV(writer, List)
        writer.writerow(['_table_'])
    def writeCSVDesign(self, writer):
        writer.writerow(['_design_'])
        directions = [['{}:{}\t'.format(k, '{}@{}'.format(v[0], v[1]) if type(v)==tuple else v) for k, v in e.items().items()]
            for e in self.Designs.TSDirections]
        for e in directions: writer.writerow([p.replace('\t', '') if e.index(p)==len(e)-1 else p for p in e])
        writer.writerow(['_design_'])
    def writeCSVPath(self, writer):
        writer.writerow(['_path_'])
        for vpaths in self.Lists.pathData:
            writer.writerow(['Shaft{}'.format(vpaths.shaft)])
            for vpath in vpaths.paths:
                writer.writerow([vpath.point])
                writer.writerow(['{}@{}\t'.format(point[0], point[1]) for point in vpath.path])
    
    def reset(self, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        for i in reversed(range(0, Rod.rowCount())): Rod.removeRow(i)
        for i in reversed(range(0, Slider.rowCount())): Slider.removeRow(i)
        for i in reversed(range(0, Shaft.rowCount())): Shaft.removeRow(i)
        for i in reversed(range(0, Chain.rowCount())): Chain.removeRow(i)
        for i in reversed(range(0, Link.rowCount())): Link.removeRow(i)
        for i in reversed(range(1, Point.rowCount())): Point.removeRow(i)
        for i in reversed(range(0, Parameter.rowCount())): Parameter.removeRow(i)
        self.Lists.clearPath()
        self.resetAllList()
    
    def writeTableXML(self, tree, List, start=0):
        if type(List)==list: List = List[start:]
        if List:
            table = ET.SubElement(tree, 'table', name=List[0].items_tags('')[0])
            for i, e in (enumerate(List) if type(List)==list else List.items()):
                profile = e.items_tags(i+start)
                element = ET.SubElement(table, 'element', name=profile[0])
                for v in profile[1:]: ET.SubElement(element, v[0]).text = 'Point{}'.format(v[1]) if type(v[1])==int else str(v[1])
    
    def writeTableCSV(self, writer, List, start=0):
        if type(List)==list: List = List[start:]
        writer.writerow(['_table_'])
        for i, e in (enumerate(List) if type(List)==list else List.items()):
            rowdata = ['{}\t'.format(k) for k in e.items(i+start)]
            rowdata[-1] = rowdata[-1].replace('\t', '')
            writer.writerow(rowdata)
    
    def Obstacles_Exclusion(self):
        table_points = self.Lists.PointList
        for e in table_points: e.round()
        for e in self.Lists.LineList:
            a = e.start
            b = e.end
            case1 = table_points[a].x==table_points[b].x
            case2 = table_points[a].y==table_points[b].y
            if case1 and case2:
                if b.fix==True: table_points[a].x += 0.01
                else: table_points[b].x += 0.01
        for e in self.Lists.ChainList:
            a = e.p1
            b = e.p2
            c = e.p3
            if table_points[a].x==table_points[b].x and table_points[a].y==table_points[b].y:
                if b.fix==True: table_points[a].x += 0.01
                else: table_points[b].x += 0.01
            if table_points[b].x==table_points[c].x and table_points[b].y==table_points[c].y:
                if c.fix==True: table_points[b].y += 0.01
                else: table_points[c].y += 0.01
            if table_points[a].x==table_points[c].x and table_points[a].y==table_points[c].y:
                if c.fix==True: table_points[a].y += 0.01
                else: table_points[c].y += 0.01
        return table_points, self.Lists.LineList, self.Lists.ChainList, self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList
    
    def Generate_Merge(self, row, Point, Link, Chain, Shaft):
        Result = self.Designs.result[row]
        print('Mechanism:\n'+'\n'.join(["{}: {}".format(tag, Result[tag])
            for tag in ['Ax', 'Ay', 'Dx', 'Dy', 'L0', 'L1', 'L2', 'L3', 'L4']]))
        pointAvg = sum([e[1] for e in Result['path']])/len(Result['path'])
        other = (Result['Ay']+Result['Dy'])/2>pointAvg and Result['Ax']<Result['Dx']
        #A-C-B-C-E
        Anum = Point.rowCount()
        Dnum = Anum+1
        Bnum = Dnum+1
        Cnum = Bnum+1
        Enum = Cnum+1
        BPath = list()
        CPath = list()
        EPath = list()
        answer = [False]
        startAngle = False
        endAngle = False
        for a in range(360+1):
            s = solver([
                Direction(p1=(Result['Ax'], Result['Ay']), p2=(Result['Ax']+10, Result['Ay']), len1=Result['L0'], angle=a, other=other), #B
                Direction(p1=0, p2=(Result['Dx'], Result['Dy']), len1=Result['L1'], len2=Result['L2'], other=other), #C
                Direction(p1=0, p2=1, len1=Result['L3'], len2=Result['L4'], other=other)]) #E
            answerT = [(Result['Ax'], Result['Ay']), (Result['Dx'], Result['Dy'])]+s.answer()
            if not False in answerT:
                if startAngle is False:
                    startAngle = float(a)
                    answer = answerT
                endAngle = float(a)
            BPath.append(answerT[2])
            CPath.append(answerT[3])
            EPath.append(answerT[4])
        if not (False in answer):
            dataAdd = len(self.Lists.PointList)==1
            if not dataAdd: self.Lists.clearPath()
            for i, point in enumerate(answer): self.Lists.editTable(Point, 'Point', False,
                point[0] if i<2 else float(round(point[0])), point[1] if i<2 else float(round(point[1])),
                i<2, 'Blue' if i<2 else 'Green' if i<4 else 'Brick-Red')
            self.Lists.editTable(Chain, 'Chain', False, "Point{}".format(Bnum), "Point{}".format(Cnum), "Point{}".format(Enum),
                str(Result['L1']), str(Result['L4']), str(Result['L3']))
            self.Lists.editTable(Link, 'Line', False, "Point{}".format(Anum), "Point{}".format(Bnum), str(Result['L0']))
            self.Lists.editTable(Link, 'Line', False, "Point{}".format(Dnum), "Point{}".format(Cnum), str(Result['L2']))
            self.Lists.editTable(Shaft, 'Shaft', False, "Point{}".format(Anum), "Point{}".format(Bnum), startAngle, endAngle, startAngle, False)
            if dataAdd: self.Lists.setPath([VPaths(Shaft.rowCount()-1, [VPath(Bnum, BPath), VPath(Cnum, CPath), VPath(Enum, EPath)])])
            print("Generate Result Merged. At: {} deg ~ {} deg.".format(startAngle, endAngle))
            return True
        else: return False
    
    def TS_Merge(self, answers, Point, Link, Chain, Slider):
        Pythagorean = lambda p1, p2: ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**(1/2)
        pNums = list()
        for i, answer in enumerate(answers):
            pNum = dict()
            direction = self.Designs.TSDirections[i]
            #New Points
            for p in ['p1', 'p2', 'p3']:
                if type(direction.get(p))==tuple:
                    self.Lists.editTable(Point, 'Point', False, direction.get(p)[0], direction.get(p)[1], False, 'Green')
                    pNum[p] = Point.rowCount()-1
            if len(answer)==2: self.Lists.editTable(Point, 'Point', False,
                str(answer[0]), str(answer[1]), False, 'Green')
            elif len(answer)==3:
                if type(direction.get('p3'))==tuple: self.Lists.editTable(Point, 'Point', False, direction.p3[0], direction.p3[1], False, 'Green')
            pNum['answer'] = Point.rowCount()-1
            pNums.append(pNum)
            #Number of Points & Length of Sides
            p1 = int(direction.p1.replace('Point', '')) if type(direction.p1)==str else pNums[direction.p1]['answer'] if type(direction.p1)==int else pNum['p1']
            p2 = int(direction.p2.replace('Point', '')) if type(direction.p2)==str else pNums[direction.p2]['answer'] if type(direction.p2)==int else pNum['p2']
            if direction.Type in ['PLPP', 'PPP']: p3 = int(direction.p3.replace('Point', '')) if type(direction.p3)==str else pNums[direction.p3]['answer'] if type(direction.p3)==int else pNum['p3']
            if direction.Type in ['PLAP', 'PLLP', 'PLPP']: pA = pNum['answer']
            #Merge options
            table_points = self.Lists.PointList
            if direction.Type in ['PLAP', 'PLLP']:
                if direction.merge==1: self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                elif direction.merge==2: self.Lists.editTable(Link, 'Line', False,
                    p2, pA, str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
                elif direction.merge==3: self.Lists.editTable(Chain, 'Chain', False, p1, pA, p2,
                    str(direction.len1),
                    str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))),
                    str(Pythagorean(table_points[p1], table_points[p2])))
                elif direction.merge==4:
                    self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Link, 'Line', False, p2, pA,
                        str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
            elif direction.Type=='PPP':
                if direction.merge==1: self.Lists.editTable(Link, 'Line', False, p1, p3, answer[2])
                elif direction.merge==2: self.Lists.editTable(Link, 'Line', False, p2, p3, answer[1])
                elif direction.merge==3: self.Lists.editTable(Chain, 'Chain', False, p1, p2, p3, answer[0], answer[1], answer[2])
                elif direction.merge==4:
                    self.Lists.editTable(Link, 'Line', False, p1, p3, answer[2])
                    self.Lists.editTable(Link, 'Line', False, p2, p3, answer[1])
            elif direction.Type=='PLPP':
                if direction.merge==1:
                    self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Slider, 'Slider', False, pA, p2, p3)
