# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ..QtModules import *
from .elements import VPath, VPaths
from .listProcess import Lists, Designs
import traceback, logging
from xml.etree import ElementTree as ET
from xml.dom import minidom
import csv, datetime
def timeNow():
    now = datetime.datetime.now()
    return "{:d}/{:d}/{:d} {:d}:{:d}".format(now.year, now.month, now.day, now.hour, now.minute)
from ..kernel.pyslvs_algorithm.TS import Direction

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
    def updateTime(self):
        self.form.lastTime = timeNow()
    def updateAuthorDescription(self, author, description):
        self.form.author = author
        self.form.description = description
    
    #Check, Read, Write, Reset
    def check(self, fileName, data):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='':
            if type(data)!=list:
                suffix = 'xml'
            else:
                suffix = 'csv'
        print("Get: [{}]".format(fileName))
        try:
            if suffix=='xml':
                if bool(data)==False:
                    tree = ET.ElementTree(file=fileName)
                    data = tree.getroot()
                if self.args.file_data:
                    ET.dump(data)
                n = data.tag=='pyslvs' and data.find('info')!=None
            elif suffix=='csv':
                if bool(data)==False:
                    with open(fileName, newline=str()) as stream:
                        reader = csv.reader(stream, delimiter=' ', quotechar='|')
                        for row in reader:
                            data += ' '.join(row).split('\t,')
                if self.args.file_data:
                    print(data)
                n = (len([e for e, x in enumerate(data) if x=='_info_'])==4 and
                    len([e for e, x in enumerate(data) if x=='_table_'])==8 and
                    len([e for e, x in enumerate(data) if x=='_design_'])==2)
            return n, data
        except:
            return False, list()
    def read(self, fileName, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml':
            errorInfo = self.readXMLMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        elif suffix=='csv':
            errorInfo = self.readCSVMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        elif suffix=='':
            if type(data)!=list:
                errorInfo = self.readXMLMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
            else:
                errorInfo = self.readCSVMerge(data, Point, Link, Chain, Shaft, Slider, Rod, Parameter)
        self.form.Stack = self.FileState.index()
        self.form.fileName = QFileInfo(fileName)
        return errorInfo
    
    def ReadError(self, e, part, errorInfo):
        logging.basicConfig(filename='pyslvs_error.log', filemode='a', level=logging.WARNING)
        logging.exception("Exception Happened.")
        traceback.print_tb(e.__traceback__)
        errorInfo.append(part)
        print(e)
    
    def readXMLMerge(self, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        errorInfo = list()
        def ReadError(e, part):
            self.ReadError(e, part, errorInfo)
        #info
        info = data.find('info')
        try:
            author = info.find('author').text
        except Exception as e:
            author = 'Anonymous'
            ReadError(e, "Author Information")
        try:
            description = info.find('description').text
        except Exception as e:
            description = str()
            ReadError(e, "Description Information")
        try:
            lastTime = info.find('lastTime').text
        except Exception as e:
            lastTime = timeNow()
            ReadError(e, "Date Information")
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
                    try:
                        self.Lists.editTable(Parameter, tableName, False, element.find('val').text, element.find('commit').text)
                    except Exception as e:
                        ReadError(e, 'Parameter')
            elif tableName=='Point' and not 'Parameter' in errorInfo:
                elements = table.findall('element')
                for element in elements:
                    try:
                        self.Lists.editTable(Point, tableName, False, element.find('x').text, element.find('y').text, element.find('fix').text=='True', element.find('color').text)
                    except Exception as e:
                        ReadError(e, tableName)
            elif not 'Parameter' in errorInfo and not 'Point' in errorInfo:
                for tableTag, Qtable in zip(['Line', 'Chain', 'Shaft', 'Slider', 'Rod'], [Link, Chain, Shaft, Slider, Rod]):
                    if tableName==tableTag:
                        elements = table.findall('element')
                        for element in elements:
                            tableArgs = [self.pNumAdd(arg.text, b) if 'Point' in arg.text else arg.text for arg in element]
                            try:
                                self.Lists.editTable(Qtable, tableTag, False, *tableArgs)
                            except Exception as e:
                                ReadError(e, tableName)
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
            except Exception as e:
                ReadError(e, 'Design')
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
                if pathdata:
                    self.Lists.setPath(pathdata)
            except Exception as e:
                ReadError(e, 'Path')
        #algorithm
        algorithm = data.find('algorithm')
        if algorithm:
            results = list()
            try:
                for mechanism in algorithm.findall('mechanism'):
                    #Root
                    result = dict()
                    result['Algorithm'] = mechanism.find('Algorithm').text
                    for tag in ['time', 'Ax', 'Ay', 'Dx', 'Dy']:
                        result[tag] = round(float(mechanism.find(tag).text), 4)
                    interruptedGeneration = mechanism.find('interruptedGeneration')
                    result['interruptedGeneration'] = 'N/A' if interruptedGeneration==None else interruptedGeneration.text
                    for node in mechanism.findall('./'):
                        if 'L' in node.tag:
                            result[node.tag] = round(float(node.text), 4)
                    #mechanismParams(Misc)
                    result['mechanismParams'] = dict()
                    mechanismParams = mechanism.find('mechanismParams')
                    for tag in ['Driving', 'Follower', 'Link', 'Target', 'ExpressionName', 'Expression']:
                        result['mechanismParams'][tag] = mechanismParams.find(tag).text
                    result['mechanismParams']['VARS'] = int(mechanismParams.find('VARS').text)
                    #mechanismParams-->targetPath
                    result['mechanismParams']['targetPath'] = tuple(tuple(round(float(val), 4) for val in dot.text.split('@'))
                        for dot in mechanismParams.find('targetPath').findall('dot'))
                    #mechanismParams-->constraint
                    result['mechanismParams']['constraint'] = [{tag:constraint.find(tag).text for tag in ['driver', 'follower', 'connect']}
                        for constraint in mechanismParams.findall('constraint')]
                    #mechanismParams-->formula
                    result['mechanismParams']['formula'] = [formula.text for formula in mechanismParams.findall('formula')]
                    #generateData(Misc)
                    result['generateData'] = dict()
                    generateData = mechanism.find('generateData')
                    if generateData==None: generateData = mechanism.find('GenerateData')
                    for tag in ['nParm', 'maxGen', 'report']:
                        result['generateData'][tag] = int(generateData.find(tag).text)
                    #generateData-->upper / lower
                    result['generateData']['upper'] = [float(upper.text) for upper in generateData.findall('upper')]
                    result['generateData']['lower'] = [float(lower.text) for lower in generateData.findall('lower')]
                    #algorithmPrams(Misc)
                    result['algorithmPrams'] = {e.tag:int(e.text) if e.tag in ['nPop', 'n', 'NP', 'strategy'] else float(e.text)
                        for e in list(mechanism.find('algorithmPrams'))}
                    #hardwareInfo
                    hardwareInfo = mechanism.find('hardwareInfo')
                    result['hardwareInfo'] = {e.tag:e.text for e in ['os', 'memory', 'cpu', 'network']
                        for e in list(hardwareInfo)} if hardwareInfo!=None else {'os':'N/A', 'memory':'N/A', 'cpu':'N/A', 'network':'N/A'}
                    #algorithm_fitness
                    result['TimeAndFitness'] = [tuple(float(v) for v in val.text.split('@')) if '@' in val.text else float(val.text)
                        for val in mechanism.findall('fitness')]
                    results.append(result)
                self.Designs.addResult(results)
            except Exception as e:
                ReadError(e, 'Algorithm')
        return errorInfo
    
    def readCSVMerge(self, data, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        errorInfo = list()
        def ReadError(e, part):
            self.ReadError(e, part, errorInfo)
        #info
        infoIndex = [e for e, x in enumerate(data) if '_info_' in x]
        try:
            author = data[infoIndex[0]:infoIndex[1]+1][1].replace('"', '')
        except Exception as e:
            author = 'Anonymous'
            ReadError(e, "Author Information")
        try:
            description = '\n'.join(data[infoIndex[1]:infoIndex[2]+1][1:-1])
            if '\n' in description:
                description = description[1:-1]
        except Exception as e:
            description = str()
            ReadError(e, "Description Information")
        try:
            lastTime = data[infoIndex[2]:infoIndex[3]+1][1]
        except Exception as e:
            lastTime = timeNow()
            ReadError(e, "Date Information")
        self.form.author = author
        self.form.description = description
        self.form.lastTime = lastTime
        b = Point.rowCount()-1 #point base number
        #table
        tableIndex = [e for e, x in enumerate(data) if '_table_' in x]
        try:
            li = data[tableIndex[6]:tableIndex[7]]
            if (len(li)-1)%3==0:
                for i in range(1, len(li), 3):
                    self.Lists.editTable(Parameter, 'n', False, li[i+1], li[i+2])
            else:
                raise ValueError
        except Exception as e:
            ReadError(e, 'Parameter')
        if not 'Parameter' in errorInfo:
            try:
                li = data[tableIndex[0]:tableIndex[1]]
                if (len(li)-1)%5==0:
                    for i in range(1, len(li), 5):
                        self.Lists.editTable(Point, 'Point', False, li[i+1], li[i+2], li[i+3]=='True', li[i+4])
                else:
                    raise ValueError
            except Exception as e:
                ReadError(e, 'Point')
        if not 'Parameter' in errorInfo and not 'Point' in errorInfo:
            try:
                li = data[tableIndex[1]:tableIndex[2]]
                if (len(li)-1)%4==0:
                    for i in range(1, len(li), 4):
                        self.Lists.editTable(Link, 'Line', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), li[i+3])
                else:
                    raise ValueError
            except Exception as e:
                ReadError(e, 'Link')
            try:
                li = data[tableIndex[2]:tableIndex[3]]
                if (len(li)-1)%7==0:
                    for i in range(1, len(li), 7):
                        self.Lists.editTable(Chain, 'Chain', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b), li[i+4], li[i+5], li[i+6])
                else:
                    raise ValueError
            except Exception as e:
                ReadError(e, 'Chain')
            try:
                li = data[tableIndex[3]:tableIndex[4]]
                if (len(li)-1)%6==0:
                    for i in range(1, len(li), 6):
                        self.Lists.editTable(Shaft, 'Shaft', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), li[i+3], li[i+4], li[i+5])
                else:
                    raise ValueError
            except Exception as e:
                ReadError(e, 'Shaft')
            try:
                li = data[tableIndex[4]:tableIndex[5]]
                if (len(li)-1)%4==0:
                    for i in range(1, len(li), 4):
                        self.Lists.editTable(Slider, 'Slider', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b))
                else:
                    raise ValueError
            except Exception as e:
               ReadError(e, 'Slider')
            try:
                li = data[tableIndex[5]:tableIndex[6]]
                if (len(li)-1)%5==0:
                    for i in range(1, len(li), 5):
                        self.Lists.editTable(Rod, 'Rod', False, self.pNumAdd(li[i+1], b), self.pNumAdd(li[i+2], b), self.pNumAdd(li[i+3], b), li[i+4])
                else:
                    raise ValueError
            except Exception as e:
                ReadError(e, 'Rod')
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
            elif len(li)%itemNum!=0:
                errorInfo.append('Design')
        except Exception as e:
            ReadError(e, 'Design')
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
                        if len(pathSTR)==0:
                            break
                    paths.append(VPath(point, path))
                    if len(pathSTR)==0:
                        break
                pathdata.append(VPaths(shaft, paths))
            if pathdata:
                self.Lists.setPath(pathdata)
        except Exception as e:
            ReadError(e, 'Path')
        return errorInfo
    
    def pNumAdd(self, pointRef, base):
        if pointRef=='Point0':
            return 'Point0'
        else:
            return 'Point{}'.format(int(pointRef.replace('Point', ''))+base)
    
    def write(self, fileName):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml':
            self.writeXML(fileName)
        elif suffix=='csv' or suffix=='':
            self.writeCSV(fileName)
        self.form.Stack = self.FileState.index()
        self.form.fileName = QFileInfo(fileName)
    def writePathOnly(self, fileName):
        suffix = QFileInfo(fileName).suffix().lower()
        if suffix=='xml':
            self.writeXMLPathOnly(fileName)
        elif suffix=='csv' or suffix=='':
            self.writeCSVPathOnly(fileName)
    
    def writeXML(self, fileName):
        root = ET.Element('pyslvs')
        self.writeXMLInfo(root)
        self.writeXMLTable(root)
        self.writeXMLDesign(root)
        self.writeXMLPath(root)
        self.writeXMLAlgorithm(root)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
        with open(fileName, 'w') as f:
            f.write(xmlstr)
    def writeXMLPathOnly(self, fileName):
        root = ET.Element('pyslvs')
        self.writeXMLInfo(root)
        self.writeXMLPath(root)
        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
        with open(fileName, 'w') as f:
            f.write(xmlstr)
    
    def writeXMLInfo(self, root):
        info = ET.SubElement(root, 'info')
        ET.SubElement(info, 'author').text = self.form.author if self.form.author!=str() else 'Anonymous'
        ET.SubElement(info, 'description').text = self.form.description
        ET.SubElement(info, 'lastTime').text = timeNow()
    def writeXMLTable(self, root):
        self.writeTableXML(root, self.Lists.ParameterList)
        self.writeTableXML(root, self.Lists.PointList, 1)
        for List in [self.Lists.LineList, self.Lists.ChainList, self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList]:
            self.writeTableXML(root, List)
    def writeXMLDesign(self, root):
        if self.Designs.TSDirections:
            design = ET.SubElement(root, 'design')
        for e in self.Designs.TSDirections:
            direction = ET.SubElement(design, 'direction')
            for k, v in e.items().items():
                ET.SubElement(direction, k).text = '{}@{}'.format(v[0], v[1]) if type(v)==tuple else str(v)
    def writeXMLPath(self, root):
        if self.Lists.pathData:
            path = ET.SubElement(root, 'path')
        for vpaths in self.Lists.pathData:
            shaft = ET.SubElement(path, 'shaft', name='Shaft{}'.format(vpaths.shaft))
            for vpath in vpaths.paths:
                point = ET.SubElement(shaft, 'point', name='Point{}'.format(vpath.point))
                for dot in vpath.path:
                    ET.SubElement(point, 'dot').text = '{}@{}'.format(dot[0], dot[1])
    def writeXMLAlgorithm(self, root):
        if self.Designs.result:
            algorithm = ET.SubElement(root, 'algorithm')
        for result in self.Designs.result:
            #Root
            mechanism = ET.SubElement(algorithm, 'mechanism')
            for tag in ['Algorithm', 'time', 'Ax', 'Ay', 'Dx', 'Dy']:
                ET.SubElement(mechanism, tag).text = str(result[tag])
            ET.SubElement(mechanism, 'interruptedGeneration').text = result['interruptedGeneration']
            for tag in result.keys():
                if 'L' in tag:
                    ET.SubElement(mechanism, tag).text = str(result[tag])
            #mechanismParams(Misc)
            mechanismParams = ET.SubElement(mechanism, 'mechanismParams')
            for tag in ['Driving', 'Follower', 'Link', 'Target', 'ExpressionName', 'Expression', 'VARS']:
                ET.SubElement(mechanismParams, tag).text = str(result['mechanismParams'][tag])
            #mechanismParams-->targetPath
            targetPath = ET.SubElement(mechanismParams, 'targetPath')
            for x, y in result['mechanismParams']['targetPath']:
                ET.SubElement(targetPath, 'dot').text = '{}@{}'.format(x, y)
            #mechanismParams-->constraint
            for e in result['mechanismParams']['constraint']:
                constraint = ET.SubElement(mechanismParams, 'constraint')
                for tag in ['driver', 'follower', 'connect']:
                    ET.SubElement(constraint, tag).text = e[tag]
            #mechanismParams-->formula
            for e in result['mechanismParams']['formula']:
                ET.SubElement(mechanismParams, 'formula').text = e
            #generateData(Misc)
            generateData = ET.SubElement(mechanism, 'generateData')
            for tag in ['nParm', 'maxGen', 'report']:
                ET.SubElement(generateData, tag).text = str(result['generateData'][tag])
            #generateData-->upper / lower
            for e in result['generateData']['upper']:
                ET.SubElement(generateData, 'upper').text = str(e)
            for e in result['generateData']['lower']:
                ET.SubElement(generateData, 'lower').text = str(e)
            #algorithmPrams(Misc)
            algorithmPrams = ET.SubElement(mechanism, 'algorithmPrams')
            for tag, e in result['algorithmPrams'].items():
                ET.SubElement(algorithmPrams, tag).text = str(e)
            #hardwareInfo
            hardwareInfo = ET.SubElement(mechanism, 'hardwareInfo')
            for tag, e in result['hardwareInfo'].items():
                ET.SubElement(hardwareInfo, tag).text = e
            #algorithm_fitness
            for fitness in result['TimeAndFitness']:
                if type(fitness)==float:
                    ET.SubElement(mechanism, 'fitness').text = str(fitness)
                else:
                    ET.SubElement(mechanism, 'fitness').text = '@'.join([str(e) for e in fitness])
    
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
            for i in range(8):
                writer.writerow(['_table_'])
            for i in range(2):
                writer.writerow(['_design_'])
            self.writeCSVPath(writer)
    
    def writeCSVInfo(self, writer):
        writer.writerows([
            ['_info_'], [self.form.author if self.form.author!=str() else 'Anonymous'],
            ['_info_'], [self.form.description],
            ['_info_'], [timeNow()], ["_info_"]])
    def writeCSVTable(self, writer):
        self.writeTableCSV(writer, self.Lists.PointList, 1)
        for List in [self.Lists.LineList, self.Lists.ChainList,
                self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList, self.Lists.ParameterList]:
            self.writeTableCSV(writer, List)
        writer.writerow(['_table_'])
    def writeCSVDesign(self, writer):
        writer.writerow(['_design_'])
        directions = [['{}:{}\t'.format(k, '{}@{}'.format(v[0], v[1]) if type(v)==tuple else v) for k, v in e.items().items()]
            for e in self.Designs.TSDirections]
        for e in directions:
            writer.writerow([p.replace('\t', '') if e.index(p)==len(e)-1 else p for p in e])
        writer.writerow(['_design_'])
    def writeCSVPath(self, writer):
        writer.writerow(['_path_'])
        for vpaths in self.Lists.pathData:
            writer.writerow(['Shaft{}'.format(vpaths.shaft)])
            for vpath in vpaths.paths:
                writer.writerow([vpath.point])
                writer.writerow(['{}@{}\t'.format(point[0], point[1]) for point in vpath.path])
    
    def reset(self, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        for i in reversed(range(0, Rod.rowCount())):
            Rod.removeRow(i)
        for i in reversed(range(0, Slider.rowCount())):
            Slider.removeRow(i)
        for i in reversed(range(0, Shaft.rowCount())):
            Shaft.removeRow(i)
        for i in reversed(range(0, Chain.rowCount())):
            Chain.removeRow(i)
        for i in reversed(range(0, Link.rowCount())):
            Link.removeRow(i)
        for i in reversed(range(1, Point.rowCount())):
            Point.removeRow(i)
        for i in reversed(range(0, Parameter.rowCount())):
            Parameter.removeRow(i)
        self.Lists.clearPath()
        self.resetAllList()
    
    def writeTableXML(self, tree, List, start=0):
        if type(List)==list:
            List = List[start:]
        if List:
            table = ET.SubElement(tree, 'table', name=List[0].items_tags('')[0])
            for i, e in (enumerate(List) if type(List)==list else List.items()):
                profile = e.items_tags(i+start)
                element = ET.SubElement(table, 'element', name=profile[0])
                for v in profile[1:]:
                    ET.SubElement(element, v[0]).text = 'Point{}'.format(v[1]) if type(v[1])==int else str(v[1])
    
    def writeTableCSV(self, writer, List, start=0):
        if type(List)==list:
            List = List[start:]
        writer.writerow(['_table_'])
        for i, e in (enumerate(List) if type(List)==list else List.items()):
            rowdata = ['{}\t'.format(k) for k in e.items(i+start)]
            rowdata[-1] = rowdata[-1].replace('\t', '')
            writer.writerow(rowdata)
    
    def Obstacles_Exclusion(self):
        table_points = self.Lists.PointList
        for e in table_points:
            e.round()
        for e in self.Lists.LineList:
            a = e.start
            b = e.end
            case1 = table_points[a].x==table_points[b].x
            case2 = table_points[a].y==table_points[b].y
            if case1 and case2:
                if b.fix==True:
                    table_points[a].x += 0.01
                else:
                    table_points[b].x += 0.01
        for e in self.Lists.ChainList:
            a = e.p1
            b = e.p2
            c = e.p3
            if table_points[a].x==table_points[b].x and table_points[a].y==table_points[b].y:
                if b.fix==True:
                    table_points[a].x += 0.01
                else:
                    table_points[b].x += 0.01
            if table_points[b].x==table_points[c].x and table_points[b].y==table_points[c].y:
                if c.fix==True:
                    table_points[b].y += 0.01
                else:
                    table_points[c].y += 0.01
            if table_points[a].x==table_points[c].x and table_points[a].y==table_points[c].y:
                if c.fix==True:
                    table_points[a].y += 0.01
                else:
                    table_points[c].y += 0.01
        return table_points, self.Lists.LineList, self.Lists.ChainList, self.Lists.ShaftList, self.Lists.SliderList, self.Lists.RodList
    
    def Generate_Merge(self, row, startAngle, endAngle, answer, Paths, Point, Link, Chain, Shaft):
        if not (False in answer):
            Result = self.Designs.result[row]
            links_tag = Result['mechanismParams']['Link'].split(',')
            print('Mechanism:\n'+'\n'.join(["{}: {}".format(tag, Result[tag]) for tag in (['Ax', 'Ay', 'Dx', 'Dy']+links_tag)]))
            expression = Result['mechanismParams']['Expression'].split(',')
            expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
            expression_result = [exp[-1] for exp in expression_tag]
            dataAdd = len(self.Lists.PointList)==1
            if not dataAdd:
                self.Lists.clearPath()
            for i, (x, y) in enumerate(answer):
                self.Lists.editTable(Point, 'Point', False, round(x, 4), round(y, 4), i<2, 'Blue' if i<2 else 'Green' if i<len(answer)-1 else 'Brick-Red')
            Rnum = Point.rowCount()-len(expression_result)
            self.Lists.editTable(Link, 'Line', False, "Point{}".format(Rnum-2), "Point{}".format(Rnum), str(Result['L0']))
            #exp = ('B', 'L2', 'L1', 'C', 'D')
            for i, exp in enumerate(expression_tag[1:]):
                p1 = -2 if exp[0]=='A' else expression_result.index(exp[0]) if exp[0] in expression_result else -1
                p2 = -2 if exp[3]=='A' else expression_result.index(exp[3]) if exp[3] in expression_result else -1
                p3 = -2 if exp[-1]=='A' else expression_result.index(exp[-1]) if exp[-1] in expression_result else -1
                self.Lists.editTable(Link, 'Line', False, "Point{}".format(Rnum+p1), "Point{}".format(Rnum+p3), str(Result[exp[1]]))
                self.Lists.editTable(Link, 'Line', False, "Point{}".format(Rnum+p2), "Point{}".format(Rnum+p3), str(Result[exp[2]]))
            self.Lists.editTable(Shaft, 'Shaft', False, "Point{}".format(Rnum-2), "Point{}".format(Rnum), startAngle, endAngle, startAngle, False)
            path_dots = [VPath(Point.rowCount()-len(expression_result)+i, Paths[expression_result[i]]) for i in range(len(expression_result))]
            list_paths = VPaths(Shaft.rowCount()-1, path_dots)
            if dataAdd and not list_paths.isBroken():
                self.Lists.setPath([list_paths])
            print("Generate Result Merged. At: {} deg ~ {} deg.".format(startAngle, endAngle))
            return True
        else:
            return False
    
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
            if len(answer)==2:
                self.Lists.editTable(Point, 'Point', False,
                str(answer[0]), str(answer[1]), False, 'Green')
            elif len(answer)==3:
                if type(direction.get('p3'))==tuple:
                    self.Lists.editTable(Point, 'Point', False, direction.p3[0], direction.p3[1], False, 'Green')
            pNum['answer'] = Point.rowCount()-1
            pNums.append(pNum)
            #Number of Points & Length of Sides
            p1 = int(direction.p1.replace('Point', '')) if type(direction.p1)==str else pNums[direction.p1]['answer'] if type(direction.p1)==int else pNum['p1']
            p2 = int(direction.p2.replace('Point', '')) if type(direction.p2)==str else pNums[direction.p2]['answer'] if type(direction.p2)==int else pNum['p2']
            if direction.Type in ['PLPP', 'PPP']:
                p3 = int(direction.p3.replace('Point', '')) if type(direction.p3)==str else pNums[direction.p3]['answer'] if type(direction.p3)==int else pNum['p3']
            if direction.Type in ['PLAP', 'PLLP', 'PLPP']:
                pA = pNum['answer']
            #Merge options
            table_points = self.Lists.PointList
            if direction.Type in ['PLAP', 'PLLP']:
                if direction.merge==1:
                    self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                elif direction.merge==2:
                    self.Lists.editTable(Link, 'Line', False, p2, pA, str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
                elif direction.merge==3:
                    self.Lists.editTable(Chain, 'Chain', False, p1, pA, p2,
                        str(direction.len1),
                        str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))),
                        str(Pythagorean(table_points[p1], table_points[p2]))
                    )
                elif direction.merge==4:
                    self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Link, 'Line', False, p2, pA,
                        str(direction.get('len2', Pythagorean(table_points[p2], table_points[pA]))))
            elif direction.Type=='PPP':
                if direction.merge==1:
                    self.Lists.editTable(Link, 'Line', False, p1, p3, answer[2])
                elif direction.merge==2:
                    self.Lists.editTable(Link, 'Line', False, p2, p3, answer[1])
                elif direction.merge==3:
                    self.Lists.editTable(Chain, 'Chain', False, p1, p2, p3, answer[0], answer[1], answer[2])
                elif direction.merge==4:
                    self.Lists.editTable(Link, 'Line', False, p1, p3, answer[2])
                    self.Lists.editTable(Link, 'Line', False, p2, p3, answer[1])
            elif direction.Type=='PLPP':
                if direction.merge==1:
                    self.Lists.editTable(Link, 'Line', False, p1, pA, str(direction.len1))
                    self.Lists.editTable(Slider, 'Slider', False, pA, p2, p3)
