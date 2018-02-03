# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang
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

from core.QtModules import *
from core.graphics import colorQt
from core.io import get_from_parenthesis, get_front_of_parenthesis
from networkx import Graph
from math import sqrt
from heapq import nsmallest

def distance_sorted(points):
    #A function to find out distance between two tuple.
    distance = lambda p1, p2: sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    #Re-sort by x coordinate first.
    points = sorted(points, key=lambda c: c[0])
    #Then we arrive next nearest point one by one.
    for i in range(len(points)):
        if i==len(points)-1:
            break
        distanceList = [distance(points[i], p) for p in points]
        j = i + nsmallest(2, range(len(distanceList)-i), key=distanceList[i:].__getitem__)[-1]
        points[i+1], points[j] = points[j], points[i+1]
    return [QPointF(*coordinate) for coordinate in points]

#This generator can keep the numbering be consistent.
def edges_view(G: Graph) -> [int, tuple]:
    for n, e in enumerate(sorted(sorted(e) for e in G.edges)):
        yield n, tuple(e)

#A function use to translate the expression.
def replace_by_dict(d: dict) -> tuple:
    expr = d['Expression'].split(';')
    nd = d['name_dict'].copy()
    tmp_list = []
    for s in expr:
        #Replace P first.
        try:
            s = (
                get_front_of_parenthesis(s, '[') + '[' +
                get_from_parenthesis(s, '[', ')').replace('P', nd['P']) + ')'
            )
        except KeyError:
            pass
        for k in sorted(nd.keys()):
            s = (
                get_front_of_parenthesis(s, '[') + '[' +
                get_from_parenthesis(s, '[', ')').replace(k, nd[k]) + ')'
            )
        tmp_list.append(s)
    return tuple(tmp_list)

class Path:
    __slots__ = ('path', 'show', 'curve')
    
    def __init__(self):
        self.path = ()
        '''
        -1: show all
        -2: hide path.
        '''
        self.show = -1
        #Display mode: The path will be the curve, otherwise the points.
        self.curve = True

#The subclass can draw a blank canvas more easier.
class BaseCanvas(QWidget):
    def __init__(self, parent=None):
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #Origin coordinate
        self.ox = self.width()/2
        self.oy = self.height()/2
        #Canvas zoom rate
        self.rate = 2
        self.zoom = 2 * self.rate
        #Canvas line width
        self.linkWidth = 3
        self.pathWidth = 3
        #Font size
        self.fontSize = 10
        #Show point mark or dimension
        self.showPointMark = True
        self.showDimension = True
        #Path track
        self.Path = Path()
        #Path solving
        self.slvsPath = ()
        self.showSlvsPath = False
    
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.translate(self.ox, self.oy)
        #Draw origin lines.
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.painter.setPen(pen)
        x_l = -self.ox
        x_r = self.width()-self.ox
        self.painter.drawLine(QPointF(x_l, 0), QPointF(x_r, 0))
        y_t = self.height()-self.oy
        y_b = -self.oy
        self.painter.drawLine(QPointF(0, y_b), QPointF(0, y_t))
        #Draw tick.
        Indexing = lambda v: int(v/self.zoom - (v/self.zoom)%5)
        for x in range(Indexing(x_l), Indexing(x_r)+1, 5):
            self.painter.drawLine(QPointF(x*self.zoom, 0), QPointF(x*self.zoom, -10 if x%10==0 else -5))
        for y in range(Indexing(y_b), Indexing(y_t)+1, 5):
            self.painter.drawLine(QPointF(0, y*self.zoom), QPointF(10 if y%10==0 else 5, y*self.zoom))
        '''
        - Please to call the "end" method when ending paint event.
        self.painter.end()
        '''
    
    def drawFrame(self, pen):
        positive_x = self.width()-self.ox
        positive_y = -self.oy
        negative_x = -self.ox
        negative_y = self.height()-self.oy
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(negative_x, positive_y), QPointF(positive_x, positive_y))
        self.painter.drawLine(QPointF(negative_x, negative_y), QPointF(positive_x, negative_y))
        self.painter.drawLine(QPointF(negative_x, positive_y), QPointF(negative_x, negative_y))
        self.painter.drawLine(QPointF(positive_x, positive_y), QPointF(positive_x, negative_y))
    
    def drawPoint(self,
        i: int,
        cx,
        cy,
        fix: bool,
        color: QColor
    ):
        pen = QPen(color)
        pen.setWidth(2)
        self.painter.setPen(pen)
        x = cx*self.zoom
        y = cy*-self.zoom
        if fix:
            bottom = y + 20
            width = 10
            self.painter.drawPolygon(QPointF(x, y), QPointF(x - width, bottom), QPointF(x + width, bottom))
            self.painter.drawEllipse(QPointF(x, y), width, width)
        else:
            self.painter.drawEllipse(QPointF(x, y), 5, 5)
        if self.showPointMark:
            pen.setColor(Qt.darkGray)
            pen.setWidth(2)
            self.painter.setPen(pen)
            self.painter.setFont(QFont("Arial", self.fontSize))
            text = "[{}]".format(i) if type(i)==str else "[Point{}]".format(i)
            if self.showDimension:
                text += ":({:.02f}, {:.02f})".format(cx, cy)
            self.painter.drawText(QPointF(x+6, y-6), text)

#A preview canvas use to show structure diagram.
class PreviewCanvas(BaseCanvas):
    def __init__(self, get_solutions_func, parent):
        super(PreviewCanvas, self).__init__(parent)
        self.showSolutions = True
        #A function should return a tuple of function expression.
        #Like: ("PLAP[P1,a0,L0,P2](P3)", "PLLP[P1,a0,L0,P2](P3)", ...)
        self.get_solutions = get_solutions_func
        self.clear()
    
    def clear(self):
        self.pressed = False
        #Origin graph.
        self.G = Graph()
        #Customize points.
        self.cus = {}
        #Multiple joints.
        self.same = {}
        #Positions.
        self.pos = {}
        #Point status.
        self.status = {}
        #Name dict.
        self.name_dict = {}
        self.grounded = -1
        self.update()
    
    def paintEvent(self, event):
        self.ox = self.width()/2
        self.oy = self.height()/2
        super(PreviewCanvas, self).paintEvent(event)
        r = 4.5
        pen = QPen()
        pen.setWidth(r)
        self.painter.setPen(pen)
        self.painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        for link in self.G.nodes:
            if link==self.grounded:
                continue
            points = []
            #Points that is belong with the link.
            for num, edge in edges_view(self.G):
                if link in edge:
                    if num in self.same:
                        num = self.same[num]
                    points.append((self.pos[num][0], -self.pos[num][1]))
            #Customize points.
            for name, link_ in self.cus.items():
                if link==link_:
                    num = int(name.replace('P', ''))
                    points.append((self.pos[num][0], -self.pos[num][1]))
            self.painter.drawPolygon(*distance_sorted(points))
        self.painter.setFont(QFont("Arial", self.fontSize*1.5))
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            color = colorQt('Dark-Magenta') if self.getStatus(node) else colorQt('Green')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, -y), r, r)
            pen.setColor(colorQt('Black'))
            self.painter.setPen(pen)
            name = 'P{}'.format(node)
            if self.name_dict:
                name = self.name_dict[name]
            self.painter.drawText(QPointF(x + 2*r, -y), name)
        if self.showSolutions:
            for expr in self.get_solutions():
                params = [
                    p for p in get_from_parenthesis(expr, '[', ']').split(',')
                    if 'P' in p
                ]
                params.append(get_from_parenthesis(expr, '(', ')'))
                func = get_front_of_parenthesis(expr, '[')
                color = QColor(121, 171, 252) if func=='PLLP' else QColor(249, 84, 216)
                color.setAlpha(255)
                pen.setColor(color)
                self.painter.setPen(pen)
                color.setAlpha(30)
                self.painter.setBrush(QBrush(color))
                qpoints = []
                for name in params:
                    x, y = self.pos[int(name.replace('P', ''))]
                    qpoints.append(QPointF(x, -y))
                self.painter.drawPolygon(*qpoints)
        self.painter.end()
    
    def setGraph(self, G: Graph, pos: dict):
        self.G = G
        self.pos = pos
        self.status = {k:False for k in pos}
        self.update()
    
    def setGrounded(self, link: int):
        self.grounded = link
        for n, edge in edges_view(self.G):
            self.status[n] = self.grounded in edge
        self.update()
    
    def setStatus(self, point: str, status: bool):
        self.status[int(point.replace('P', ''))] = status
        self.update()
    
    def getStatus(self, point: int) -> bool:
        return self.status[point] or (point in self.same)
    
    def setNameDict(self, name_dict: dict):
        self.name_dict = {v: k for k, v in name_dict.items()}
        self.update()
    
    def setShowSolutions(self, status: bool):
        self.showSolutions = status
        self.update()
    
    def isAllLock(self) -> bool:
        for node, status in self.status.items():
            if not status and node not in self.same:
                return False
        return True
    
    def name_in_same(self, name) -> bool:
        return int(name.replace('P', '')) in self.same
