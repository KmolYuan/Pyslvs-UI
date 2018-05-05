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
from core.io import EditPointTable
from .entities_method import _deletePoint


def _enablePointContext(self):
    """Adjust the status of QActions.
    
    What ever we have least one point or not,
    need to enable / disable QAction.
    """
    selectedRows = self.EntitiesPoint.selectedRows()
    selectionCount = len(selectedRows)
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
    
    def mjFunc(i):
        """Generate a merge function."""
        return lambda: _toMultipleJoint(self, i, selectedRows)
    
    for i, p in enumerate(selectedRows):
        action = QAction("Base on Point{}".format(p), self)
        action.triggered.connect(mjFunc(i))
        self.popMenu_point_merge.addAction(action)


def _enableLinkContext(self):
    """Enable / disable link's QAction, same as point table."""
    selectionCount = len(self.EntitiesLink.selectedRows())
    row = self.EntitiesLink.currentRow()
    self.action_link_context_add.setVisible(selectionCount <= 0)
    selected_one = selectionCount == 1
    self.action_link_context_edit.setEnabled((row > -1) and selected_one)
    self.action_link_context_delete.setEnabled((row > 0) and selected_one)
    self.action_link_context_copydata.setEnabled((row > -1) and selected_one)
    self.action_link_context_release.setVisible((row == 0) and selected_one)
    self.action_link_context_constrain.setVisible((row > 0) and selected_one)


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
            ", ".join('Point{}'.format(p) for p in points),
            'Point{}'.format(row)
        )
    )
    points_data = self.EntitiesPoint.dataTuple()
    for i, p in enumerate(points):
        if i == index:
            continue
        newLinks = points_data[row].links
        for l in points_data[p].links:
            #Add new links.
            if l not in newLinks:
                newLinks.append(l)
        args = self.EntitiesPoint.rowTexts(row)
        args[0] = ','.join(newLinks)
        self.CommandStack.push(EditPointTable(
            row,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        _deletePoint(self, p)
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
