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

from core.QtModules import *
from core.graphics import (
    BaseCanvas,
    distance_sorted,
    colorQt
)
from core.io import get_from_parenthesis
from networkx import Graph
from string import ascii_uppercase
from itertools import product
'''
'CollectionsDialog',
'ConstrainsDialog',
'TargetsDialog',
'SolutionsDialog',
'''
from .TriangularIteration_dialog import *
from .Ui_TriangularIteration import Ui_Form

#This is a generator to get a non-numeric and non-repeat name string.
#('A', 'B', ..., 'AA', 'AB', ..., 'AAA', 'AAB', ...)
def letter_names():
    i = 0
    while True:
        i += 1
        for e in product(ascii_uppercase, repeat=i):
            yield ''.join(e)

class PreviewCanvas(BaseCanvas):
    def __init__(self, parent=None):
        super(PreviewCanvas, self).__init__(parent)
        self.get_joint_number = lambda: parent.joint_name.currentIndex()
        self.pressed = False
        self.clear()
    
    def clear(self):
        self.G = Graph()
        self.pos = {}
        self.status = {}
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
            self.painter.drawPolygon(*distance_sorted([
                (self.pos[n][0], -self.pos[n][1])
                for n, edge in enumerate(self.G.edges) if link in edge
            ]))
        self.painter.setFont(QFont("Arial", self.fontSize*1.5))
        for node, (x, y) in self.pos.items():
            color = colorQt('Dark-Magenta') if self.status[node] else colorQt('Green')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, -y), r, r)
            pen.setColor(colorQt('Black'))
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(x + 2*r, -y), 'P{}'.format(node))
        self.painter.end()
    
    def setGraph(self, G, pos):
        self.G = G
        self.pos = pos
        self.status = {k:False for k in pos}
        self.update()
    
    def setGrounded(self, link: int):
        self.grounded = link
        for n, edge in enumerate(self.G.edges):
            self.status[n] = self.grounded in edge
        self.update()
    
    def setStatus(self, point: str, status: bool):
        self.status[int(point.replace('P', ''))] = status
        self.update()
    
    def mousePressEvent(self, event):
        self.pressed = True
    
    def mouseReleaseEvent(self, event):
        self.pressed = False
    
    def mouseMoveEvent(self, event):
        if self.pressed:
            row = self.get_joint_number()
            if row>-1:
                x = (event.x() - self.ox)
                y = -(event.y() - self.oy)
                self.pos[row] = (x, y)
                self.update()

warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "

class CollectionsTriangularIteration(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(CollectionsTriangularIteration, self).__init__(parent)
        self.setupUi(self)
        self.unsaveFunc = parent.workbookNoSave
        '''
        self.addToCollection = CollectionsStructure.addCollection
        '''
        self.collections = {}
        self.Expression.parm_bind = {}
        self.PreviewWindow = PreviewCanvas(self)
        self.main_layout.insertWidget(0, self.PreviewWindow)
        self.clear_button.clicked.connect(self.clear)
        self.clear()
    
    def addCollections(self, collections):
        self.collections.update(collections)
    
    def clear(self):
        self.collections.clear()
        self.PreviewWindow.clear()
        self.joint_name.clear()
        self.Expression_list.clear()
        self.Expression.parm_bind.clear()
        self.grounded_list.clear()
        self.Driver_list.clear()
        self.Follower_list.clear()
        self.Target_list.clear()
        self.constraint_list.clear()
        self.Link_Expression.clear()
        self.Expression.clear()
        for label in [
            self.Expression_list_label,
            self.grounded_label,
            self.Driver_label,
            self.Follower_label,
            self.Target_label
        ]:
            self.setWarning(label, True)
    
    def setWarning(self, label, warning: bool):
        label.setText(label.text().replace(warning_icon, ''))
        if warning:
            label.setText(warning_icon + label.text())
    
    @pyqtSlot()
    def on_addToCollection_button_clicked(self):
        self.addToCollection(tuple(self.PreviewWindow.G.edges))
    
    @pyqtSlot(Graph, dict)
    def setGraph(self, G, pos):
        self.clear()
        self.PreviewWindow.setGraph(G, pos)
        for link in G.nodes:
            self.grounded_list.addItem("({})".format(", ".join(
                'P{}'.format(n)
                for n, edge in enumerate(G.edges)
                if link in edge
            )))
        #Point name as (P1, P2, P3, ...).
        for node in pos:
            self.joint_name.addItem('P{}'.format(node))
    
    @pyqtSlot(int)
    def on_grounded_list_currentRowChanged(self, row):
        self.setWarning(self.grounded_label, not row>-1)
        self.PreviewWindow.setGrounded(row)
        self.on_joint_name_currentIndexChanged()
        self.Expression_list.clear()
        self.Expression.clear()
        self.Follower_list.clear()
        self.Driver_list.clear()
        if row>-1:
            self.Follower_list.addItems(
                self.grounded_list.currentItem().text()
                .replace('(', '')
                .replace(')', '')
                .split(", ")
            )
        self.setWarning(self.Follower_label, not row>-1)
        self.setWarning(self.Driver_label, True)
        self.setWarning(self.Expression_list_label, True)
    
    @pyqtSlot(int)
    def on_joint_name_currentIndexChanged(self, index=None):
        if index is None:
            index = self.joint_name.currentIndex()
        if index>-1:
            status = self.PreviewWindow.status[index]
            self.status.setText("Known" if status else "Not known")
            self.PLAP_solution.setEnabled(not status)
            self.PLLP_solution.setEnabled(not status)
        else:
            self.status.setText("No status")
            self.PLAP_solution.setEnabled(False)
            self.PLLP_solution.setEnabled(False)
    
    @pyqtSlot()
    def on_Driver_add_clicked(self):
        row = self.Follower_list.currentRow()
        if row>-1:
            self.Driver_list.addItem(self.Follower_list.takeItem(row))
            self.setWarning(self.Driver_label, False)
    
    @pyqtSlot()
    def on_Follower_add_clicked(self):
        row = self.Driver_list.currentRow()
        if row>-1:
            self.Follower_list.addItem(self.Driver_list.takeItem(row))
            self.setWarning(self.Driver_label, not bool(self.Driver_list.count()))
    
    def expression(self):
        expr_list = set([])
        for expr in self.Expression.text().split(';'):
            param_list = get_from_parenthesis(expr, '[', ']').split(',')
            param_list.append(get_from_parenthesis(expr, '(', ')'))
            expr_list.update(param_list)
        return expr_list
    
    def getParam(self, angle: bool =False):
        i = 0
        p = '{}{{}}'.format('a' if angle else 'L')
        while p.format(i) in self.expression():
            i += 1
        return i
    
    def get_currentMechanismParams(self):
        name_dict = self.Expression.parm_bind
        return {
            #To keep the origin graph.
            'Graph':tuple(self.PreviewWindow.G.edges),
            #To keep the position of points.
            'pos':self.PreviewWindow.pos.copy(),
            'Driver':{
                name_dict[self.Driver_list.item().text()]:None
                for row in range(self.Driver_list.count())
            },
            'Follower':{
                name_dict[self.Follower_list.item().text()]:None
                for row in range(self.Follower_list.count())
            },
            'Target':{
                name_dict[self.Target_list.item().text()]:None
                for row in range(self.Target_list.count())
            },
            'Link_Expression':self.Link_Expression.text(),
            'Expression':self.Expression.text(),
            'constraint':[tuple(
                name_dict[name]
                for name in self.constraint_list.item(row).text().split(',')
            ) for row in range(self.constraint_list.count())]
        }
    
    @pyqtSlot()
    def on_load_button_clicked(self):
        dlg = CollectionsDialog(self)
        dlg.show()
        if dlg.exec_():
            print(dlg.mechanismParams)
    
    @pyqtSlot()
    def on_constrains_button_clicked(self):
        dlg = ConstrainsDialog(self)
        dlg.show()
        if dlg.exec_():
            self.constraint_list.clear()
            for row in range(dlg.main_list.count()):
                self.constraint_list.addItem(dlg.main_list.item(row).text())
    
    @pyqtSlot()
    def on_Target_button_clicked(self):
        dlg = TargetsDialog(self)
        dlg.show()
        if dlg.exec_():
            self.Target_list.clear()
            for row in range(dlg.targets_list.count()):
                self.Target_list.addItem(dlg.targets_list.item(row).text())
    
    @pyqtSlot()
    def on_PLAP_solution_clicked(self):
        dlg = SolutionsDialog('PLAP', self)
        dlg.show()
        if dlg.exec_():
            point = self.joint_name.currentText()
            item = QListWidgetItem()
            self.Expression_list.addItem(item)
            item.setText("PLAP[{},{},{},{}]({})".format(
                dlg.point_A.currentText(),
                'a{}'.format(self.getParam(angle=True)),
                'L{}'.format(self.getParam()),
                dlg.point_B.currentText(),
                point
            ))
            self.on_joint_name_currentIndexChanged()
            self.PreviewWindow.setStatus(point, True)
            self.setWarning(self.Expression_list_label, False)
    
    @pyqtSlot()
    def on_PLLP_solution_clicked(self):
        dlg = SolutionsDialog('PLLP', self)
        dlg.show()
        if dlg.exec_():
            point = self.joint_name.currentText()
            link_num = self.getParam()
            item = QListWidgetItem()
            self.Expression_list.addItem(item)
            item.setText("PLLP[{},{},{},{}]({})".format(
                dlg.point_A.currentText(),
                'L{}'.format(link_num),
                'L{}'.format(link_num + 1),
                dlg.point_B.currentText(),
                point
            ))
            self.on_joint_name_currentIndexChanged()
            self.PreviewWindow.setStatus(point, True)
            self.setWarning(self.Expression_list_label, False)
    
    @pyqtSlot(QListWidgetItem)
    def on_Expression_list_itemChanged(self, item):
        parm_bind = {}
        expr_list = []
        #At this time, we should turn the points number to letter names.
        ln = letter_names()
        for row in range(self.Expression_list.count()):
            expr = self.Expression_list.item(row).text()
            params = get_from_parenthesis(expr, '[', ']').split(',')
            params.append(get_from_parenthesis(expr, '(', ')'))
            for name in params:
                if 'P' in name:
                    #Find out with who was shown earlier.
                    if name not in parm_bind:
                        parm_bind[name] = next(ln)
                    expr = expr.replace(name, parm_bind[name])
            expr_list.append(expr)
        self.Expression.parm_bind = parm_bind
        link_expr_list = []
        self.Expression.setText(';'.join(expr_list))
        for row in range(self.grounded_list.count()):
            try:
                link_expr = ','.join(parm_bind[name] for name in (
                    self.grounded_list.item(row).text()
                    .replace('(', '')
                    .replace(')', '')
                    .split(", ")
                ))
            except KeyError:
                continue
            else:
                if row==self.grounded_list.currentRow():
                    link_expr_list.insert(0, link_expr)
                else:
                    link_expr_list.append(link_expr)
        self.Link_Expression.setText(';'.join(
            ('ground' if i==0 else '') + "[{}]".format(link)
            for i, link in enumerate(link_expr_list)
        ))
    
    @pyqtSlot()
    def on_Expression_clear_clicked(self):
        self.on_grounded_list_currentRowChanged(self.grounded_list.currentRow())
    
    @pyqtSlot()
    def on_save_button_clicked(self):
        name, ok = QInputDialog.getText(self, "Profile name", "Please enter the profile name:")
        if ok:
            i = 0
            while (name not in self.collections) and (not name):
                name = "Structure_{}".format(i)
            self.collections[name] = self.get_currentMechanismParams()
            self.unsaveFunc()
