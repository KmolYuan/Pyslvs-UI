# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Sequence, Callable, Union
from abc import ABC
from qtpy.QtCore import Slot, QPoint
from qtpy.QtWidgets import QAction, QApplication, QTableWidget
from pyslvs import VLink
from pyslvs_ui.graphics import BaseCanvas
from pyslvs_ui.widgets import EditPointTable, EditLinkTable, Preferences
from pyslvs_ui.io import PreferencesDialog
from .storage import StorageMethodInterface


def _copy_table_data(table: QTableWidget) -> None:
    """Copy item text to clipboard."""
    text = table.currentItem().text()
    if text:
        QApplication.clipboard().setText(text)


class ActionMethodInterface(StorageMethodInterface, ABC):
    """Abstract class for action methods."""

    def __enable_point_context(self) -> None:
        """Adjust the status of QActions.

        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selection = self.entities_point.selected_rows()
        # Set grounded state
        if selection:
            self.action_p_lock.setChecked(all(
                VLink.FRAME in self.vpoint_list[row].links for row in selection
            ))
        self.context.point_enable(len(selection))

        def mj_func(order: int) -> Callable[[], None]:
            """Generate a merge function."""
            @Slot()
            def func() -> None:
                self.__merge_joint(order, selection)
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

    def __merge_joint(self, index: int, points: Sequence[int]) -> None:
        """Merge the joints into a specific joint."""
        base = points[index]
        self.cmd_stack.beginMacro(
            f"Merge {sorted(points)} based on {{Point{base}}}"
        )
        links = list(self.vpoint_list[base].links)
        args = self.entities_point.row_data(base)
        for p in points:
            if p != base:
                links.extend(set(self.vpoint_list[p].links) - set(links))
        args.links = ','.join(links)
        self.cmd_stack.push(EditPointTable(
            base,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        for p in sorted(points, reverse=True):
            if p != base:
                self.delete_point(p)
        self.cmd_stack.endMacro()

    def __merge_link(self, index: int, links: Sequence[int]) -> None:
        """Merge links to a base link.

        @index: The index of main joint in the sequence.
        """
        row = links[index]
        links_text = ", ".join(self.vlink_list[link].name for link in links)
        name = self.vlink_list[row].name
        self.cmd_stack.beginMacro(f"Merge {{{links_text}}} to joint {{{name}}}")
        points = list(self.vlink_list[row].points)
        args = self.entities_link.row_data(row)
        for link in sorted(links, reverse=True):
            if self.vlink_list[link].name == self.vlink_list[row].name:
                continue
            for point in self.vlink_list[link].points:
                if point not in points:
                    points.append(point)
            self.delete_link(link)
        args.points = ','.join(f'Point{p}' for p in points)
        row = [vlink.name for vlink in self.vlink_list].index(args.name)
        self.cmd_stack.push(EditLinkTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.cmd_stack.endMacro()

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
        for action in self.context.opt:
            action.setVisible(
                self.main_panel.currentWidget() is self.synthesis_tab
                and self.synthesis_tab_widget.currentWidget() is self.optimizer
                and self.optimizer.has_target()
            )
        index = self.entities_tab.currentIndex()
        if index == 0:
            self.__enable_point_context()
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
        self.apply_preferences(dlg.prefer_applied)
        dlg.deleteLater()
        self.solve()

    def apply_preferences(self, prefer: Preferences, *, force: bool = False):
        """Apply preference from a setting."""
        for name in self.prefer.diff(None if force else prefer):
            value: Union[bool, int, float, str] = getattr(prefer, name)
            setattr(self.prefer, name, value)
            if name == 'line_width_option':
                self.main_canvas.set_link_width(cast(int, value))
            elif name == 'path_width_option':
                self.main_canvas.set_path_width(cast(int, value))
            elif name == 'font_size_option':
                self.main_canvas.set_font_size(cast(int, value))
            elif name == 'selection_radius_option':
                self.main_canvas.set_selection_radius(cast(int, value))
            elif name == 'link_trans_option':
                self.main_canvas.set_transparency(cast(int, value))
            elif name == 'margin_factor_option':
                self.main_canvas.set_margin_factor(cast(int, value))
            elif name == 'joint_size_option':
                self.main_canvas.set_joint_size(cast(int, value))
            elif name == 'zoom_by_option':
                self.main_canvas.set_zoom_by(cast(int, value))
            elif name == 'nav_toolbar_pos_option':
                self.__set_nav_toolbar_pos(cast(int, value))
            elif name == 'default_zoom_option':
                self.main_canvas.set_default_zoom(cast(int, value))
            elif name == 'snap_option':
                self.main_canvas.set_snap(cast(float, value))
            elif name == 'title_full_path_option':
                self.set_window_title_full_path()
            for canvas in (
                self.main_canvas,
                self.collections.configure_widget.configure_canvas,
                self.optimizer.preview_canvas,
            ):
                if name == 'tick_mark_option':
                    cast(BaseCanvas, canvas).set_show_ticks(cast(int, value))
                elif name == 'monochrome_option':
                    cast(BaseCanvas, canvas).set_monochrome_mode(cast(bool, value))

    def __set_nav_toolbar_pos(self, pos: int) -> None:
        """Set the position of toolbar. (0: top, 1: bottom)"""
        if pos not in {0, 1}:
            raise ValueError("invalid toolbar position.")
        if pos == 1:
            pos = 2
        if self.canvas_layout.indexOf(self.nav_toolbar) == pos:
            return
        self.canvas_layout.insertWidget(pos, self.nav_toolbar)
        self.canvas_layout.insertWidget(1, self.zoom_widget)

    @Slot(bool, name='on_grid_mode_btn_toggled')
    def __set_grid_mode(self, enabled: bool) -> None:
        """Return grid mode state."""
        self.main_canvas.set_snap(self.prefer.snap_option if enabled else 0.)
