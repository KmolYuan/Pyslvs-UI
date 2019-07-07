# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Callable
from abc import ABC, abstractmethod
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

    @abstractmethod
    def __init__(self):
        super(ActionMethodInterface, self).__init__()
        self.mouse_pos_x = 0.
        self.mouse_pos_y = 0.

    def __enable_point_context(self):
        """Adjust the status of QActions.

        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selection = self.entities_point.selected_rows()
        count = len(selection)
        # If connecting with the ground.
        if count:
            self.action_point_context_lock.setChecked(all(
                'ground' in self.entities_point.item(row, 1).text()
                for row in self.entities_point.selected_rows()
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
            self.action_point_context_clone,
            self.action_point_context_copydata,
            self.action_point_context_copy_coord,
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
        selection = self.entities_link.selected_rows()
        count = len(selection)
        row = self.entities_link.currentRow()
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
            name = self.entities_link.item(row, 0).text()
            action = QAction(f"Base on \"{name}\"", self)
            action.triggered.connect(ml_func(i))
            self.pop_menu_link_merge.addAction(action)

    def __to_multiple_joint(self, index: int, points: Sequence[int]):
        """Merge points into a multiple joint.

        @index: The index of main joint in the sequence.
        """
        row = points[index]
        points_text = ", ".join(f'Point{p}' for p in points)
        self.command_stack.beginMacro(
            f"Merge {{{points_text}}} as multiple joint {{Point{row}}}"
        )
        links = list(self.vpoint_list[row].links)
        args = self.entities_point.row_data(row)
        for point in sorted(points, reverse=True):
            for link in self.vpoint_list[point].links:
                if link not in links:
                    links.append(link)
            self.delete_point(point)
        args[0] = ','.join(links)
        self.command_stack.push(AddTable(self.vpoint_list, self.entities_point))
        self.command_stack.push(EditPointTable(
            self.entities_point.rowCount() - 1,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    def __merge_link(self, index: int, links: Sequence[int]):
        """Merge links to a base link.

        @index: The index of main joint in the sequence.
        """
        row = links[index]
        links_text = ", ".join(self.entities_link.item(link, 0).text() for link in links)
        name = self.entities_link.item(row, 0).text()
        self.command_stack.beginMacro(f"Merge {{{links_text}}} to joint {{{name}}}")
        points = list(self.vlink_list[row].points)
        args = self.entities_link.row_data(row)
        for link in sorted(links, reverse=True):
            if self.vlink_list[link].name == self.vlink_list[row].name:
                continue
            for point in self.vlink_list[link].points:
                if point not in points:
                    points.append(point)
            self.delete_link(link)
        args[2] = ','.join(f'Point{p}' for p in points)
        row = [vlink.name for vlink in self.vlink_list].index(args[0])
        self.command_stack.push(EditLinkTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    @Slot(float, float)
    def set_mouse_pos(self, x: float, y: float):
        """Mouse position on canvas."""
        self.mouse_pos_x = x
        self.mouse_pos_y = y

    @Slot(QPoint)
    def point_context_menu(self, point: QPoint):
        """EntitiesPoint context menu."""
        self.__enable_point_context()
        self.pop_menu_point.exec(self.entities_point_widget.mapToGlobal(point))
        self.action_new_link.setVisible(True)
        self.pop_menu_point_merge.clear()

    @Slot(QPoint)
    def link_context_menu(self, point: QPoint):
        """EntitiesLink context menu."""
        self.__enable_link_context()
        self.pop_menu_link.exec(self.entities_link_widget.mapToGlobal(point))
        self.pop_menu_link_merge.clear()

    @Slot(QPoint)
    def canvas_context_menu(self, point: QPoint):
        """MainCanvas context menu."""
        index = self.entities_tab.currentIndex()
        if index == 0:
            self.__enable_point_context()
            is_synthesis = self.synthesis_tab_widget.currentIndex() == 2
            self.action_canvas_context_path.setVisible(is_synthesis)
            self.pop_menu_canvas_p.exec(self.main_canvas.mapToGlobal(point))
            self.action_new_link.setVisible(True)
            self.pop_menu_point_merge.clear()
        elif index == 1:
            self.__enable_link_context()
            self.pop_menu_canvas_l.exec(self.main_canvas.mapToGlobal(point))
            self.pop_menu_link_merge.clear()

    @Slot()
    def enable_mechanism_actions(self):
        """Enable / disable 'mechanism' menu."""
        point_selection = self.entities_point.selected_rows()
        link_selection = self.entities_link.selected_rows()
        one_point = len(point_selection) == 1
        one_link = len(link_selection) == 1
        point_selected = bool(point_selection)
        link_selected = bool(link_selection and 0 not in link_selection)
        # Edit
        self.action_edit_point.setEnabled(one_point)
        self.action_edit_link.setEnabled(one_link)
        # Delete
        self.action_delete_point.setEnabled(point_selected)
        self.action_delete_link.setEnabled(link_selected)

    @Slot()
    def copy_points_table(self):
        """Copy text from point table."""
        _copy_table_data(self.entities_point)

    @Slot()
    def copy_links_table(self):
        """Copy text from link table."""
        _copy_table_data(self.entities_link)

    def copy_coord(self):
        """Copy the current coordinate of the point."""
        pos = self.entities_point.current_position(self.entities_point.currentRow())
        text = str(pos[0] if len(pos) == 1 else pos)
        QApplication.clipboard().setText(text)
