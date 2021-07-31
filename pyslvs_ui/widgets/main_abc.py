# -*- coding: utf-8 -*-

"""Predefined methods of main window."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List, Sequence, Dict, Mapping, Optional, Any
from abc import abstractmethod
from qtpy.QtCore import Qt, QPoint
from qtpy.QtWidgets import QMainWindow
from pyslvs import VPoint
from pyslvs.graph import Graph
from pyslvs_ui.qt_patch import QABCMeta
from .main_ui import Ui_MainWindow

_Coord = Tuple[float, float]
_Phase = Tuple[float, float, float]


class MainWindowABC(QMainWindow, Ui_MainWindow, metaclass=QABCMeta):
    """Main window abstract class."""

    @abstractmethod
    def __init__(self):
        super(MainWindowABC, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

    @abstractmethod
    def command_reload(self, index: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def new_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_normal_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_fixed_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def edit_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_selected_points(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def lock_points(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def new_link(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def edit_link(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_selected_links(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def deduce_links(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def constrain_link(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def release_ground(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_target_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_free_move(self, args: Sequence[Tuple[int, _Phase]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_point_by_pos(self, x: float, y: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_mouse_pos(self, x: float, y: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_back_position(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def solve(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def resolve(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def enable_mechanism_actions(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def clone_point(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def copy_coord(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def copy_points_table(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def copy_links_table(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def canvas_context_menu(self, point: QPoint) -> None:
        raise NotImplementedError

    @abstractmethod
    def point_context_menu(self, point: QPoint) -> None:
        raise NotImplementedError

    @abstractmethod
    def link_context_menu(self, point: QPoint) -> None:
        raise NotImplementedError

    @abstractmethod
    def preview_path(
        self,
        auto_preview: List[List[_Coord]],
        slider_auto_preview: Dict[int, List[_Coord]],
        vpoints: Sequence[VPoint]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def reload_canvas(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def output_to(self, format_name: str, format_choose: Sequence[str]) -> str:
        raise NotImplementedError

    @abstractmethod
    def right_input(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_coords_as_current(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def dof(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def save_reply_box(self, title: str, file_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def input_from(
        self,
        format_name: str,
        format_choose: Sequence[str]
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def input_from_multiple(
        self,
        format_name: str,
        format_choose: Sequence[str]
    ) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_graph(self) -> Tuple[
        Graph,
        List[int],
        List[Tuple[int, int]],
        Mapping[int, _Coord],
        Mapping[int, int],
        Mapping[int, int]
    ]:
        raise NotImplementedError

    @abstractmethod
    def get_configure(self) -> Mapping[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def project_no_save(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def project_saved(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def merge_result(self, expr: str, path: Sequence[Sequence[_Coord]]) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_file_changed(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_storage(self) -> Mapping[str, str]:
        raise NotImplementedError

    @abstractmethod
    def add_empty_links(self, link_color: Mapping[str, str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse_expression(self, expr: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_multiple_storage(self, exprs: Mapping[str, str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_points(
        self,
        p_attr: Sequence[Tuple[float, float, str, str, int, float]]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_points_by_graph(
        self,
        graph: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: Optional[int]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_window_title_full_path(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def import_pmks_url(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_picture_clipboard(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_expr(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def py_script(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def export_dxf(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def export_slvs(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_pmks(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def export_image(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def show_overview(self) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def new() -> MainWindowABC:
        raise NotImplementedError

    @abstractmethod
    def point_alignment(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_expression(
        self,
        points: Optional[Sequence[VPoint]] = None,
        indent: int = -1
    ) -> str:
        raise NotImplementedError
