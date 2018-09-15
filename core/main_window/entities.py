# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Dict,
    Union,
    Optional,
)
from itertools import chain
from networkx import Graph
from core.QtModules import pyqtSlot, QAbcMeta
from core.entities import (
    EditPointDialog,
    EditLinkDialog,
)
from core.libs import expr_solving
from core.graphics import edges_view
from core.io import (
    AddTable,
    DeleteTable,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)
from core.widgets import MainWindowUiInterface


class EntitiesMethodInterface(MainWindowUiInterface, metaclass=QAbcMeta):
    
    """Interface class for entities methods."""
    
    def __init__(self):
        super(EntitiesMethodInterface, self).__init__()
    
    def __editPoint(self, row: Union[int, bool] = False):
        """Edit point function."""
        dlg = EditPointDialog(
            self.EntitiesPoint.dataTuple(),
            self.EntitiesLink.dataTuple(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        row_count = self.EntitiesPoint.rowCount()
        type_str = dlg.type_box.currentText().split()[0]
        if type_str != 'R':
            type_str += f":{dlg.angle_box.value() % 360}"
        args = [
            ','.join(
                dlg.selected.item(link).text()
                for link in range(dlg.selected.count())
            ),
            type_str,
            dlg.color_box.currentText(),
            dlg.x_box.value(),
            dlg.y_box.value()
        ]
        if row is False:
            self.CommandStack.beginMacro(f"Add {{Point{row_count}}}")
            self.CommandStack.push(AddTable(self.EntitiesPoint))
            row = row_count
        else:
            row = dlg.name_box.currentIndex()
            self.CommandStack.beginMacro(f"Edit {{Point{row}}}")
        self.CommandStack.push(EditPointTable(
            row,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()
    
    def __editLink(self, row: Union[int, bool] = False):
        """Edit link function."""
        dlg = EditLinkDialog(
            self.EntitiesPoint.dataTuple(),
            self.EntitiesLink.dataTuple(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        name = dlg.name_edit.text()
        args = [
            name,
            dlg.color_box.currentText(),
            ','.join(
                dlg.selected.item(point).text()
                for point in range(dlg.selected.count())
            )
        ]
        if row is False:
            self.CommandStack.beginMacro(f"Add {{Link: {name}}}")
            self.CommandStack.push(AddTable(self.EntitiesLink))
            row = self.EntitiesLink.rowCount() - 1
        else:
            row = dlg.name_box.currentIndex()
            self.CommandStack.beginMacro(f"Edit {{Link: {name}}}")
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()
    
    def __getLinkSerialNumber(self) -> str:
        """Return a new serial number name of link."""
        names = {
            self.EntitiesLink.item(row, 0).text()
            for row in range(self.EntitiesLink.rowCount())
        }
        i = 1
        while f"link_{i}" in names:
            i += 1
        return f"link_{i}"

    @pyqtSlot(name='on_action_Delete_Link_triggered')
    def deleteLink(self, row: int):
        """Push delete link command to stack.
        
        Remove link will not remove the points.
        """
        if not row > 0:
            return
        args = self.EntitiesLink.rowTexts(row, has_name=True)
        args[2] = ''
        name = self.EntitiesLink.item(row, 0).text()
        self.CommandStack.beginMacro(f"Delete {{Link: {name}}}")
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.EntitiesLink,
            is_rename=False
        ))
        self.CommandStack.endMacro()

    @pyqtSlot(name='on_action_Delete_Point_triggered')
    def deletePoint(self, row: int):
        """Push delete point command to stack."""
        args = self.EntitiesPoint.rowTexts(row)
        args[0] = ''
        self.CommandStack.beginMacro(f"Delete {{Point{row}}}")
        self.CommandStack.push(EditPointTable(
            row,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        for i in range(self.EntitiesLink.rowCount()):
            self.CommandStack.push(FixSequenceNumber(
                self.EntitiesLink,
                i,
                row
            ))
        self.CommandStack.push(DeleteTable(
            row,
            self.EntitiesPoint,
            is_rename=True
        ))
        self.InputsWidget.variableExcluding(row)
        self.CommandStack.endMacro()
    
    @pyqtSlot(float, float)
    def qAddNormalPoint(self, x: float, y: float):
        """Add point group using alt key."""
        if self.SynthesisTab.currentIndex() == 2:
            self.addTargetPoint()
        else:
            self.addPoint(x, y, False)
    
    def addNormalPoint(self):
        """Add a point (not fixed)."""
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    def addFixedPoint(self):
        """Add a point (fixed)."""
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, True)
    
    def addPoint(
        self,
        x: float,
        y: float,
        fixed: bool = False,
        color: Optional[str] = None
    ) -> int:
        """Add an ordinary point.
        Return the row count of new point.
        """
        row_count = self.EntitiesPoint.rowCount()
        if fixed:
            links = 'ground'
            if color is None:
                color = 'Blue'
        else:
            links = ''
            if color is None:
                color = 'Green'
        self.CommandStack.beginMacro(f"Add {{Point{row_count}}}")
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            row_count,
            self.EntitiesPoint,
            self.EntitiesLink,
            [links, 'R', color, x, y]
        ))
        self.CommandStack.endMacro()
        return row_count
    
    def addPointsByGraph(
        self,
        graph: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: Optional[int]
    ):
        """Add points by NetworkX graph and position dict."""
        base_count = self.EntitiesPoint.rowCount()
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Number and Type Synthesis}"
        )
        
        for i in range(len(pos)):
            self.addPoint(*pos[i])
        
        ground: Optional[int] = None
        for link in graph.nodes:
            self.addLink(self.__getLinkSerialNumber(), 'Blue', [
                base_count + n for n, edge in edges_view(graph) if link in edge
            ])
            if link == ground_link:
                ground = self.EntitiesLink.rowCount() - 1
        self.CommandStack.endMacro()
        if ground_link is not None:
            self.constrainLink(ground)

    @pyqtSlot(list)
    def addNormalLink(self, points: Sequence[int]):
        """Add a link."""
        self.addLink(self.__getLinkSerialNumber(), 'Blue', points)
    
    def addLink(self, name: str, color: str, points: Optional[Sequence[int]] = None):
        """Push a new link command to stack."""
        if points is None:
            points: List[int] = []
        link_args = [name, color, ','.join(f'Point{i}' for i in points)]
        self.CommandStack.beginMacro(f"Add {{Link: {name}}}")
        self.CommandStack.push(AddTable(self.EntitiesLink))
        self.CommandStack.push(EditLinkTable(
            self.EntitiesLink.rowCount() - 1,
            self.EntitiesLink,
            self.EntitiesPoint,
            link_args
        ))
        self.CommandStack.endMacro()
    
    def newPoint(self):
        """Create a point with arguments."""
        self.__editPoint()

    @pyqtSlot(name='on_action_Edit_Point_triggered')
    def editPoint(self):
        """Edit a point with arguments."""
        row = self.EntitiesPoint.currentRow()
        self.__editPoint(row if (row > -1) else 0)
    
    def lockPoints(self):
        """Turn a group of points to fixed on ground or not."""
        to_fixed = self.action_point_context_lock.isChecked()
        for row in self.EntitiesPoint.selectedRows():
            new_links = self.EntitiesPoint.item(row, 1).text().split(',')
            if to_fixed:
                if 'ground' not in new_links:
                    new_links.append('ground')
            else:
                if 'ground' in new_links:
                    new_links.remove('ground')
            args = self.EntitiesPoint.rowTexts(row)
            args[0] = ','.join(s for s in new_links if s)
            self.CommandStack.beginMacro(f"Edit {{Point{row}}}")
            self.CommandStack.push(EditPointTable(
                row,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
            self.CommandStack.endMacro()
    
    def clonePoint(self):
        """Clone a point (with orange color)."""
        row = self.EntitiesPoint.currentRow()
        args = self.EntitiesPoint.rowTexts(row)
        args[2] = 'Orange'
        row_count = self.EntitiesPoint.rowCount()
        self.CommandStack.beginMacro(f"Clone {{Point{row}}} as {{Point{row_count}}}")
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            row_count,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()

    @pyqtSlot(tuple)
    def setFreemove(
        self,
        coords: Sequence[Tuple[int, Tuple[float, float, float]]]
    ):
        """Free move function."""
        points_text = ", ".join(f"Point{c[0]}" for c in coords)
        self.CommandStack.beginMacro(f"Moved {{{points_text}}}")
        for row, (x, y, angle) in coords:
            args = self.EntitiesPoint.rowTexts(row)
            args[3] = x
            args[4] = y
            if args[1] != 'R':
                args[1] = f"{args[1].split(':')[0]}:{angle:.02f}"
            self.CommandStack.push(EditPointTable(
                row,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
        self.CommandStack.endMacro()

    @pyqtSlot(int)
    def adjustLink(self, value: int):
        """Preview the free move result."""
        vpoints = self.EntitiesPoint.dataTuple()
        mapping = {n: f'P{n}' for n in range(len(vpoints))}
        mapping[self.link_freemode_linkname.text()] = float(value)
        try:
            result = expr_solving(
                self.getTriangle(),
                mapping,
                vpoints,
                tuple(v[-1] for v in self.InputsWidget.inputPair())
            )
        except RuntimeError:
            pass
        else:
            self.MainCanvas.adjustLink(result)
            if not self.link_freemode_slider.isSliderDown():
                self.MainCanvas.emit_freemove_all()

    @pyqtSlot(bool)
    def setLinkFreemove(self, enable: bool):
        """Free move function for link length."""
        self.link_freemode_widget.setEnabled(enable)
        self.link_freemode_linkname.clear()
        if not enable:
            return
        item = self.EntitiesExpr.currentItem()
        if not item:
            return
        name, value = item.text().split(':')
        self.link_freemode_linkname.setText(name)
        try:
            self.link_freemode_slider.valueChanged.disconnect(self.adjustLink)
        except TypeError:
            pass
        self.link_freemode_slider.setValue(float(value))
        self.link_freemode_slider.valueChanged.connect(self.adjustLink)

    @pyqtSlot(name='on_action_New_Link_triggered')
    def newLink(self):
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
        rows = self.EntitiesPoint.selectedRows()
        if not len(rows) > 1:
            self.__editLink()
            return
        links_all = list(chain(*(
            self.EntitiesPoint.getLinks(row) for row in rows
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
        row = self.EntitiesLink.findName(name)
        self.CommandStack.beginMacro(f"Edit {{Link: {name}}}")
        args = self.EntitiesLink.rowTexts(row, has_name=True)
        points = set(self.EntitiesLink.getPoints(row))
        points.update(rows)
        args[2] = ','.join(f'Point{p}' for p in points)
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @pyqtSlot(name='on_action_Edit_Link_triggered')
    def editLink(self):
        """Edit a link with arguments."""
        self.__editLink(self.EntitiesLink.currentRow())

    @pyqtSlot()
    def releaseGround(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__getLinkSerialNumber()
        args = [name, 'Blue', self.EntitiesLink.item(0, 2).text()]
        self.CommandStack.beginMacro(f"Release ground to {{Link: {name}}}")
        # Free all points.
        self.CommandStack.push(EditLinkTable(
            0,
            self.EntitiesLink,
            self.EntitiesPoint,
            ['ground', 'White', '']
        ))
        # Create new link.
        self.CommandStack.push(AddTable(self.EntitiesLink))
        self.CommandStack.push(EditLinkTable(
            self.EntitiesLink.rowCount() - 1,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @pyqtSlot()
    def constrainLink(self, row1: Optional[int] = None, row2: int = 0):
        """Turn a link to ground, then delete this link."""
        if row1 is None:
            row1 = self.EntitiesLink.currentRow()
        name = self.EntitiesLink.item(row1, 0).text()
        link_args = self.EntitiesLink.rowTexts(row1, has_name=True)
        link_args[2] = ''
        new_points = sorted(
            set(self.EntitiesLink.item(0, 2).text().split(',')) |
            set(self.EntitiesLink.item(row1, 2).text().split(','))
        )
        base_args = self.EntitiesLink.rowTexts(row2, has_name=True)
        base_args[2] = ','.join(e for e in new_points if e)
        self.CommandStack.beginMacro(f"Constrain {{Link: {name}}} to ground")
        # Turn to ground.
        self.CommandStack.push(EditLinkTable(
            row2,
            self.EntitiesLink,
            self.EntitiesPoint,
            base_args
        ))
        # Free all points and delete the link.
        self.CommandStack.push(EditLinkTable(
            row1,
            self.EntitiesLink,
            self.EntitiesPoint,
            link_args
        ))
        self.CommandStack.push(DeleteTable(
            row1,
            self.EntitiesLink,
            is_rename=False
        ))
        self.CommandStack.endMacro()
    
    def deletePoints(self):
        """Delete the selected points.
        Be sure that the points will has new position after deleted.
        """
        selections = self.EntitiesPoint.selectedRows()
        for i, p in enumerate(selections):
            if p > selections[i - 1]:
                row = p - i
            else:
                row = p
            self.deletePoint(row)
    
    def deleteLinks(self):
        """Delete the selected links.
        Be sure that the links will has new position after deleted.
        """
        selections = self.EntitiesLink.selectedRows()
        selections = tuple(
            p - i + int(0 in selections) if p > selections[i - 1] else p
            for i, p in enumerate(selections)
        )
        for row in selections:
            self.deleteLink(row)
    
    def setCoordsAsCurrent(self):
        """Update points position as current coordinate."""
        vpoints = self.EntitiesPoint.dataTuple()
        self.setFreemove(tuple(
            (row, (vpoint.cx, vpoint.cy, vpoint.angle))
            for row, vpoint in enumerate(vpoints)
        ))
