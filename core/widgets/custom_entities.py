# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from networkx import Graph
from itertools import chain
from typing import (
    Tuple,
    Dict,
)
from core.QtModules import (
    pyqtSlot,
)
from core.entities import (
    EditPointDialog,
    EditLinkDialog,
)
from core.graphics import edges_view
from core.io import (
    AddTable,
    DeleteTable,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)


class EntitiesCmds:
    
    """A class contain storage functions."""
    
    @pyqtSlot()
    def qAddNormalPoint(self):
        """Add point group using alt key."""
        tabText = self.SynthesisTab.tabText(self.SynthesisTab.currentIndex())
        if tabText == "Dimensional":
            self.addTargetPoint()
        else:
            self.addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    def addNormalPoint(self):
        """Add a point (not fixed)."""
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    def addFixedPoint(self):
        """Add a point (fixed)."""
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, True)
    
    def addPoint(self,
        x: float,
        y: float,
        fixed: bool =False,
        color: str =None
    ) -> int:
        """Add an ordinary point.
        Return the row count of new point.
        """
        rowCount = self.Entities_Point.rowCount()
        if fixed:
            links = 'ground'
            if color is None:
                color = 'Blue'
        else:
            links = ''
            if color is None:
                color = 'Green'
        self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
        self.CommandStack.push(AddTable(self.Entities_Point))
        self.CommandStack.push(EditPointTable(
            rowCount,
            self.Entities_Point,
            self.Entities_Link,
            [links, 'R', color, x, y]
        ))
        self.CommandStack.endMacro()
        return rowCount
    
    def addPointsByGraph(self,
        G: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: int
    ):
        """Add points by networkx graph and position dict."""
        base_count = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Number and Type Synthesis}"
        )
        for i in range(len(pos)):
            self.addPoint(*pos[i])
        for link in G.nodes:
            self.addLink(self.__getLinkSerialNumber(), 'Blue', [
                base_count + n
                for n, edge in edges_view(G) if (link in edge)
            ])
            if link == ground_link:
                ground = self.Entities_Link.rowCount()-1
        self.CommandStack.endMacro()
        if ground_link is not None:
            self.constrainLink(ground)
    
    @pyqtSlot(list)
    def addNormalLink(self, points: Tuple[int]):
        """Add a link."""
        self.addLink(self.__getLinkSerialNumber(), 'Blue', points)
    
    def addLink(self, name: str, color: str, points: Tuple[int] = ()):
        """Push a new link command to stack."""
        linkArgs = [name, color, ','.join('Point{}'.format(i) for i in points)]
        self.CommandStack.beginMacro("Add {{Link: {}}}".format(name))
        self.CommandStack.push(AddTable(self.Entities_Link))
        self.CommandStack.push(EditLinkTable(
            self.Entities_Link.rowCount() - 1,
            self.Entities_Link,
            self.Entities_Point,
            linkArgs
        ))
        self.CommandStack.endMacro()
    
    def __getLinkSerialNumber(self) -> str:
        """Return a new serial number name of link."""
        names = [
            self.Entities_Link.item(row, 0).text()
            for row in range(self.Entities_Link.rowCount())
        ]
        i = 1
        while "link_{}".format(i) in names:
            i += 1
        return "link_{}".format(i)
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        """Create a point with arguments."""
        self.__editPoint()
    
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self):
        """Edit a point with arguments."""
        row = self.Entities_Point.currentRow()
        self.__editPoint(row if (row > -1) else 0)
    
    def __editPoint(self, row: int = False):
        """Edit point function."""
        dlg = EditPointDialog(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        rowCount = self.Entities_Point.rowCount()
        Type = dlg.Type.currentText().split()[0]
        if Type != 'R':
            Type += ":{}".format(dlg.Angle.value()%360)
        args = [
            ','.join(
                dlg.selected.item(link).text()
                for link in range(dlg.selected.count())
            ),
            Type,
            dlg.Color.currentText(),
            dlg.X_coordinate.value(),
            dlg.Y_coordinate.value()
        ]
        if row is False:
            self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
            self.CommandStack.push(AddTable(self.Entities_Point))
            row = rowCount
        else:
            row = dlg.Point.currentIndex()
            self.CommandStack.beginMacro("Edit {{Point{}}}".format(rowCount))
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        self.CommandStack.endMacro()
    
    def lockPoint(self):
        """Turn a group of points to fixed on ground or not."""
        toFixed = self.action_point_context_lock.isChecked()
        for row in self.Entities_Point.selectedRows():
            newLinks = self.Entities_Point.item(row, 1).text().split(',')
            if toFixed:
                if 'ground' not in newLinks:
                    newLinks.append('ground')
            else:
                if 'ground' in newLinks:
                    newLinks.remove('ground')
            args = self.Entities_Point.rowTexts(row)
            args[0] = ','.join(s for s in newLinks if s)
            self.CommandStack.beginMacro("Edit {{Point{}}}".format(row))
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
            self.CommandStack.endMacro()
    
    def __toMultipleJoint(self, index: int, points: Tuple[int]):
        """Merge points into a multiple joint.
        
        @index: The index of main joint in the sequence.
        """
        row = points[index]
        self.CommandStack.beginMacro(
            "Merge {{{}}} as multiple joint {{{}}}".format(
                ", ".join('Point{}'.format(p) for p in points),
                'Point{}'.format(row)
            )
        )
        points_data = self.Entities_Point.data()
        for i, p in enumerate(points):
            if i == index:
                continue
            newLinks = points_data[row].links
            for l in points_data[p].links:
                #Add new links.
                if l not in newLinks:
                    newLinks.append(l)
            args = self.Entities_Point.rowTexts(row)
            args[0] = ','.join(newLinks)
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
            self.__deletePoint(p)
        self.CommandStack.endMacro()
    
    def clonePoint(self):
        """Clone a point (with orange color)."""
        row = self.Entities_Point.currentRow()
        args = self.Entities_Point.rowTexts(row)
        args[2] = 'Orange'
        rowCount = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Clone {{Point{}}} as {{Point{}}}".format(row, rowCount)
        )
        self.CommandStack.push(AddTable(self.Entities_Point))
        self.CommandStack.push(EditPointTable(
            rowCount,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot(tuple)
    def setFreemoved(self, coordinates: Tuple[Tuple[float, float]]):
        """Free move function."""
        self.CommandStack.beginMacro("Moved {{{}}}".format(", ".join(
            "Point{}".format(c[0]) for c in coordinates
        )))
        for row, (x, y) in coordinates:
            args = self.Entities_Point.rowTexts(row)
            args[3] = x
            args[4] = y
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_New_Link_triggered(self):
        """Create a link with arguments.
        
        + Last than one point:
            
            - Create a new link
        
        + Search method:
            
            - Find the intersection between points that was
                including any link.
            - Add the points that is not in the intersection
                to the link.
        
        + If no, just create a new link by selected points.
        """
        rows = self.Entities_Point.selectedRows()
        if not len(rows) > 1:
            self.__editLink()
            return
        links_all = list(chain(*(
            self.Entities_Point.getLinks(row) for row in rows
        )))
        count_0 = False
        for p in set(links_all):
            if links_all.count(p) > 1:
                count_0 = True
                break
        if (not links_all) or (not count_0):
            self.addNormalLink(rows)
            return
        name = max(set(links_all), key=links_all.count)
        row = self.Entities_Link.findName(name)
        self.CommandStack.beginMacro("Edit {{Link: {}}}".format(name))
        args = self.Entities_Link.rowTexts(row, hasName=True)
        points = set(self.Entities_Link.getPoints(row))
        points.update(rows)
        args[2] = ','.join('Point{}'.format(p) for p in points)
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Edit_Link_triggered(self):
        """Edit a link with arguments."""
        self.__editLink(self.Entities_Link.currentRow())
    
    def __editLink(self, row=False):
        """Edit link function."""
        dlg = EditLinkDialog(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        name = dlg.name_edit.text()
        args = [
            name,
            dlg.Color.currentText(),
            ','.join(
                dlg.selected.item(point).text()
                for point in range(dlg.selected.count())
            )
        ]
        if row is False:
            self.CommandStack.beginMacro("Add {{Link: {}}}".format(name))
            self.CommandStack.push(AddTable(self.Entities_Link))
            row = self.Entities_Link.rowCount()-1
        else:
            row = dlg.Link.currentIndex()
            self.CommandStack.beginMacro("Edit {{Link: {}}}".format(name))
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def releaseGround(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__getLinkSerialNumber()
        args = [name, 'Blue', self.Entities_Link.item(0, 2).text()]
        self.CommandStack.beginMacro(
            "Release ground to {{Link: {}}}".format(name)
        )
        #Free all points.
        self.CommandStack.push(EditLinkTable(
            0,
            self.Entities_Link,
            self.Entities_Point,
            ['ground', 'White', '']
        ))
        #Create new link.
        self.CommandStack.push(AddTable(self.Entities_Link))
        self.CommandStack.push(EditLinkTable(
            self.Entities_Link.rowCount() - 1,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def constrainLink(self, row=None):
        """Turn a link to ground, then delete this link."""
        if row is None:
            row = self.Entities_Link.currentRow()
        name = self.Entities_Link.item(row, 0).text()
        linkArgs = [
            self.Entities_Link.item(row, 0).text(),
            self.Entities_Link.item(row, 1).text(),
            ''
        ]
        newPoints = sorted(
            set(self.Entities_Link.item(0, 2).text().split(',')) |
            set(self.Entities_Link.item(row, 2).text().split(','))
        )
        groundArgs = ['ground', 'White', ','.join(e for e in newPoints if e)]
        self.CommandStack.beginMacro(
            "Constrain {{Link: {}}} to ground".format(name)
        )
        #Turn to ground.
        self.CommandStack.push(EditLinkTable(
            0,
            self.Entities_Link,
            self.Entities_Point,
            groundArgs
        ))
        #Free all points and delete the link.
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            linkArgs
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Link,
            isRename=False
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self):
        """Delete the selected points.
        Be sure that the points will has new position after deleted.
        """
        selections = self.Entities_Point.selectedRows()
        for i, p in enumerate(selections):
            if p > selections[i-1]:
                row = p-i
            else:
                row = p
            self.__deletePoint(row)
    
    def __deletePoint(self, row: int):
        """Push delete point command to stack."""
        args = self.Entities_Point.rowTexts(row)
        args[0] = ''
        self.CommandStack.beginMacro("Delete {{Point{}}}".format(row))
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        for i in range(self.Entities_Link.rowCount()):
            self.CommandStack.push(FixSequenceNumber(
                self.Entities_Link,
                i,
                row
            ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Point,
            isRename=True
        ))
        self.InputsWidget.variableExcluding(row)
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Link_triggered(self):
        """Delete the selected links.
        Be sure that the links will has new position after deleted.
        """
        selections = self.Entities_Link.selectedRows()
        selections = tuple(
            p - i + int(0 in selections) if p>selections[i-1] else p
            for i, p in enumerate(selections)
        )
        for row in selections:
            self.__deleteLink(row)
    
    def __deleteLink(self, row: int):
        """Push delete link command to stack.
        
        Remove link will not remove the points.
        """
        if not row > 0:
            return
        args = self.Entities_Link.rowTexts(row, hasName=True)
        args[2] = ''
        self.CommandStack.beginMacro("Delete {{Link: {}}}".format(
            self.Entities_Link.item(row, 0).text()
        ))
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Link,
            isRename=False
        ))
        self.CommandStack.endMacro()
