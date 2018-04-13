# -*- coding: utf-8 -*-

"""All color options in Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QPointF,
    QWidget,
    QSizePolicy,
    QPainter,
    QBrush,
    Qt,
    QPen,
    QColor,
    QFont,
    QPainterPath,
    pyqtSlot,
)
from core.graphics import colorQt, colorPath
from core.io import triangle_expr
from networkx import Graph
from math import (
    radians,
    sin,
    cos,
    atan2,
    isnan
)
from typing import (
    Dict,
    Tuple,
    Sequence,
    Any
)
from functools import reduce

def convex_hull(points: Sequence[Tuple[float, float]]):
    """Returns points on convex hull in CCW order
    according to Graham's scan algorithm.
    """
    
    def cmp(a: float, b: float) -> int:
        return (a > b) - (a < b)
    
    def turn(
        p: Tuple[float, float],
        q: Tuple[float, float],
        r: Tuple[float, float]
    ):
        return cmp(
            (q[0] - p[0])*(r[1] - p[1]) -
            (r[0] - p[0])*(q[1] - p[1]),
            0
        )
    
    def _keep_left(
        hull: Sequence[Tuple[float, float]],
        r: Tuple[float, float]
    ):
        while (len(hull) > 1) and (turn(hull[-2], hull[-1], r) != 1):
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull
    
    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])
    return [
        QPointF(x, y)
        for x, y in (l.extend(u[i] for i in range(1, len(u) - 1)) or l)
    ]

def edges_view(G: Graph) -> Tuple[int, Tuple[int, int]]:
    """This generator can keep the numbering be consistent."""
    for n, edge in enumerate(sorted(sorted(e) for e in G.edges)):
        yield (n, tuple(edge))

def replace_by_dict(d: dict) -> Tuple[str]:
    """A function use to translate the expression."""
    tmp_list = []
    for func, args, target in triangle_expr(d['Expression']):
        tmp_list.append("{}[{}]({})".format(func, ','.join(args), target))
    return tuple(tmp_list)

class Path:
    
    """Path option class."""
    
    __slots__ = ('path', 'show', 'curve')
    
    def __init__(self):
        self.path = ()
        #Show mode parameter.
        self.show = -1
        #Display mode: The path will be the curve, otherwise the points.
        self.curve = True

class BaseCanvas(QWidget):
    
    """The subclass can draw a blank canvas more easier."""
    
    def __init__(self, parent=None):
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        ))
        #Origin coordinate.
        self.ox = self.width()/2
        self.oy = self.height()/2
        #Canvas zoom rate.
        self.rate = 2
        self.zoom = 2 * self.rate
        #Canvas line width.
        self.linkWidth = 3
        self.pathWidth = 3
        #Font size.
        self.fontSize = 15
        #Show point mark or dimension.
        self.showPointMark = True
        self.showDimension = True
        #Path track.
        self.Path = Path()
        #Path solving.
        self.targetPath = {}
        self.showTargetPath = False
    
    def paintEvent(self, event):
        """Using a QPainter under 'self',
        so just change QPen or QBrush before painting.
        """
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
            self.painter.drawLine(
                QPointF(x*self.zoom, 0),
                QPointF(x*self.zoom, -10 if x%10==0 else -5)
            )
        for y in range(Indexing(y_b), Indexing(y_t)+1, 5):
            self.painter.drawLine(
                QPointF(0, y*self.zoom),
                QPointF(10 if y%10==0 else 5, y*self.zoom)
            )
        """Please to call the "end" method when ending paint event.
        
        self.painter.end()
        """
    
    def __drawPoint(self,
        i: int,
        cx,
        cy,
        fix: bool,
        color: QColor
    ):
        """Draw a joint."""
        pen = QPen(color)
        pen.setWidth(2)
        self.painter.setPen(pen)
        x = cx*self.zoom
        y = cy*-self.zoom
        if fix:
            bottom = y + 20
            width = 10
            #Draw a triangle below.
            self.painter.drawPolygon(
                QPointF(x, y),
                QPointF(x - width, bottom),
                QPointF(x + width, bottom)
            )
            self.painter.drawEllipse(QPointF(x, y), width, width)
        else:
            self.painter.drawEllipse(QPointF(x, y), 5, 5)
        if not self.showPointMark:
            return
        pen.setColor(Qt.darkGray)
        pen.setWidth(2)
        self.painter.setPen(pen)
        self.painter.setFont(QFont("Arial", self.fontSize))
        text = "[{}]".format(i) if type(i)==str else "[Point{}]".format(i)
        if self.showDimension:
            text += ":({:.02f}, {:.02f})".format(cx, cy)
        self.painter.drawText(QPointF(x+6, y-6), text)
    
    def __drawTargetPath(self):
        """Draw solving path."""
        pen = QPen()
        pen.setWidth(self.pathWidth)
        for i, name in enumerate(sorted(self.targetPath)):
            path = self.targetPath[name]
            Pen, Dot, Brush = colorPath(i)
            pen.setColor(Pen)
            self.painter.setPen(pen)
            self.painter.setBrush(Brush)
            if len(path) > 1:
                pointPath = QPainterPath()
                for i, (x, y) in enumerate(path):
                    x *= self.zoom
                    y *= -self.zoom
                    self.painter.drawEllipse(QPointF(x, y), 4, 4)
                    if i==0:
                        self.painter.drawText(QPointF(x+6, y-6), name)
                        pointPath.moveTo(x, y)
                    else:
                        x2, y2 = path[i-1]
                        self.__drawArrow(x, y, x2*self.zoom, y2*-self.zoom)
                        pointPath.lineTo(QPointF(x, y))
                self.painter.drawPath(pointPath)
                for x, y in path:
                    pen.setColor(Dot)
                    self.painter.setPen(pen)
                    self.painter.drawEllipse(
                        QPointF(x*self.zoom, y*-self.zoom), 3, 3
                    )
            elif len(path) == 1:
                x = path[0][0]*self.zoom
                y = path[0][1]*-self.zoom
                self.painter.drawText(QPointF(x+6, y-6), name)
                pen.setColor(Dot)
                self.painter.setPen(pen)
                self.painter.drawEllipse(QPointF(x, y), 3, 3)
        self.painter.setBrush(Qt.NoBrush)
    
    def __drawArrow(self, x1: float, y1: float, x2: float, y2: float):
        """Front point -> Back point"""
        a = atan2(y2 - y1, x2 - x1)
        x1 = (x1 + x2) / 2 - 7.5*cos(a)
        y1 = (y1 + y2) / 2 - 7.5*sin(a)
        self.painter.drawLine(
            QPointF(x1, y1),
            QPointF(x1 + 15*cos(a + radians(20)), y1 + 15*sin(a + radians(20)))
        )
        self.painter.drawLine(
            QPointF(x1, y1),
            QPointF(x1 + 15*cos(a - radians(20)), y1 + 15*sin(a - radians(20)))
        )
    
    def __drawCurve(self, path: Sequence[Tuple[float, float]]):
        pointPath = QPainterPath()
        error = False
        for i, (x, y) in enumerate(path):
            if isnan(x):
                error = True
                self.painter.drawPath(pointPath)
                pointPath = QPainterPath()
            else:
                x *= self.zoom
                y *= -self.zoom
                if i==0:
                    pointPath.moveTo(x, y)
                    continue
                if error:
                    pointPath.moveTo(x, y)
                    error = False
                else:
                    pointPath.lineTo(x, y)
        self.painter.drawPath(pointPath)
    
    def __drawDot(self, path: Sequence[Tuple[float, float]]):
        for x, y in path:
            if isnan(x):
                continue
            self.painter.__drawPoint(QPointF(x*self.zoom, y*-self.zoom))

class PreviewCanvas(BaseCanvas):
    
    """A preview canvas use to show structure diagram."""
    
    #Pen width.
    r = 4.5
    
    def __init__(self, get_solutions_func, parent):
        super(PreviewCanvas, self).__init__(parent)
        self.showSolutions = True
        #A function should return a tuple of function expression.
        #Like: ("PLAP[P1,a0,L0,P2](P3)", "PLLP[P1,a0,L0,P2](P3)", ...)
        self.get_solutions = get_solutions_func
        """Attributes.
        
        + Origin graph
        + Customize points: Dict[str, int]
        + Multiple joints: Dict[int, int]
        + Positions: Dict[int, Tuple[float, float]]
        + Joint status: Dict[int, bool]
        + Name dict: Dict['P0', 'A']
        """
        self.G = Graph()
        self.cus = {}
        self.same = {}
        self.pos = {}
        self.status = {}
        self.clear()
    
    def clear(self):
        """Clear the attributes.
        
        + Special marks
        """
        self.G = Graph()
        self.cus.clear()
        self.same.clear()
        self.pos.clear()
        self.status.clear()
        self.grounded = -1
        self.Driver = -1
        self.Target = -1
        self.update()
    
    def paintEvent(self, event):
        """Draw the structure."""
        width = self.width()
        height = self.height()
        self.ox = width/2
        self.oy = height/2
        sq_w = 240
        if width <= height:
            self.zoom = width / sq_w
        else:
            self.zoom = height / sq_w
        super(PreviewCanvas, self).paintEvent(event)
        self.__drawLimit(sq_w)
        pen = QPen()
        pen.setWidth(self.r)
        self.painter.setPen(pen)
        self.painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        #Links
        for link in self.G.nodes:
            if link==self.grounded:
                continue
            points = []
            #Points that is belong with the link.
            for num, edge in edges_view(self.G):
                if link in edge:
                    if num in self.same:
                        num = self.same[num]
                    x, y = self.pos[num]
                    points.append((x*self.zoom, y*-self.zoom))
            #Customize points.
            for name, link_ in self.cus.items():
                if link==link_:
                    num = int(name.replace('P', ''))
                    x, y = self.pos[num]
                    points.append((x*self.zoom, y*-self.zoom))
            self.painter.drawPolygon(*convex_hull(points))
        self.painter.setFont(QFont("Arial", self.fontSize*1.5))
        #Nodes
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            x *= self.zoom
            y *= -self.zoom
            if node in (self.Driver, self.Target):
                if node==self.Driver:
                    pen.setColor(colorQt('Red'))
                elif node==self.Target:
                    pen.setColor(colorQt('Yellow'))
                self.painter.setPen(pen)
                self.painter.drawEllipse(QPointF(x, y), self.r, self.r)
            if self.getStatus(node):
                color = colorQt('Dark-Magenta')
            else:
                color = colorQt('Green')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, y), self.r, self.r)
            pen.setColor(colorQt('Black'))
            self.painter.setPen(pen)
        #Solutions
        if self.showSolutions:
            solutions = ';'.join(self.get_solutions())
            if solutions:
                for func, args, target in triangle_expr(solutions):
                    self.__drawSolution(func, args, target)
        #Text of node.
        pen.setColor(Qt.black)
        self.painter.setPen(pen)
        for node, (x, y) in self.pos.items():
            if node in self.same:
                continue
            self.painter.drawText(QPointF(
                x*self.zoom + 2*self.r,
                y*-self.zoom
            ), 'P{}'.format(node))
        self.painter.end()
    
    def __drawLimit(self, sq_w: int):
        """Center square."""
        limit = sq_w / 2 * self.zoom
        self.painter.drawLine(QPointF(-limit, limit), QPointF(limit, limit))
        self.painter.drawLine(QPointF(-limit, limit), QPointF(-limit, -limit))
        self.painter.drawLine(QPointF(-limit, -limit), QPointF(limit, -limit))
        self.painter.drawLine(QPointF(limit, -limit), QPointF(limit, limit))
    
    def __drawSolution(self, func: str, args: Tuple[str], target: str):
        """Draw the solution triangle."""
        params = [args[0], args[-1]]
        params.append(target)
        if func == 'PLLP':
            color = QColor(121, 171, 252)
        else:
            color = QColor(249, 84, 216)
        color.setAlpha(255)
        pen = QPen()
        pen.setColor(color)
        pen.setWidth(self.r)
        self.painter.setPen(pen)
        for n in (0, 1):
            x, y = self.pos[int(params[-1].replace('P', ''))]
            x2, y2 = self.pos[int(params[n].replace('P', ''))]
            self._BaseCanvas__drawArrow(
                x*self.zoom, y*-self.zoom, x2*self.zoom, y2*-self.zoom
            )
        color.setAlpha(30)
        self.painter.setBrush(QBrush(color))
        qpoints = []
        for name in params:
            x, y = self.pos[int(name.replace('P', ''))]
            qpoints.append(QPointF(x*self.zoom, y*-self.zoom))
        self.painter.drawPolygon(*qpoints)
    
    def setGraph(self, G: Graph, pos: Dict[int, Tuple[float, float]]):
        """Set the graph from NetworkX graph type."""
        self.G = G
        self.pos = pos
        self.status = {k: False for k in pos}
        self.update()
    
    def setGrounded(self, link: int):
        """Set the grounded link number."""
        self.grounded = link
        for n, edge in edges_view(self.G):
            self.status[n] = self.grounded in edge
        for n, link in self.cus.items():
            self.status[int(n.replace('P', ''))] = self.grounded == link
        self.update()
    
    def setDriver(self, nodes: Sequence[int]):
        """Set driver nodes."""
        self.Driver = tuple(nodes)
        self.update()
    
    def setTarget(self, nodes: Sequence[int]):
        """Set target nodes."""
        self.Target = tuple(nodes)
        self.update()
    
    def setStatus(self, point: str, status: bool):
        """Set status node."""
        self.status[int(point.replace('P', ''))] = status
        self.update()
    
    def getStatus(self, point: int) -> bool:
        """Get status. If multiple joints, return true."""
        return self.status[point] or (point in self.same)
    
    @pyqtSlot(bool)
    def setShowSolutions(self, status: bool):
        """Switch solutions."""
        self.showSolutions = status
        self.update()
    
    def from_profile(self, params: Dict[str, Any]):
        """Simple load by dict object."""
        #Add customize joints.
        G = Graph(params['Graph'])
        self.setGraph(G, params['pos'])
        self.cus = params['cus']
        self.same = params['same']
        #Grounded setting.
        Driver = set(params['Driver'])
        Follower = set(params['Follower'])
        for row, link in enumerate(G.nodes):
            points = set(
                'P{}'.format(n)
                for n, edge in edges_view(G) if link in edge
            )
            if (Driver | Follower) <= points:
                self.setGrounded(row)
                break
        #Expression
        for func, args, target in triangle_expr(params['Expression']):
            self.setStatus(target, True)
    
    def isAllLock(self) -> bool:
        """Is all joint has solution."""
        for node, status in self.status.items():
            if not status and node not in self.same:
                return False
        return True
    
    def isMultiple(self, name: str) -> bool:
        """Is the name in 'same'."""
        return int(name.replace('P', '')) in self.same
