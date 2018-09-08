# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Callable
from core.QtModules import (
    pyqtSlot,
    QAction,
    QApplication,
    QPoint,
    QAbcMeta,
)
from core.io import (
    AddTable,
    EditPointTable,
    EditLinkTable,
)
from .storage import StorageMethodInterface


def _copyTableData(table):
    """Copy item text to clipboard."""
    text = table.currentItem().text()
    if text:
        QApplication.clipboard().setText(text)


class ActionMethodInterface(StorageMethodInterface, metaclass=QAbcMeta):
    
    """Interface class for action methods."""
    
    def __init__(self):
        super(ActionMethodInterface, self).__init__()
        self.mouse_pos_x = 0.
        self.mouse_pos_y = 0.
    
    def __enablePointContext(self):
        """Adjust the status of QActions.
        
        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selection = self.EntitiesPoint.selectedRows()
        count = len(selection)
        # If connecting with the ground.
        if count:
            self.action_point_context_lock.setChecked(all(
                'ground' in self.EntitiesPoint.item(row, 1).text()
                for row in self.EntitiesPoint.selectedRows()
            ))
        # If no any points selected.
        for action in (
            self.action_point_context_add,
            self.action_canvas_context_add,
            self.action_canvas_context_grounded_add,
        ):
            action.setVisible(count == 0)
        self.action_point_context_lock.setVisible(count > 0)
        self.action_point_context_delete.setVisible(count > 0)
        # If a point selected.
        for action in (
            self.action_point_context_edit,
            self.action_point_context_copyPoint,
            self.action_point_context_copydata,
            self.action_point_context_copyCoord,
        ):
            action.setVisible(count == 1)
        # If two or more points selected.
        self.action_New_Link.setVisible(count > 1)
        self.popMenu_point_merge.menuAction().setVisible(count > 1)
        
        def mjFunc(order: int):
            """Generate a merge function."""
            @pyqtSlot()
            def func():
                self.__toMultipleJoint(order, selection)
            return func
        
        for i, p in enumerate(selection):
            action = QAction(f"Base on Point{p}", self)
            action.triggered.connect(mjFunc(i))
            self.popMenu_point_merge.addAction(action)
    
    def __enableLinkContext(self):
        """Enable / disable link's QAction, same as point table."""
        selection = self.EntitiesLink.selectedRows()
        count = len(selection)
        row = self.EntitiesLink.currentRow()
        self.action_link_context_add.setVisible(count == 0)
        selected_one = count == 1
        not_ground = row > 0
        any_link = row > -1
        self.action_link_context_edit.setVisible(any_link and selected_one)
        self.action_link_context_delete.setVisible(not_ground and (count > 0))
        self.action_link_context_copydata.setVisible(any_link and selected_one)
        self.action_link_context_release.setVisible((row == 0) and selected_one)
        self.action_link_context_constrain.setVisible(not_ground and selected_one)
        self.popMenu_link_merge.menuAction().setVisible(count > 1)
        
        def mlFunc(order: int) -> Callable[[], None]:
            """Generate a merge function."""
            @pyqtSlot(int)
            def func():
                self.__mergeLink(order, selection)
            return func
        
        for i, row in enumerate(selection):
            name = self.EntitiesLink.item(row, 0).text()
            action = QAction(f"Base on \"{name}\"", self)
            action.triggered.connect(mlFunc(i))
            self.popMenu_link_merge.addAction(action)
    
    def __toMultipleJoint(self, index: int, points: Tuple[int]):
        """Merge points into a multiple joint.
        
        @index: The index of main joint in the sequence.
        """
        row = points[index]
        points_text = ", ".join(f'Point{p}' for p in points)
        self.CommandStack.beginMacro(
            f"Merge {{{points_text}}} as multiple joint {{Point{row}}}"
        )
        vpoints = self.EntitiesPoint.dataTuple()
        links = list(vpoints[row].links)
        args = self.EntitiesPoint.rowTexts(row)
        for point in sorted(points, reverse=True):
            for link in vpoints[point].links:
                if link not in links:
                    links.append(link)
            self.deletePoint(point)
        args[0] = ','.join(links)
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            self.EntitiesPoint.rowCount() - 1,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()
    
    def __mergeLink(self, index: int, links: Tuple[int]):
        """Merge links to a base link.
        
        @index: The index of main joint in the sequence.
        """
        row = links[index]
        links_text = ", ".join(self.EntitiesLink.item(link, 0).text() for link in links)
        name = self.EntitiesLink.item(row, 0).text()
        self.CommandStack.beginMacro(f"Merge {{{links_text}}} to joint {{{name}}}")
        vlinks = self.EntitiesLink.dataTuple()
        points = list(vlinks[row].points)
        args = self.EntitiesLink.rowTexts(row, has_name=True)
        for link in sorted(links, reverse=True):
            if vlinks[link].name == vlinks[row].name:
                continue
            for point in vlinks[link].points:
                if point not in points:
                    points.append(point)
            self.deleteLink(link)
        args[2] = ','.join(f'Point{p}' for p in points)
        self.CommandStack.push(EditLinkTable(
            [vlink.name for vlink in self.EntitiesLink.data()].index(args[0]),
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @pyqtSlot(float, float)
    def setMousePos(self, x: float, y: float):
        """Mouse position on canvas."""
        self.mouse_pos_x = x
        self.mouse_pos_y = y

    @pyqtSlot(QPoint)
    def point_context_menu(self, point: QPoint):
        """EntitiesPoint context menu."""
        self.__enablePointContext()
        self.popMenu_point.exec_(self.EntitiesPoint_widget.mapToGlobal(point))
        self.action_New_Link.setVisible(True)
        self.popMenu_point_merge.clear()

    @pyqtSlot(QPoint)
    def link_context_menu(self, point: QPoint):
        """EntitiesLink context menu."""
        self.__enableLinkContext()
        self.popMenu_link.exec_(self.EntitiesLink_widget.mapToGlobal(point))
        self.popMenu_link_merge.clear()

    @pyqtSlot(QPoint)
    def canvas_context_menu(self, point: QPoint):
        """MainCanvas context menu."""
        index = self.EntitiesTab.currentIndex()
        if index == 0:
            self.__enablePointContext()
            self.action_canvas_context_path.setVisible(self.SynthesisTab.currentIndex() == 2)
            self.popMenu_canvas_p.exec_(self.MainCanvas.mapToGlobal(point))
            self.action_New_Link.setVisible(True)
            self.popMenu_point_merge.clear()
        elif index == 1:
            self.__enableLinkContext()
            self.popMenu_canvas_l.exec_(self.MainCanvas.mapToGlobal(point))
            self.popMenu_link_merge.clear()

    @pyqtSlot()
    def enableMechanismActions(self):
        """Enable / disable 'mechanism' menu."""
        point_selection = self.EntitiesPoint.selectedRows()
        link_selection = self.EntitiesLink.selectedRows()
        one_point = len(point_selection) == 1
        one_link = len(link_selection) == 1
        point_selected = bool(point_selection)
        link_selected = (
            bool(link_selection) and
            (0 not in link_selection) and
            (not one_link)
        )
        # Edit
        self.action_Edit_Point.setEnabled(one_point)
        self.action_Edit_Link.setEnabled(one_link)
        # Delete
        self.action_Delete_Point.setEnabled(point_selected)
        self.action_Delete_Link.setEnabled(link_selected)

    @pyqtSlot()
    def copyPointsTable(self):
        """Copy text from point table."""
        _copyTableData(self.EntitiesPoint)

    @pyqtSlot()
    def copyLinksTable(self):
        """Copy text from link table."""
        _copyTableData(self.EntitiesLink)
    
    def copyCoord(self):
        """Copy the current coordinate of the point."""
        pos = self.EntitiesPoint.currentPosition(self.EntitiesPoint.currentRow())
        text = str(pos[0] if (len(pos) == 1) else pos)
        QApplication.clipboard().setText(text)
