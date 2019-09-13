# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Callable, Union
from abc import ABC, abstractmethod
from pyslvs_ui.core.QtModules import (
    Slot,
    QAction,
    QApplication,
    QPoint,
    QTableWidget,
)
from pyslvs_ui.core.widgets import AddTable, EditPointTable, EditLinkTable
from pyslvs_ui.core.io import PreferencesDialog
from .storage import StorageMethodInterface


def _copy_table_data(table: QTableWidget) -> None:
    """Copy item text to clipboard."""
    text = table.currentItem().text()
    if text:
        QApplication.clipboard().setText(text)


class ActionMethodInterface(StorageMethodInterface, ABC):

    """Abstract class for action methods."""

    @abstractmethod
    def __init__(self) -> None:
        super(ActionMethodInterface, self).__init__()
        self.mouse_pos_x = 0.
        self.mouse_pos_y = 0.

    def __enable_point_context(self) -> None:
        """Adjust the status of QActions.

        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selection = self.entities_point.selected_rows()
        # Set grounded state
        if selection:
            self.action_p_lock.setChecked(all(
                'ground' in self.vpoint_list[row].links for row in selection
            ))
        self.context.point_enable(len(selection))

        def mj_func(order: int) -> Callable[[], None]:
            """Generate a merge function."""
            @Slot()
            def func() -> None:
                self.__to_multiple_joint(order, selection)
            return func

        for i, p in enumerate(selection):
            action = QAction(f"Base on Point{p}", self)
            action.triggered.connect(mj_func(i))
            self.pop_point_m.addAction(action)

    def __enable_link_context(self) -> None:
        """Enable / disable link's QAction, same as point table."""
        selection = self.entities_link.selected_rows()
        row = self.entities_link.currentRow()
        self.context.link_enable(len(selection), row)

        def ml_func(order: int) -> Callable[[], None]:
            """Generate a merge function."""
            @Slot(int)
            def func() -> None:
                self.__merge_link(order, selection)
            return func

        for i, row in enumerate(selection):
            action = QAction(f"Base on \"{self.vlink_list[row].name}\"", self)
            action.triggered.connect(ml_func(i))
            self.pop_link_m.addAction(action)

    def __to_multiple_joint(self, index: int, points: Sequence[int]) -> None:
        """Merge points into a multiple joint.

        @index: The index of main joint in the sequence.
        """
        row = points[index]
        self.command_stack.beginMacro(
            f"Merge {sorted(points)} as multiple joint {{Point{row}}}"
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

    def __merge_link(self, index: int, links: Sequence[int]) -> None:
        """Merge links to a base link.

        @index: The index of main joint in the sequence.
        """
        row = links[index]
        links_text = ", ".join(self.vlink_list[link].name for link in links)
        name = self.vlink_list[row].name
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
    def set_mouse_pos(self, x: float, y: float) -> None:
        """Mouse position on canvas."""
        self.mouse_pos_x = x
        self.mouse_pos_y = y

    @Slot(QPoint)
    def point_context_menu(self, point: QPoint) -> None:
        """EntitiesPoint context menu."""
        self.__enable_point_context()
        self.pop_point.exec_(self.entities_point_widget.mapToGlobal(point))
        self.action_new_link.setVisible(True)
        self.pop_point_m.clear()

    @Slot(QPoint)
    def link_context_menu(self, point: QPoint) -> None:
        """EntitiesLink context menu."""
        self.__enable_link_context()
        self.pop_link.exec_(self.entities_link_widget.mapToGlobal(point))
        self.pop_link_m.clear()

    @Slot(QPoint)
    def canvas_context_menu(self, point: QPoint) -> None:
        """MainCanvas context menu."""
        index = self.entities_tab.currentIndex()
        if index == 0:
            self.__enable_point_context()
            self.action_c_add_target.setVisible(
                self.synthesis_tab_widget.currentIndex() == 2
                and self.main_panel.currentIndex() == 2
                and self.dimensional_synthesis.has_target()
            )
            self.pop_canvas_p.exec_(self.main_canvas.mapToGlobal(point))
            self.action_new_link.setVisible(True)
            self.pop_point_m.clear()
        elif index == 1:
            self.__enable_link_context()
            self.pop_canvas_l.exec_(self.main_canvas.mapToGlobal(point))
            self.pop_link_m.clear()

    @Slot()
    def enable_mechanism_actions(self) -> None:
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
    def copy_points_table(self) -> None:
        """Copy text from point table."""
        _copy_table_data(self.entities_point)

    @Slot()
    def copy_links_table(self) -> None:
        """Copy text from link table."""
        _copy_table_data(self.entities_link)

    def copy_coord(self) -> None:
        """Copy the current coordinate of the point."""
        pos = self.entities_point.current_position(self.entities_point.currentRow())
        text = str(pos[0] if len(pos) == 1 else pos)
        QApplication.clipboard().setText(text)

    @Slot(name='on_action_preference_triggered')
    def __set_preference(self) -> None:
        """Set preference by dialog."""
        dlg = PreferencesDialog(self)
        dlg.show()
        dlg.exec_()
        # Update values
        for name in dlg.diff():
            value: Union[bool, int, float, str] = getattr(self.prefer, name)
            if name == 'line_width_option':
                self.main_canvas.set_link_width(value)
            elif name == 'path_width_option':
                self.main_canvas.set_path_width(value)
            elif name == 'font_size_option':
                self.main_canvas.set_font_size(value)
            elif name == 'selection_radius_option':
                self.main_canvas.set_selection_radius(value)
            elif name == 'link_trans_option':
                self.main_canvas.set_transparency(value)
            elif name == 'margin_factor_option':
                self.main_canvas.set_margin_factor(value)
            elif name == 'joint_size_option':
                self.main_canvas.set_joint_size(value)
            elif name == 'zoom_by_option':
                self.main_canvas.set_zoom_by(value)
            elif name == 'snap_option':
                self.main_canvas.set_snap(value)
            elif name == 'background_option':
                self.main_canvas.set_background(value)
            elif name == 'background_opacity_option':
                self.main_canvas.set_background_opacity(value)
            elif name == 'background_scale_option':
                self.main_canvas.set_background_scale(value)
            elif name == 'background_offset_x_option':
                self.main_canvas.set_background_offset_x(value)
            elif name == 'background_offset_y_option':
                self.main_canvas.set_background_offset_y(value)
            elif name == 'title_full_path_option':
                self.set_window_title_full_path()
            for canvas in (
                self.main_canvas,
                self.collection_tab_page.configure_widget.configure_canvas,
                self.dimensional_synthesis.preview_canvas,
            ):
                if name == 'tick_mark_option':
                    canvas.set_show_ticks(value)
                elif name == 'monochrome_option':
                    canvas.set_monochrome_mode(value)
        dlg.deleteLater()
        self.solve()