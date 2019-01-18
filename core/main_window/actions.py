# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Callable
from abc import ABC
from core.QtModules import (
    Slot,
    QAction,
    QApplication,
    QPoint,
)
from core.widgets import (
    AddTable,
    EditPointTable,
    EditLinkTable,
)
from .storage import StorageMethodInterface


def _copy_table_data(table):
    """Copy item text to clipboard."""
    text = table.currentItem().text()
    if text:
        QApplication.clipboard().setText(text)


class ActionMethodInterface(StorageMethodInterface, ABC):

    """Abstract class for action methods."""

    def __init__(self):
        super(ActionMethodInterface, self).__init__()
        self.mouse_pos_x = 0.
        self.mouse_pos_y = 0.

    def __enable_point_context(self):
        """Adjust the status of QActions.

        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selection = self.EntitiesPoint.selected_rows()
        count = len(selection)
        # If connecting with the ground.
        if count:
            self.action_point_context_lock.setChecked(all(
                'ground' in self.EntitiesPoint.item(row, 1).text()
                for row in self.EntitiesPoint.selected_rows()
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
        self.action_new_link.setVisible(count > 1)
        self.pop_menu_point_merge.menuAction().setVisible(count > 1)

        def mj_func(order: int):
            """Generate a merge function."""
            @Slot()
            def func():
                self.__to_multiple_joint(order, selection)
            return func

        for i, p in enumerate(selection):
            action = QAction(f"Base on Point{p}", self)
            action.triggered.connect(mj_func(i))
            self.pop_menu_point_merge.addAction(action)

    def __enable_link_context(self):
        """Enable / disable link's QAction, same as point table."""
        selection = self.EntitiesLink.selected_rows()
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
        self.pop_menu_link_merge.menuAction().setVisible(count > 1)

        def ml_func(order: int) -> Callable[[], None]:
            """Generate a merge function."""
            @Slot(int)
            def func():
                self.__merge_link(order, selection)
            return func

        for i, row in enumerate(selection):
            name = self.EntitiesLink.item(row, 0).text()
            action = QAction(f"Base on \"{name}\"", self)
            action.triggered.connect(ml_func(i))
            self.pop_menu_link_merge.addAction(action)

    def __to_multiple_joint(self, index: int, points: Tuple[int]):
        """Merge points into a multiple joint.

        @index: The index of main joint in the sequence.
        """
        row = points[index]
        points_text = ", ".join(f'Point{p}' for p in points)
        self.CommandStack.beginMacro(
            f"Merge {{{points_text}}} as multiple joint {{Point{row}}}"
        )
        vpoints = self.EntitiesPoint.data_tuple()
        links = list(vpoints[row].links)
        args = self.EntitiesPoint.row_text(row)
        for point in sorted(points, reverse=True):
            for link in vpoints[point].links:
                if link not in links:
                    links.append(link)
            self.delete_point(point)
        args[0] = ','.join(links)
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            self.EntitiesPoint.rowCount() - 1,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()

    def __merge_link(self, index: int, links: Tuple[int]):
        """Merge links to a base link.

        @index: The index of main joint in the sequence.
        """
        row = links[index]
        links_text = ", ".join(self.EntitiesLink.item(link, 0).text() for link in links)
        name = self.EntitiesLink.item(row, 0).text()
        self.CommandStack.beginMacro(f"Merge {{{links_text}}} to joint {{{name}}}")
        vlinks = self.EntitiesLink.data_tuple()
        points = list(vlinks[row].points)
        args = self.EntitiesLink.row_text(row, has_name=True)
        for link in sorted(links, reverse=True):
            if vlinks[link].name == vlinks[row].name:
                continue
            for point in vlinks[link].points:
                if point not in points:
                    points.append(point)
            self.delete_link(link)
        args[2] = ','.join(f'Point{p}' for p in points)
        self.CommandStack.push(EditLinkTable(
            [vlink.name for vlink in self.EntitiesLink.data()].index(args[0]),
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @Slot(float, float)
    def set_mouse_pos(self, x: float, y: float):
        """Mouse position on canvas."""
        self.mouse_pos_x = x
        self.mouse_pos_y = y

    @Slot(QPoint)
    def point_context_menu(self, point: QPoint):
        """EntitiesPoint context menu."""
        self.__enable_point_context()
        self.pop_menu_point.exec_(self.EntitiesPoint_widget.mapToGlobal(point))
        self.action_new_link.setVisible(True)
        self.pop_menu_point_merge.clear()

    @Slot(QPoint)
    def link_context_menu(self, point: QPoint):
        """EntitiesLink context menu."""
        self.__enable_link_context()
        self.pop_menu_link.exec_(self.EntitiesLink_widget.mapToGlobal(point))
        self.pop_menu_link_merge.clear()

    @Slot(QPoint)
    def canvas_context_menu(self, point: QPoint):
        """MainCanvas context menu."""
        index = self.EntitiesTab.currentIndex()
        if index == 0:
            self.__enable_point_context()
            self.action_canvas_context_path.setVisible(self.SynthesisTab.currentIndex() == 2)
            self.pop_menu_canvas_p.exec_(self.MainCanvas.mapToGlobal(point))
            self.action_new_link.setVisible(True)
            self.pop_menu_point_merge.clear()
        elif index == 1:
            self.__enable_link_context()
            self.pop_menu_canvas_l.exec_(self.MainCanvas.mapToGlobal(point))
            self.pop_menu_link_merge.clear()

    @Slot()
    def enable_mechanism_actions(self):
        """Enable / disable 'mechanism' menu."""
        point_selection = self.EntitiesPoint.selected_rows()
        link_selection = self.EntitiesLink.selected_rows()
        one_point = len(point_selection) == 1
        one_link = len(link_selection) == 1
        point_selected = bool(point_selection)
        link_selected = (
            bool(link_selection) and
            (0 not in link_selection) and
            (not one_link)
        )
        # Edit
        self.action_edit_point.setEnabled(one_point)
        self.action_edit_link.setEnabled(one_link)
        # Delete
        self.action_delete_point.setEnabled(point_selected)
        self.action_delete_link.setEnabled(link_selected)

    @Slot()
    def copy_points_table(self):
        """Copy text from point table."""
        _copy_table_data(self.EntitiesPoint)

    @Slot()
    def copy_links_table(self):
        """Copy text from link table."""
        _copy_table_data(self.EntitiesLink)

    def copy_coord(self):
        """Copy the current coordinate of the point."""
        pos = self.EntitiesPoint.current_position(self.EntitiesPoint.currentRow())
        text = str(pos[0] if (len(pos) == 1) else pos)
        QApplication.clipboard().setText(text)
