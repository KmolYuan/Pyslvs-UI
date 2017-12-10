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

from ...QtModules import *
from ...graphics.color import colorNum
from networkx import shell_layout, nx_agraph, random_layout

def graph(G, width, engine):
    if engine=="random":
        pos_engine = {k:(x*200, y*200) for k, (x, y) in random_layout(G).items()}.items()
    elif engine=="shell":
        pos_engine = shell_layout(G, scale=100).items()
    else:
        pos_engine = nx_agraph.graphviz_layout(G, prog=engine).items() #, prog="circo", args="-Goverlap=false"
    pos = {k:(round(float(x), 4), round(float(y), 4)) for k, (x, y) in pos_engine}
    x_cen = (max(x for x, y in pos.values())+min(x for x, y in pos.values()))/2
    y_cen = (max(y for x, y in pos.values())+min(y for x, y in pos.values()))/2
    pos = {k:(x-x_cen, y-y_cen) for k, (x, y) in pos.items()}
    rect = [max(max(x for x, y in pos.values()), max(y for x, y in pos.values()))*2*1.2]*2
    pixmap = QPixmap(*rect)
    painter = QPainter(pixmap)
    painter.fillRect(pixmap.rect(), QBrush(Qt.white))
    painter.translate(pixmap.width()/2, pixmap.height()/2)
    pen = QPen(Qt.black)
    pen.setWidth(5)
    painter.setPen(pen)
    for l1, l2 in G.edges:
        painter.drawLine(QPointF(*pos[l1]), QPointF(*pos[l2]))
    r = 5
    for k, (x, y) in pos.items():
        color = colorNum(len(list(G.neighbors(k)))-1)
        pen.setColor(color)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(x, y), r, r)
    painter.end()
    return QIcon(pixmap.scaledToWidth(width))
