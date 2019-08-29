# -*- coding: utf-8 -*-

"""The custom widgets of main window.

+ Sub widgets.
+ Context menus.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Dict,
    Callable,
    Union,
    Optional,
    Any,
)
from abc import abstractmethod
from enum import Flag, auto, unique
from dataclasses import dataclass, field
from pyslvs import (
    __version__,
    VPoint,
    VLink,
    Graph,
    color_rgb,
)
from core.QtModules import (
    Slot,
    Qt,
    QMainWindow,
    QAction,
    QMenu,
    QIcon,
    QPixmap,
    QPoint,
    QLabel,
    QPushButton,
    QKeySequence,
    QStandardPaths,
    QFileInfo,
    QSettings,
    QUndoStack,
    QUndoView,
    QABCMeta,
)
from core.info import ARGUMENTS, logger, kernel_list
from core.io import YamlEditor, DatabaseWidget
from core.synthesis import (
    StructureSynthesis,
    Collections,
    DimensionalSynthesis,
)
from .Ui_main import Ui_MainWindow
from .main_canvas import DynamicCanvas
from .tables import (
    BaseTableWidget,
    PointTableWidget,
    LinkTableWidget,
    ExprTableWidget,
    SelectionLabel,
    FPSLabel,
)
from .inputs import InputsWidget

_Coord = Tuple[float, float]


def _set_actions(actions: Sequence[QAction], state: bool):
    """Set actions method."""
    for action in actions:
        action.setVisible(state)


@unique
class _Enable(Flag):

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

    T_P = auto()
    T_L = auto()
    C_P = auto()
    C_L = auto()


@dataclass(eq=False)
class Context:

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

    def point_enable(self, count: int):
        """Point operations settings."""
        for actions, state in (
            (self.p_no, count == 0),
            (self.p_one, count == 1),
            (self.p_any, count > 0),
            (self.p_mul, count > 1),
        ):
            _set_actions(actions, state)

    def link_enable(self, count: int, current_row: int):
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

    def __getitem__(self, key: _Enable) -> Tuple[Union[List[QAction], QMenu], ...]:
        meta = []
        for enable in _Enable:  # type: _Enable
            if enable in key:
                meta.append(self.__getattribute__(enable.name.lower()))
        return tuple(meta)

    def __setitem__(self, key: _Enable, value: Union[List[QAction], QMenu]):
        self.__setattr__(key.name.lower(), value)


class MainWindowBase(QMainWindow, Ui_MainWindow, metaclass=QABCMeta):

    """External UI settings."""

    @abstractmethod
    def __init__(self):
        super(MainWindowBase, self).__init__()
        self.setupUi(self)

        # Environment path
        self.env = ""
        # Entities list
        self.vpoint_list: List[VPoint] = []
        self.vlink_list = [VLink('ground', 'White', (), color_rgb)]

        # Condition list of context menus
        self.context = Context()

        # Initialize custom UI
        self.__undo_redo()
        self.__appearance()
        self.__free_move()
        self.__options()
        self.__zoom()
        self.__context_menu()

        # Open file from command line
        if ARGUMENTS.c:
            self.set_locate(QFileInfo(ARGUMENTS.c).canonicalFilePath())
        else:
            desktop = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
            self.set_locate(self.settings.value("ENV", desktop, type=str))

    def show(self):
        """Overridden function to zoom the canvas's size after startup."""
        super(MainWindowBase, self).show()
        self.main_canvas.zoom_to_fit()

    def set_locate(self, locate: str):
        """Set environment variables."""
        if locate == self.env:
            # If no changed.
            return

        self.env = locate
        logger.debug(f"~Set workplace to: [\"{self.env}\"]")

    def __undo_redo(self):
        """Undo list settings.

        + Undo stack.
        + Undo view widget.
        + Hot keys.
        """
        self.command_stack = QUndoStack(self)
        self.command_stack.setUndoLimit(self.undo_limit_option.value())
        self.undo_limit_option.valueChanged.connect(self.command_stack.setUndoLimit)
        self.command_stack.indexChanged.connect(self.command_reload)
        self.undo_view = QUndoView(self.command_stack)
        self.undo_view.setEmptyLabel("~ Start Pyslvs")
        self.undo_redo_layout.addWidget(self.undo_view)
        self.action_redo = self.command_stack.createRedoAction(self, "Redo")
        self.action_undo = self.command_stack.createUndoAction(self, "Undo")
        self.action_redo.setShortcuts([
            QKeySequence("Ctrl+Shift+Z"),
            QKeySequence("Ctrl+Y"),
        ])
        self.action_redo.setStatusTip("Backtracking undo action.")
        self.action_redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_undo.setStatusTip("Recover last action.")
        self.action_undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
        self.menu_edit.addAction(self.action_undo)
        self.menu_edit.addAction(self.action_redo)

    def __appearance(self):
        """Start up and initialize custom widgets."""
        # Version label
        self.version_label.setText(__version__)

        # Entities tables
        self.entities_tab.tabBar().setStatusTip(
            "Switch the tabs to change to another view mode."
        )

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

        # Select all button on the Point and Link tab as corner widget.
        select_all_button = QPushButton()
        select_all_button.setIcon(QIcon(QPixmap(":/icons/select_all.png")))
        select_all_button.setToolTip("Select all")
        select_all_button.setStatusTip("Select all item of point table.")

        @Slot()
        def table_select_all():
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.entities_point,
                self.entities_link,
                self.entities_expr,
            ]
            tables[self.entities_tab.currentIndex()].selectAll()

        select_all_button.clicked.connect(table_select_all)
        self.entities_tab.setCornerWidget(select_all_button)
        select_all_action = QAction("Select all point", self)
        select_all_action.triggered.connect(table_select_all)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(select_all_action)

        # QPainter canvas window
        self.main_canvas = DynamicCanvas(self)
        select_tips = QLabel(self, Qt.ToolTip)
        self.entities_tab.currentChanged.connect(self.main_canvas.set_selection_mode)

        @Slot(QPoint, str)
        def show_select_tips(pos: QPoint, text: str):
            select_tips.setText(text)
            select_tips.move(pos - QPoint(0, select_tips.height()))
            select_tips.show()

        self.main_canvas.selected_tips.connect(show_select_tips)
        self.main_canvas.selected_tips_hide.connect(select_tips.hide)

        @Slot(tuple, bool)
        def table_set_selection(selections: Sequence[int], key_detect: bool):
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.entities_point,
                self.entities_link,
                self.entities_expr,
            ]
            tables[self.entities_tab.currentIndex()].set_selections(selections, key_detect)

        self.main_canvas.selected.connect(table_set_selection)
        self.entities_point.row_selection_changed.connect(self.main_canvas.set_selection)

        @Slot()
        def table_clear_selection():
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.entities_point,
                self.entities_link,
                self.entities_expr,
            ]
            tables[self.entities_tab.currentIndex()].clearSelection()

        self.main_canvas.noselected.connect(table_clear_selection)

        clean_selection_action = QAction("Clean selection", self)
        clean_selection_action.triggered.connect(table_clear_selection)
        clean_selection_action.setShortcut("Esc")
        clean_selection_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(clean_selection_action)

        self.main_canvas.free_moved.connect(self.set_free_move)
        self.main_canvas.alt_add.connect(self.add_point_by_pos)
        self.main_canvas.doubleclick_edit.connect(self.edit_point)
        self.main_canvas.zoom_changed.connect(self.zoom_bar.setValue)
        self.main_canvas.tracking.connect(self.set_mouse_pos)
        self.canvas_splitter.insertWidget(0, self.main_canvas)
        self.canvas_splitter.setSizes([600, 10, 30])

        # Selection label on status bar right side
        selection_label = SelectionLabel(self)
        self.entities_point.selectionLabelUpdate.connect(
            selection_label.update_select_point
        )
        self.main_canvas.browse_tracking.connect(
            selection_label.update_mouse_position
        )
        self.status_bar.addPermanentWidget(selection_label)

        # FPS label on status bar right side
        fps_label = FPSLabel(self)
        self.main_canvas.fps_updated.connect(fps_label.update_text)
        self.status_bar.addPermanentWidget(fps_label)

        # Inputs widget
        self.inputs_widget = InputsWidget(self)
        self.inputs_tab_layout.addWidget(self.inputs_widget)
        self.free_move_button.toggled.connect(self.inputs_widget.variable_value_reset)
        self.inputs_widget.about_to_resolve.connect(self.resolve)

        @Slot(tuple, bool)
        def inputs_set_selection(selections: Sequence[int], _=None):
            """Distinguish table by tab index."""
            self.inputs_widget.clear_selection()
            if self.entities_tab.currentIndex() == 0:
                self.inputs_widget.set_selection(selections)

        self.main_canvas.selected.connect(inputs_set_selection)
        self.main_canvas.noselected.connect(self.inputs_widget.clear_selection)
        self.inputs_widget.update_preview_button.clicked.connect(self.main_canvas.update_preview_path)

        # Number and type synthesis
        self.structure_synthesis = StructureSynthesis(self)
        self.synthesis_tab_widget.addTab(
            self.structure_synthesis,
            self.structure_synthesis.windowIcon(),
            "Structural"
        )

        # Synthesis collections
        self.collection_tab_page = Collections(self)
        self.synthesis_tab_widget.addTab(
            self.collection_tab_page,
            self.collection_tab_page.windowIcon(),
            "Collections"
        )
        self.structure_synthesis.addCollection = (
            self.collection_tab_page.structure_widget.add_collection
        )

        # Dimensional synthesis
        self.dimensional_synthesis = DimensionalSynthesis(self)
        self.main_canvas.set_target_point.connect(self.dimensional_synthesis.set_point)
        self.synthesis_tab_widget.addTab(
            self.dimensional_synthesis,
            self.dimensional_synthesis.windowIcon(),
            "Dimensional"
        )

        @Slot()
        def set_design_progress():
            """Synthesis progress bar."""
            pos = self.synthesis_tab_widget.currentIndex()
            if pos == 1:
                pos += self.collection_tab_page.tab_widget.currentIndex()
            elif pos == 2:
                pos += 1
            self.synthesis_progress.setValue(pos)

        self.synthesis_tab_widget.currentChanged.connect(set_design_progress)
        self.collection_tab_page.tab_widget.currentChanged.connect(set_design_progress)

        # Same options of structure previews
        as_node1 = self.collection_tab_page.structure_widget.graph_link_as_node
        as_node2 = self.structure_synthesis.graph_link_as_node
        as_node1.toggled.connect(as_node2.setChecked)
        as_node2.toggled.connect(as_node1.setChecked)
        show_label1 = self.collection_tab_page.structure_widget.graph_show_label
        show_label2 = self.structure_synthesis.graph_show_label
        show_label1.toggled.connect(show_label2.setChecked)
        show_label2.toggled.connect(show_label1.setChecked)

        # File widget settings
        self.database_widget = DatabaseWidget(self)
        self.vc_layout.addWidget(self.database_widget)
        self.database_widget.commit_add.clicked.connect(self.commit)
        self.database_widget.branch_add.clicked.connect(self.commit_branch)
        self.action_stash.triggered.connect(self.database_widget.stash)

        # YAML editor
        self.yaml_editor = YamlEditor(self)

        # Console dock will hide when startup
        self.console_widget.hide()
        # Connect to GUI button
        self.console_disconnect_button.setEnabled(not ARGUMENTS.debug_mode)
        self.console_connect_button.setEnabled(ARGUMENTS.debug_mode)

        # Splitter stretch factor
        self.main_splitter.setStretchFactor(0, 4)
        self.main_splitter.setStretchFactor(1, 15)
        self.mechanism_panel_splitter.setSizes([500, 200])

        # Enable mechanism menu actions when shows.
        self.menu_mechanism.aboutToShow.connect(self.enable_mechanism_actions)

        @Slot()
        def new_main_window():
            """Start a new window."""
            run = self.__class__()
            run.show()

        self.action_new_window.triggered.connect(new_main_window)

    def __free_move(self):
        """Menu of free move mode."""
        free_move_mode_menu = QMenu(self)

        def free_move_mode_func(j: int, icon_qt: QIcon):
            @Slot()
            def func() -> None:
                self.free_move_button.setIcon(icon_qt)
                self.main_canvas.set_free_move(j)
                self.entities_tab.setCurrentIndex(0)
                self.inputs_widget.variable_stop.click()
            return func

        for i, (text, icon, tip) in enumerate([
            ("View mode", "free_move_off", "Disable free move mode."),
            ("Translate mode", "translate", "Edit by 2 DOF moving."),
            ("Rotate mode", "rotate", "Edit by 1 DOF moving."),
            ("Reflect mode", "reflect", "Edit by flip axis."),
        ]):
            action = QAction(QIcon(QPixmap(f":/icons/{icon}.png")), text, self)
            action.triggered.connect(free_move_mode_func(i, action.icon()))
            action.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))
            action.setShortcutContext(Qt.WindowShortcut)
            action.setStatusTip(tip)
            free_move_mode_menu.addAction(action)
            if i == 0:
                self.free_move_disable = action
        self.free_move_button.setMenu(free_move_mode_menu)

    def __options(self):
        """Signal connection for option widgets.

        + Spin boxes
        + Combo boxes
        + Check boxes
        """
        # While value change, update the canvas widget.
        self.settings = QSettings(
            QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + '/.pyslvs.ini',
            QSettings.IniFormat,
            self
        )
        self.zoom_bar.valueChanged.connect(self.main_canvas.set_zoom)
        self.line_width_option.valueChanged.connect(self.main_canvas.set_link_width)
        self.path_width_option.valueChanged.connect(self.main_canvas.set_path_width)
        self.font_size_option.valueChanged.connect(self.main_canvas.set_font_size)
        self.action_show_point_mark.toggled.connect(self.main_canvas.set_point_mark)
        self.action_show_dimensions.toggled.connect(self.main_canvas.set_show_dimension)
        self.selection_radius_option.valueChanged.connect(self.main_canvas.set_selection_radius)
        self.link_trans_option.valueChanged.connect(self.main_canvas.set_transparency)
        self.margin_factor_option.valueChanged.connect(self.main_canvas.set_margin_factor)
        self.joint_size_option.valueChanged.connect(self.main_canvas.set_joint_size)
        self.zoom_by_option.currentIndexChanged.connect(self.main_canvas.set_zoom_by)
        self.snap_option.valueChanged.connect(self.main_canvas.set_snap)
        self.background_option.textChanged.connect(self.main_canvas.set_background)
        self.background_opacity_option.valueChanged.connect(self.main_canvas.set_background_opacity)
        self.background_scale_option.valueChanged.connect(self.main_canvas.set_background_scale)
        self.background_offset_x_option.valueChanged.connect(self.main_canvas.set_background_offset_x)
        self.background_offset_y_option.valueChanged.connect(self.main_canvas.set_background_offset_y)
        self.monochrome_option.toggled.connect(self.main_canvas.set_monochrome_mode)
        self.monochrome_option.toggled.connect(
            self.collection_tab_page.configure_widget.configure_canvas.set_monochrome_mode
        )
        self.monochrome_option.toggled.connect(self.dimensional_synthesis.preview_canvas.set_monochrome_mode)

        # Resolve after change current kernel.
        self.planar_solver_option.addItems(kernel_list)
        self.path_preview_option.addItems(kernel_list + ("Same as solver kernel",))
        self.planar_solver_option.currentIndexChanged.connect(self.solve)
        self.path_preview_option.currentIndexChanged.connect(self.solve)
        self.settings_reset.clicked.connect(self.reset_options)

    def __zoom(self):
        """Zoom functions.

        + 'zoom to fit' function connections.
        + Zoom text buttons
        """
        self.action_zoom_to_fit.triggered.connect(self.main_canvas.zoom_to_fit)
        self.ResetCanvas.clicked.connect(self.main_canvas.zoom_to_fit)

        def zoom_level(value: int):
            """Return a function that set the specified zoom value."""
            @Slot()
            def func():
                self.zoom_bar.setValue(value)
            return func

        zoom_menu = QMenu(self)
        for level in range(
            self.zoom_bar.minimum() - self.zoom_bar.minimum() % 100 + 100,
            500 + 1,
            100
        ):
            action = QAction(f'{level}%', self)
            action.triggered.connect(zoom_level(level))
            zoom_menu.addAction(action)
        action = QAction("customize", self)
        action.triggered.connect(self.customize_zoom)
        zoom_menu.addAction(action)
        self.zoom_button.setMenu(zoom_menu)

    def __action(
        self,
        name: Union[str, QAction],
        slot: Optional[Callable[..., None]] = None,
        enable: Optional[_Enable] = None,
        *,
        is_menu: bool = False
    ) -> Union[QAction, QMenu]:
        """New action or menu."""
        if type(name) is QAction:
            menu = None
            action: QAction = name
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
                if type(target) is QMenu:
                    if is_menu:
                        target.addMenu(menu)
                    else:
                        target.addAction(action)
                elif type(target) is list:
                    target.append(action)
                else:
                    raise ValueError("not a list or menu")
        if is_menu:
            return menu
        else:
            return action

    def __context_menu(self):
        """Context menu settings."""
        self.entities_point_widget.customContextMenuRequested.connect(self.point_context_menu)
        self.pop_point = QMenu(self)
        self.entities_link_widget.customContextMenuRequested.connect(self.link_context_menu)
        self.pop_link = QMenu(self)
        self.main_canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.main_canvas.customContextMenuRequested.connect(self.canvas_context_menu)
        self.pop_canvas_p = QMenu(self)
        self.pop_canvas_l = QMenu(self)
        for enable, menu in (
            (_Enable.T_P, self.pop_point),
            (_Enable.T_L, self.pop_link),
            (_Enable.C_P, self.pop_canvas_p),
            (_Enable.C_L, self.pop_canvas_l),
        ):
            menu.setSeparatorsCollapsible(True)
            self.context[enable] = menu
        # EntitiesPoint
        two_menus_p = _Enable.T_P | _Enable.C_P
        two_menus_l = _Enable.T_L | _Enable.C_L
        self.__action("&Add", self.new_point, _Enable.T_P | _Enable.P_NO)
        self.__action("&Add", self.add_normal_point, _Enable.C_P | _Enable.P_NO)
        self.__action("Add to [ground]", self.add_fixed_point, _Enable.C_P | _Enable.P_NO)
        self.action_c_add_target: QAction = self.__action(
            "Add &Target Point",
            self.add_target_point,
            _Enable.C_P | _Enable.C_L | _Enable.P_NO | _Enable.L_NO
        )
        self.__action(self.action_new_link, enable=two_menus_p | two_menus_l | _Enable.P_MUL | _Enable.L_NO)
        self.__action("&Edit", self.edit_point, two_menus_p | _Enable.P_ONE)
        self.action_p_lock: QAction = self.__action("&Grounded", self.lock_points, two_menus_p | _Enable.P_ANY)
        self.action_p_lock.setCheckable(True)
        self.pop_point_m = self.__action("Multiple joint", enable=two_menus_p | _Enable.P_MUL, is_menu=True)
        self.__action("&Copy Table Data", self.copy_points_table, _Enable.T_P | _Enable.P_ONE)
        self.__action("Copy Coordinate", self.copy_coord, _Enable.T_P | _Enable.P_ONE)
        self.__action("C&lone", self.clone_point, two_menus_p | _Enable.P_ONE)
        self.pop_point.addSeparator()
        self.pop_canvas_p.addSeparator()
        self.__action("&Delete", self.delete_selected_points, two_menus_p | _Enable.P_ANY)
        # EntitiesLink
        self.__action("&Edit", self.edit_link, two_menus_l | _Enable.L_ONE)
        self.pop_link_m = self.__action("Merge Links", enable=two_menus_l | _Enable.L_MUL, is_menu=True)
        self.__action("&Copy Table Data", self.copy_links_table, _Enable.T_L | _Enable.L_ONE)
        self.__action("&Release", self.release_ground, two_menus_l | _Enable.L_ONE | _Enable.L_GND)
        self.__action("C&onstrain", self.constrain_link, two_menus_l | _Enable.L_ONE | _Enable.L_N_GND)
        self.pop_link.addSeparator()
        self.pop_canvas_l.addSeparator()
        self.__action("Remove &Empty Names", self.delete_empty_links, _Enable.T_L)
        self.__action("&Delete", self.delete_selected_links, two_menus_l | _Enable.L_ANY)

    @Slot(int, name='on_entities_tab_currentChanged')
    def __set_selection_mode(self, index: int):
        """Connect selection signal for main canvas."""
        # Set selection from click table items.
        tables: List[BaseTableWidget] = [
            self.entities_point,
            self.entities_link,
            self.entities_expr,
        ]
        try:
            for table in tables:
                table.row_selection_changed.disconnect()
        except TypeError:
            pass

        tables[index].row_selection_changed.connect(self.main_canvas.set_selection)
        # Double click signal.
        try:
            self.main_canvas.doubleclick_edit.disconnect()
        except TypeError:
            pass
        if index == 0:
            self.main_canvas.doubleclick_edit.connect(self.edit_point)
        elif index == 1:
            self.main_canvas.doubleclick_edit.connect(self.edit_link)
        # Clear all selections.
        for table in tables:
            table.clearSelection()
        self.inputs_widget.clear_selection()

    @abstractmethod
    def command_reload(self, index: int) -> None:
        ...

    @abstractmethod
    def new_point(self) -> None:
        ...

    @abstractmethod
    def add_normal_point(self) -> None:
        ...

    @abstractmethod
    def add_fixed_point(self) -> None:
        ...

    @abstractmethod
    def edit_point(self) -> None:
        ...

    @abstractmethod
    def delete_selected_points(self) -> None:
        ...

    @abstractmethod
    def lock_points(self) -> None:
        ...

    @abstractmethod
    def new_link(self) -> None:
        ...

    @abstractmethod
    def edit_link(self) -> None:
        ...

    @abstractmethod
    def delete_selected_links(self) -> None:
        ...

    @abstractmethod
    def delete_empty_links(self) -> None:
        ...

    @abstractmethod
    def constrain_link(self) -> None:
        ...

    @abstractmethod
    def release_ground(self) -> None:
        ...

    @abstractmethod
    def add_target_point(self) -> None:
        ...

    @abstractmethod
    def set_free_move(self, args: Sequence[Tuple[int, Tuple[float, float, float]]]) -> None:
        ...

    @abstractmethod
    def add_point_by_pos(self, x: float, y: float) -> None:
        ...

    @abstractmethod
    def set_mouse_pos(self, x: float, y: float) -> None:
        ...

    @abstractmethod
    def solve(self) -> None:
        ...

    @abstractmethod
    def resolve(self) -> None:
        ...

    @abstractmethod
    def commit(self, is_branch: bool = False) -> None:
        ...

    @abstractmethod
    def commit_branch(self) -> None:
        ...

    @abstractmethod
    def enable_mechanism_actions(self) -> None:
        ...

    @abstractmethod
    def clone_point(self) -> None:
        ...

    @abstractmethod
    def copy_coord(self) -> None:
        ...

    @abstractmethod
    def copy_points_table(self) -> None:
        ...

    @abstractmethod
    def copy_links_table(self) -> None:
        ...

    @abstractmethod
    def canvas_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def point_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def link_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def customize_zoom(self) -> None:
        ...

    @abstractmethod
    def reset_options(self) -> None:
        ...

    @abstractmethod
    def preview_path(
        self,
        auto_preview: List[List[_Coord]],
        slider_auto_preview: Dict[int, List[_Coord]],
        vpoints: Sequence[VPoint]
    ) -> None:
        ...

    @abstractmethod
    def reload_canvas(self) -> None:
        ...

    @abstractmethod
    def output_to(self, format_name: str, format_choose: Sequence[str]) -> str:
        ...

    @abstractmethod
    def right_input(self) -> bool:
        ...

    @abstractmethod
    def set_coords_as_current(self) -> None:
        ...

    @abstractmethod
    def dof(self) -> int:
        ...

    @abstractmethod
    def save_reply_box(self, title: str, file_name: str) -> None:
        ...

    @abstractmethod
    def input_from(
        self,
        format_name: str,
        format_choose: Sequence[str],
        multiple: bool = False
    ) -> str:
        ...

    @abstractmethod
    def get_graph(self) -> Tuple[
        Graph,
        List[int],
        List[Tuple[int, int]],
        Dict[int, _Coord],
        Dict[int, int],
        Dict[int, int]
    ]:
        ...

    @abstractmethod
    def get_configure(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def workbook_no_save(self) -> None:
        ...

    @abstractmethod
    def workbook_saved(self) -> bool:
        ...

    @abstractmethod
    def merge_result(
        self,
        expr: str,
        path: Sequence[Sequence[_Coord]]
    ) -> None:
        ...

    @abstractmethod
    def check_file_changed(self) -> bool:
        ...

    @abstractmethod
    def get_storage(self) -> Dict[str, str]:
        ...

    @abstractmethod
    def add_empty_links(self, link_color: Dict[str, str]) -> None:
        ...

    @abstractmethod
    def parse_expression(self, expr: str) -> None:
        ...

    @abstractmethod
    def add_multiple_storage(self, exprs: Sequence[Tuple[str, str]]) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @abstractmethod
    def add_points(
        self,
        p_attr: Sequence[Tuple[float, float, str, str, int, float]]
    ) -> None:
        ...
