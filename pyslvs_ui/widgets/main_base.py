# -*- coding: utf-8 -*-

"""The custom widgets of main window.

+ Sub widgets.
+ Context menus.
"""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    cast, TypeVar, Tuple, List, Sequence, Iterator, Callable,
    Union, Optional, Type,
)
from abc import abstractmethod, ABC
from enum import Flag, auto, unique
from dataclasses import dataclass, field, fields, Field, astuple
from qtpy.QtCore import Slot, Qt, QPoint, QDir, QSettings
from qtpy.QtWidgets import (
    QAction,
    QWidget,
    QMenu,
    QLabel,
    QPushButton,
    QUndoStack,
)
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VPoint, VLink, color_rgb
from pyslvs_ui.info import ARGUMENTS, logger, Kernel
from pyslvs_ui.io import ProjectWidget, ProjectFormat
from pyslvs_ui.synthesis import StructureSynthesis, Collections, Optimizer
from .main_abc import MainWindowABC
from .canvas import MainCanvas
from .tables import (
    BaseTableWidget,
    PointTableWidget,
    LinkTableWidget,
    ExprTableWidget,
    SelectionLabel,
    FPSLabel,
)
from .inputs import InputsWidget

_N = TypeVar('_N')
_Action = Union[List[QAction], QMenu]


def _set_actions(actions: Sequence[QAction], state: bool) -> None:
    """Set actions method."""
    for action in actions:
        action.setVisible(state)


@unique
class _Enable(Flag):
    # Conditions
    # No / One / Any / Multiple / Ground / Not ground
    P_NO = auto()
    P_ONE = auto()
    P_ANY = auto()
    P_MUL = auto()
    L_NO = auto()
    L_ONE = auto()
    L_ANY = auto()
    L_MUL = auto()
    L_GND = auto()
    L_N_GND = auto()
    # Menus
    # Table / Context menu
    P_T = auto()
    L_T = auto()
    P_C = auto()
    L_C = auto()
    # Optimizer page
    OPT = auto()


@dataclass(repr=False, eq=False)
class _Context:
    """Context menu actions."""
    p_no: List[QAction] = field(default_factory=list)
    p_one: List[QAction] = field(default_factory=list)
    p_any: List[QAction] = field(default_factory=list)
    p_mul: List[QAction] = field(default_factory=list)
    l_no: List[QAction] = field(default_factory=list)
    l_one: List[QAction] = field(default_factory=list)
    l_any: List[QAction] = field(default_factory=list)
    l_mul: List[QAction] = field(default_factory=list)
    l_gnd: List[QAction] = field(default_factory=list)
    l_n_gnd: List[QAction] = field(default_factory=list)
    opt: List[QAction] = field(default_factory=list)

    def point_enable(self, count: int) -> None:
        """Point operations settings."""
        for actions, state in (
            (self.p_no, count == 0),
            (self.p_one, count == 1),
            (self.p_any, count > 0),
            (self.p_mul, count > 1),
        ):
            _set_actions(actions, state)

    def link_enable(self, count: int, current_row: int) -> None:
        """Link operations settings."""
        for actions, state in (
            (self.l_no, count == 0),
            (self.l_one, count == 1),
            (self.l_any, count > 0),
            (self.l_mul, count > 1),
        ):
            _set_actions(actions, state)
        for actions, state in (
            (self.l_gnd, current_row == 0),
            (self.l_n_gnd, current_row != 0),
        ):
            for action in actions:
                action.setVisible(action.isVisible() and state)

    def __getitem__(self, key: _Enable) -> Tuple[_Action, ...]:
        meta = []
        for enable in _Enable:  # type: _Enable
            if enable in key:
                meta.append(getattr(self, enable.name.lower()))
        return tuple(meta)

    def __setitem__(self, key: _Enable, value: _Action) -> None:
        self.__setattr__(key.name.lower(), value)


@dataclass(repr=False)
class Preferences:
    """The settings of Pyslvs."""
    line_width_option: int = 3
    font_size_option: int = 14
    path_width_option: int = 3
    scale_factor_option: int = 10
    selection_radius_option: int = 10
    link_trans_option: int = 0
    margin_factor_option: int = 5
    joint_size_option: int = 10
    zoom_by_option: int = 0
    snap_option: float = 1
    tick_mark_option: int = 1
    nav_toolbar_pos_option: int = 1
    default_zoom_option: int = 500
    grab_no_background_option: bool = True
    monochrome_option: bool = False
    undo_limit_option: int = 60
    open_project_actions_option: int = 1
    file_type_option: ProjectFormat = ProjectFormat.YAML
    planar_solver_option: int = 0
    path_preview_option: int = Kernel.SAME_AS_SOLVING
    auto_remove_link_option: bool = True
    title_full_path_option: bool = False
    console_error_option: bool = ARGUMENTS.debug_mode
    # "Do not save the settings" by default
    not_save_option: bool = True

    def diff(self, other: Optional[Preferences]) -> Iterator[str]:
        """Show the fields of differences.
        Pass None to iterate over all names.
        """
        for field_obj in fields(self):  # type: Field
            name: str = field_obj.name
            if other is None or getattr(self, name) != getattr(other, name):
                yield name

    def reset(self) -> None:
        """Reset the user values."""
        for field_obj in fields(self):  # type: Field
            setattr(self, field_obj.name, field_obj.default)

    def copy(self):
        """Make a copy of preference data."""
        return Preferences(*astuple(self))


class MainWindowBase(MainWindowABC, ABC):
    """External UI settings."""
    vpoint_list: List[VPoint]
    vlink_list: List[VLink]

    __tables: Sequence[BaseTableWidget]

    @abstractmethod
    def __init__(self):
        super(MainWindowBase, self).__init__()
        # Environment path
        self.env = ""
        # Alignment mode
        self.alignment_mode = 0
        # Entities list
        self.vpoint_list = []
        self.vlink_list = [VLink(VLink.FRAME, 'White', (), color_rgb)]
        # Condition list of context menus
        self.context = _Context()
        # Preference
        self.prefer = Preferences()
        # Set path from command line
        home_dir = QDir.home()
        self.settings = QSettings(
            home_dir.absoluteFilePath(".pyslvs.ini"),
            QSettings.IniFormat,
            self
        )
        if ARGUMENTS.c:
            self.set_locate(QDir(ARGUMENTS.c).absolutePath())
        else:
            home_dir.cd("Desktop")
            env = self.settings.value("ENV", home_dir.absolutePath())
            self.set_locate(str(env))

        # Initialize custom UI
        self.__undo_redo()
        self.__appearance()
        self.__alignment()
        self.__free_move()
        self.__options()
        self.__context_menu()

    def env_path(self) -> str:
        """Return environment path."""
        return self.env

    def set_locate(self, locate: str) -> None:
        """Set environment variables."""
        if locate == self.env or not QDir(locate).exists():
            return
        self.env = locate
        logger.debug(f"~Set workplace to: \"{self.env}\"")

    def __undo_redo(self) -> None:
        """Undo list settings.

        + Undo stack.
        + Undo view widget.
        + Hot keys.
        """
        self.cmd_stack = QUndoStack(self)
        self.cmd_stack.setUndoLimit(self.prefer.undo_limit_option)
        self.cmd_stack.indexChanged.connect(self.command_reload)
        redo = self.cmd_stack.createRedoAction(self, "Redo")
        undo = self.cmd_stack.createUndoAction(self, "Undo")
        redo.setShortcuts(["Ctrl+Shift+Z", "Ctrl+Y"])
        redo.setStatusTip("Backtracking undo action.")
        redo.setIcon(QIcon(QPixmap("icons:redo.png")))
        undo.setShortcut("Ctrl+Z")
        undo.setStatusTip("Recover last action.")
        undo.setIcon(QIcon(QPixmap("icons:undo.png")))
        self.menu_edit.insertActions(self.action_new_point, [undo, redo])
        self.menu_edit.insertSeparator(self.action_new_point)

    def __appearance(self) -> None:
        """Start up and initialize custom widgets."""
        # Entities tables
        tab_bar = self.entities_tab.tabBar()
        tab_bar.setStatusTip("Switch the tabs to change to another view mode.")
        self.entities_point = PointTableWidget(self.entities_point_widget)
        self.entities_point.cellDoubleClicked.connect(self.edit_point)
        self.entities_point.delete_request.connect(self.delete_selected_points)
        self.entities_point_layout.addWidget(self.entities_point)
        self.entities_link = LinkTableWidget(self.entities_link_widget)
        self.entities_link.cellDoubleClicked.connect(self.edit_link)
        self.entities_link.delete_request.connect(self.delete_selected_links)
        self.entities_link_layout.addWidget(self.entities_link)
        self.entities_expr = ExprTableWidget(self.EntitiesExpr_widget)
        self.entities_expr_layout.insertWidget(0, self.entities_expr)
        self.__tables = (
            self.entities_point,
            self.entities_link,
            self.entities_expr,
        )

        # Select all button on the Point and Link tab as corner widget
        select_all_btn = QPushButton()
        select_all_btn.setIcon(QIcon(QPixmap("icons:select_all.png")))
        select_all_btn.setToolTip("Select all")
        select_all_btn.setStatusTip("Select all item of point table.")

        @Slot()
        def table_select_all() -> None:
            """Distinguish table by tab index."""
            self.__tables[self.entities_tab.currentIndex()].selectAll()

        select_all_btn.clicked.connect(table_select_all)
        self.entities_tab.setCornerWidget(select_all_btn)
        select_all_action = QAction("Select all point", self)
        select_all_action.triggered.connect(table_select_all)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(select_all_action)

        # QPainter canvas window
        self.main_canvas = MainCanvas(self)
        self.entities_tab.currentChanged.connect(
            self.main_canvas.set_selection_mode)
        select_tips = QLabel(self, Qt.ToolTip)

        @Slot(QPoint, str)
        def show_select_tips(pos: QPoint, text: str) -> None:
            select_tips.setText(text)
            select_tips.move(pos - QPoint(0, select_tips.height()))
            select_tips.show()

        self.main_canvas.selected_tips.connect(show_select_tips)
        self.main_canvas.selected_tips_hide.connect(select_tips.hide)

        @Slot(tuple, bool)
        def table_selection(selection: Sequence[int], check_key: bool) -> None:
            """Distinguish table by tab index."""
            index = self.entities_tab.currentIndex()
            self.__tables[index].set_selections(selection, check_key)

        self.main_canvas.selected.connect(table_selection)
        self.entities_point.row_selection_changed.connect(
            self.main_canvas.set_selection)

        @Slot()
        def table_clear_selection() -> None:
            """Clear the selection of specific table by tab index."""
            index = self.entities_tab.currentIndex()
            self.__tables[index].clearSelection()

        clean_selection_action = QAction("Clean selection", self)
        clean_selection_action.triggered.connect(table_clear_selection)
        clean_selection_action.setShortcut("Esc")
        clean_selection_action.setShortcutContext(Qt.WindowShortcut)
        self.main_canvas.no_selected.connect(table_clear_selection)
        self.addAction(clean_selection_action)

        self.main_canvas.free_moved.connect(self.set_free_move)
        self.main_canvas.alt_add.connect(self.add_point_by_pos)
        self.main_canvas.doubleclick_edit.connect(self.edit_point)
        self.main_canvas.zoom_changed.connect(self.zoom_bar.setValue)
        self.main_canvas.tracking.connect(self.set_mouse_pos)
        self.canvas_layout.insertWidget(0, self.main_canvas)
        self.canvas_splitter.setSizes([600, 10, 30])

        # Selection label on status bar right side
        selection_label = SelectionLabel(self)
        self.entities_point.selectionLabelUpdate.connect(
            selection_label.update_select_point)
        self.main_canvas.browse_tracking.connect(
            selection_label.update_mouse_position)
        self.status_bar.addPermanentWidget(selection_label)

        # FPS label on status bar right side
        fps_label = FPSLabel(self)
        self.main_canvas.fps_updated.connect(fps_label.update_text)
        self.status_bar.addPermanentWidget(fps_label)

        # Inputs widget
        self.inputs_widget = InputsWidget(self)
        self.inputs_tab_layout.addWidget(self.inputs_widget)
        self.free_move_btn.toggled.connect(
            self.inputs_widget.variable_value_reset)
        self.inputs_widget.about_to_resolve.connect(self.resolve)

        @Slot(tuple, bool)
        def inputs_selection(selections: Sequence[int], _=None) -> None:
            """Distinguish table by tab index."""
            self.inputs_widget.clear_selection()
            if self.entities_tab.currentIndex() == 0:
                self.inputs_widget.set_selection(selections)

        self.main_canvas.selected.connect(inputs_selection)
        self.main_canvas.no_selected.connect(self.inputs_widget.clear_selection)
        self.inputs_widget.update_preview_btn.clicked.connect(
            self.main_canvas.update_preview_path)

        # Synthesis collections
        self.collections = Collections(self)
        # Number and type synthesis
        self.structure_synthesis = StructureSynthesis(self)
        # Dimensional synthesis
        self.optimizer = Optimizer(self)
        self.main_canvas.set_target_point.connect(self.optimizer.set_point)
        for widget, name in [
            (self.structure_synthesis, "Structure"),
            (self.collections, "Collections"),
            (self.optimizer, "Optimizer"),
        ]:  # type: QWidget, str
            self.synthesis_tab_widget.addTab(widget, widget.windowIcon(), name)
        # Same options of structure previews
        as_node1 = self.collections.structure_widget.graph_link_as_node
        as_node2 = self.structure_synthesis.graph_link_as_node
        as_node1.toggled.connect(as_node2.setChecked)
        as_node2.toggled.connect(as_node1.setChecked)
        show_label1 = self.collections.structure_widget.graph_show_label
        show_label2 = self.structure_synthesis.graph_show_label
        show_label1.toggled.connect(show_label2.setChecked)
        show_label2.toggled.connect(show_label1.setChecked)
        # File widget settings
        self.project_widget = ProjectWidget(self)
        self.project_layout.addWidget(self.project_widget)
        # Zooming and console dock will hide when startup
        self.zoom_widget.hide()
        self.console_widget.hide()
        # Connect to GUI button
        debug_mode = ARGUMENTS.debug_mode
        self.console_disconnect_btn.setEnabled(not debug_mode)
        self.console_connect_btn.setEnabled(debug_mode)
        # Splitter stretch factor
        self.main_splitter.setStretchFactor(0, 4)
        self.main_splitter.setStretchFactor(1, 15)
        self.mechanism_panel_splitter.setSizes([500, 200])
        # Enable mechanism menu actions when shows
        self.menu_edit.aboutToShow.connect(self.enable_mechanism_actions)
        # New main window function
        self.action_new_window.triggered.connect(self.new)

    def __alignment(self) -> None:
        """Menu of alignment function."""

        def switch_icon(m: int, icon_name: str) -> Callable[[], None]:
            @Slot()
            def func() -> None:
                self.alignment_mode = m
                self.alignment_btn.setIcon(QIcon(QPixmap(icon_name)))

            return func

        menu = QMenu(self)
        for i, (text, icon) in enumerate([
            ("Vertical alignment", "vertical_align"),
            ("Horizontal alignment", "horizontal_align"),
        ]):
            icon = f"icons:{icon}.png"
            action = QAction(QIcon(QPixmap(icon)), text, self)
            action.triggered.connect(switch_icon(i, icon))
            menu.addAction(action)
        self.alignment_btn.setMenu(menu)
        self.alignment_btn.clicked.connect(self.point_alignment)

    def __free_move(self) -> None:
        """Menu of free move mode."""

        def free_move_mode_func(j: int, icon_qt: QIcon) -> Callable[[], None]:
            @Slot()
            def func() -> None:
                self.free_move_btn.setIcon(icon_qt)
                self.main_canvas.set_free_move(j)
                self.entities_tab.setCurrentIndex(0)
                self.inputs_widget.variable_stop.click()

            return func

        menu = QMenu(self)
        for i, (text, icon, tip) in enumerate([
            ("View mode", "free_move_off", "Disable free move mode."),
            ("Translate mode", "translate", "Edit by 2 DOF moving."),
            ("Rotate mode", "rotate", "Edit by 1 DOF moving."),
            ("Reflect mode", "reflect", "Edit by flip axis."),
        ]):
            action = QAction(QIcon(QPixmap(f"icons:{icon}.png")), text, self)
            action.triggered.connect(free_move_mode_func(i, action.icon()))
            action.setShortcut(f"Ctrl+{i + 1}")
            action.setShortcutContext(Qt.WindowShortcut)
            action.setStatusTip(tip)
            menu.addAction(action)
            if i == 0:
                self.free_move_disable = action
        self.free_move_btn.setMenu(menu)

    def __options(self) -> None:
        """Signal connection for option widgets.

        + Spin boxes
        + Combo boxes
        + Check boxes
        """
        # While value change, update the canvas widget
        self.zoom_bar.valueChanged.connect(self.main_canvas.set_zoom)
        self.action_show_point_mark.toggled.connect(
            self.main_canvas.set_point_mark)
        self.action_show_dimensions.toggled.connect(
            self.main_canvas.set_show_dimension)

    def __action(
        self,
        name: Union[str, QAction],
        slot: Optional[Callable[..., None]] = None,
        enable: Optional[_Enable] = None,
        *,
        to: Type[_N]
    ) -> _N:
        """New action or menu."""
        is_menu = to is QMenu
        if isinstance(name, QAction):
            menu: Optional[QMenu] = None
            action = name
        elif is_menu:
            menu = QMenu(name, self)
            action = menu.menuAction()
        else:
            menu = None
            action = QAction(name, self)
        if slot is not None:
            action.triggered.connect(slot)
        if enable is not None:
            for target in self.context[enable]:
                if isinstance(target, QMenu):
                    if is_menu:
                        target.addMenu(menu)
                    else:
                        target.addAction(action)
                elif isinstance(target, list):
                    target.append(action)
                else:
                    raise ValueError("not a list or menu")
        if is_menu:
            return cast(QMenu, menu)
        else:
            return action

    def __context_menu(self) -> None:
        """Context menu settings."""
        self.entities_point_widget.customContextMenuRequested.connect(
            self.point_context_menu)
        self.pop_point = QMenu(self)
        self.entities_link_widget.customContextMenuRequested.connect(
            self.link_context_menu)
        self.pop_link = QMenu(self)
        self.main_canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.main_canvas.customContextMenuRequested.connect(
            self.canvas_context_menu)
        self.pop_canvas_p = QMenu(self)
        self.pop_canvas_l = QMenu(self)
        for enable, menu in (
            (_Enable.P_T, self.pop_point),
            (_Enable.L_T, self.pop_link),
            (_Enable.P_C, self.pop_canvas_p),
            (_Enable.L_C, self.pop_canvas_l),
        ):
            menu.setSeparatorsCollapsible(True)
            self.context[enable] = menu
        # Point table
        two_menus_p = _Enable.P_T | _Enable.P_C
        two_menus_l = _Enable.L_T | _Enable.L_C
        self.__action("&Add", self.new_point, _Enable.P_T | _Enable.P_NO,
                      to=QAction)
        self.__action("&Add", self.add_normal_point, _Enable.P_C | _Enable.P_NO,
                      to=QAction)
        self.__action("Add to [ground]", self.add_fixed_point,
                      _Enable.P_C | _Enable.P_NO, to=QAction)
        self.action_add_target = self.__action(
            "Add &Target Point",
            self.add_target_point,
            _Enable.P_C | _Enable.L_C | _Enable.OPT,
            to=QAction
        )
        self.__action(
            self.action_new_link,
            enable=two_menus_p | two_menus_l | _Enable.P_MUL | _Enable.L_NO,
            to=QAction
        )
        self.__action("&Edit", self.edit_point, two_menus_p | _Enable.P_ONE,
                      to=QAction)
        self.action_p_lock = self.__action("&Grounded", self.lock_points,
                                           two_menus_p | _Enable.P_ANY,
                                           to=QAction)
        self.action_p_lock.setCheckable(True)
        self.pop_point_m = self.__action("Multiple joint",
                                         enable=two_menus_p | _Enable.P_MUL,
                                         to=QMenu)
        self.__action("&Copy Table Data", self.copy_points_table,
                      _Enable.P_T | _Enable.P_ONE, to=QAction)
        self.__action("Copy Coordinate", self.copy_coord,
                      _Enable.P_T | _Enable.P_ONE, to=QAction)
        self.__action("C&lone", self.clone_point, two_menus_p | _Enable.P_ONE,
                      to=QAction)
        self.pop_point.addSeparator()
        self.pop_canvas_p.addSeparator()
        self.__action("&Delete", self.delete_selected_points,
                      two_menus_p | _Enable.P_ANY, to=QAction)
        # EntitiesLink
        self.__action("&Edit", self.edit_link, two_menus_l | _Enable.L_ONE,
                      to=QAction)
        self.pop_link_m = self.__action("Merge Links",
                                        enable=two_menus_l | _Enable.L_MUL,
                                        to=QMenu)
        self.__action("&Copy Table Data", self.copy_links_table,
                      _Enable.L_T | _Enable.L_ONE, to=QAction)
        self.__action("&Release", self.release_ground,
                      two_menus_l | _Enable.L_ONE | _Enable.L_GND, to=QAction)
        self.__action("C&onstrain", self.constrain_link,
                      two_menus_l | _Enable.L_ONE | _Enable.L_N_GND, to=QAction)
        self.pop_link.addSeparator()
        self.pop_canvas_l.addSeparator()
        self.__action(self.action_deduce_links,
                      enable=two_menus_l | _Enable.L_NO, to=QAction)
        self.__action("&Delete", self.delete_selected_links,
                      two_menus_l | _Enable.L_ANY, to=QAction)

    @Slot(int, name='on_entities_tab_currentChanged')
    def __set_selection_mode(self, index: int) -> None:
        """Connect selection signal for main canvas."""
        # Set selection from click table items
        try:
            for table in self.__tables:
                table.row_selection_changed.disconnect()
        except TypeError:
            pass
        self.__tables[index].row_selection_changed.connect(
            self.main_canvas.set_selection)
        # Double click signal
        try:
            self.main_canvas.doubleclick_edit.disconnect()
        except TypeError:
            pass
        if index == 0:
            self.main_canvas.doubleclick_edit.connect(self.edit_point)
        elif index == 1:
            self.main_canvas.doubleclick_edit.connect(self.edit_link)
        # Clear all selections
        for table in self.__tables:
            table.clearSelection()
        self.inputs_widget.clear_selection()
