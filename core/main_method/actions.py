# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple
from core.QtModules import (
    QAction,
    QApplication,
    QPoint,
)
from core.io import (
    AddTable,
    EditPointTable,
    EditLinkTable,
)
from .entities import _deletePoint, _deleteLink


def _enablePointContext(self):
    """Adjust the status of QActions.
    
    What ever we have least one point or not,
    need to enable / disable QAction.
    """
    selection = self.EntitiesPoint.selectedRows()
    selectionCount = len(selection)
    row = self.EntitiesPoint.currentRow()
    #If connecting with the ground.
    if selectionCount:
        self.action_point_context_lock.setChecked(all(
            'ground' in self.EntitiesPoint.item(row, 1).text()
            for row in self.EntitiesPoint.selectedRows()
        ))
    #If no any points selected.
    for action in (
        self.action_point_context_add,
        self.action_canvas_context_add,
        self.action_canvas_context_fix_add,
    ):
        action.setVisible(selectionCount <= 0)
    self.action_point_context_lock.setVisible(row > -1)
    self.action_point_context_delete.setVisible(row > -1)
    #If a point selected.
    for action in (
        self.action_point_context_edit,
        self.action_point_context_copyPoint,
        self.action_point_context_copydata,
        self.action_point_context_copyCoord,
    ):
        action.setVisible(row > -1)
        action.setEnabled(selectionCount == 1)
    #If two or more points selected.
    self.action_New_Link.setVisible(selectionCount > 1)
    self.popMenu_point_merge.menuAction().setVisible(selectionCount > 1)
    
    def mjFunc(i: int):
        """Generate a merge function."""
        return lambda: _toMultipleJoint(self, i, selection)
    
    for i, p in enumerate(selection):
        action = QAction("Base on Point{}".format(p), self)
        action.triggered.connect(mjFunc(i))
        self.popMenu_point_merge.addAction(action)


def _enableLinkContext(self):
    """Enable / disable link's QAction, same as point table."""
    selection = self.EntitiesLink.selectedRows()
    selectionCount = len(selection)
    row = self.EntitiesLink.currentRow()
    self.action_link_context_add.setVisible(selectionCount <= 0)
    selected_one = selectionCount == 1
    not_ground = row > 0
    any_link = row > -1
    self.action_link_context_edit.setEnabled(any_link and selected_one)
    self.action_link_context_delete.setEnabled(not_ground and selected_one)
    self.action_link_context_copydata.setEnabled(any_link and selected_one)
    self.action_link_context_release.setVisible((row == 0) and selected_one)
    self.action_link_context_constrain.setVisible(not_ground and selected_one)
    self.popMenu_link_merge.menuAction().setVisible(selectionCount > 1)
    
    def mlFunc(i: int):
        """Generate a merge function."""
        return lambda: _mergeLinkage(self, i, selection)
    
    for i, row in enumerate(selection):
        action = QAction("Base on \"{}\"".format(self.EntitiesLink.item(row, 0).text()), self)
        action.triggered.connect(mlFunc(i))
        self.popMenu_link_merge.addAction(action)


def _copyTableData(self, table):
    """Copy item text to clipboard."""
    text = table.currentItem().text()
    if text:
        QApplication.clipboard().setText(text)


def _toMultipleJoint(self, index: int, points: Tuple[int]):
    """Merge points into a multiple joint.
    
    @index: The index of main joint in the sequence.
    """
    row = points[index]
    self.CommandStack.beginMacro(
        "Merge {{{}}} as multiple joint {{{}}}".format(
            ", ".join('Point{}'.format(point) for point in points),
            'Point{}'.format(row)
        )
    )
    vpoints = self.EntitiesPoint.dataTuple()
    links = list(vpoints[row].links)
    args = self.EntitiesPoint.rowTexts(row)
    for point in sorted(points, reverse=True):
        for link in vpoints[point].links:
            if link not in links:
                links.append(link)
        _deletePoint(self, point)
    args[0] = ','.join(links)
    self.CommandStack.push(AddTable(self.EntitiesPoint))
    self.CommandStack.push(EditPointTable(
        self.EntitiesPoint.rowCount() - 1,
        self.EntitiesPoint,
        self.EntitiesLink,
        args
    ))
    self.CommandStack.endMacro()


def _mergeLinkage(self, index: int, links: Tuple[int]):
    """Merge links to a base linkage.
    
    @index: The index of main joint in the sequence.
    """
    row = links[index]
    self.CommandStack.beginMacro(
        "Merge {{{}}} to joint {{{}}}".format(
            ", ".join(self.EntitiesLink.item(link, 0).text() for link in links),
            self.EntitiesLink.item(row, 0).text()
        )
    )
    vlinks = self.EntitiesLink.dataTuple()
    points = list(vlinks[row].points)
    args = self.EntitiesLink.rowTexts(row, hasName=True)
    for link in sorted(links, reverse=True):
        for point in vlinks[link].points:
            if point not in points:
                points.append(point)
        _deleteLink(self, link)
    args[2] = ','.join('Point{}'.format(p) for p in points)
    self.CommandStack.push(AddTable(self.EntitiesLink))
    self.CommandStack.push(EditLinkTable(
        self.EntitiesLink.rowCount() - 1,
        self.EntitiesLink,
        self.EntitiesPoint,
        args
    ))
    self.CommandStack.endMacro()


def setMousePos(self, x: float, y: float):
    """Mouse position on canvas."""
    self.mouse_pos_x = x
    self.mouse_pos_y = y


def on_point_context_menu(self, point: QPoint):
    """EntitiesPoint context menu."""
    _enablePointContext(self)
    self.popMenu_point.exec_(self.Entities_Point_Widget.mapToGlobal(point))
    self.action_New_Link.setVisible(True)
    self.popMenu_point_merge.clear()


def on_link_context_menu(self, point: QPoint):
    """EntitiesLink context menu."""
    _enableLinkContext(self)
    self.popMenu_link.exec_(self.Entities_Link_Widget.mapToGlobal(point))
    self.popMenu_link_merge.clear()


def on_canvas_context_menu(self, point: QPoint):
    """MainCanvas context menu."""
    _enablePointContext(self)
    tabText = self.SynthesisTab.tabText(self.SynthesisTab.currentIndex())
    self.action_canvas_context_path.setVisible(tabText == "Dimensional")
    self.popMenu_canvas.exec_(self.MainCanvas.mapToGlobal(point))
    self.action_New_Link.setVisible(True)
    self.popMenu_point_merge.clear()


def enableMechanismActions(self):
    """Enable / disable 'mechanism' menu."""
    pointSelection = self.EntitiesPoint.selectedRows()
    linkSelection = self.EntitiesLink.selectedRows()
    ONE_POINT = len(pointSelection) == 1
    ONE_LINK = len(linkSelection) == 1
    POINT_SELECTED = bool(pointSelection)
    LINK_SELECTED = (
        bool(linkSelection) and
        (0 not in linkSelection) and
        (not ONE_LINK)
    )
    #Edit
    self.action_Edit_Point.setEnabled(ONE_POINT)
    self.action_Edit_Link.setEnabled(ONE_LINK)
    #Delete
    self.action_Delete_Point.setEnabled(POINT_SELECTED)
    self.action_Delete_Link.setEnabled(LINK_SELECTED)


def copyPointsTable(self):
    """Copy text from point table."""
    _copyTableData(self, self.EntitiesPoint)


def copyLinksTable(self):
    """Copy text from link table."""
    _copyTableData(self, self.EntitiesLink)


def copyCoord(self):
    """Copy the current coordinate of the point."""
    pos = self.EntitiesPoint.currentPosition(self.EntitiesPoint.currentRow())
    text = str(pos[0] if (len(pos) == 1) else pos)
    QApplication.clipboard().setText(text)
