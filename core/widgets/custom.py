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
    Any,
)
from abc import abstractmethod
from core.QtModules import (
    Slot,
    Qt,
    QMainWindow,
    QAction,
    QMenu,
    QIcon,
    QPixmap,
    QPoint,
    QPushButton,
    QKeySequence,
    QStandardPaths,
    QFileInfo,
    QSettings,
    QUndoStack,
    QUndoView,
    QABCMeta,
)
from core.info import __version__, ARGUMENTS
from core.libs import (
    kernel_list,
    VPoint,
    Graph,
)
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
_major, _minor, _build, _label = __version__


class MainWindowBase(QMainWindow, Ui_MainWindow, metaclass=QABCMeta):

    """External UI settings."""

    @abstractmethod
    def __init__(self):
        super(MainWindowBase, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.env = ""

        self.set_locate(
            QFileInfo(ARGUMENTS.c).canonicalFilePath()
            if ARGUMENTS.c else
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )

        # Undo stack stream.
        self.CommandStack = QUndoStack(self)

        # Initialize custom UI.
        self.__undo_redo()
        self.__appearance()
        self.__free_move()
        self.__options()
        self.__zoom()
        self.__point_context_menu()
        self.__link_context_menu()
        self.__canvas_context_menu()

    def show(self):
        """Overridden function to zoom the canvas's size after startup."""
        super(MainWindowBase, self).show()
        self.MainCanvas.zoom_to_fit()

    def set_locate(self, locate: str):
        """Set environment variables."""
        if locate == self.env:
            # If no changed.
            return

        self.env = locate
        print(f"~Set workplace to: [\"{self.env}\"]")

    def __undo_redo(self):
        """Undo list settings.

        + Undo stack.
        + Undo view widget.
        + Hot keys.
        """
        self.CommandStack.setUndoLimit(self.undolimit_option.value())
        self.undolimit_option.valueChanged.connect(self.CommandStack.setUndoLimit)
        self.CommandStack.indexChanged.connect(self.command_reload)
        self.undoView = QUndoView(self.CommandStack)
        self.undoView.setEmptyLabel("~ Start Pyslvs")
        self.UndoRedoLayout.addWidget(self.undoView)
        self.action_Redo = self.CommandStack.createRedoAction(self, "Redo")
        self.action_Undo = self.CommandStack.createUndoAction(self, "Undo")
        self.action_Redo.setShortcuts([
            QKeySequence("Ctrl+Shift+Z"),
            QKeySequence("Ctrl+Y"),
        ])
        self.action_Redo.setStatusTip("Backtracking undo action.")
        self.action_Redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
        self.action_Undo.setShortcut("Ctrl+Z")
        self.action_Undo.setStatusTip("Recover last action.")
        self.action_Undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.action_Redo)

    def __appearance(self):
        """Start up and initialize custom widgets."""
        # Version label
        self.version_label.setText(f"v{_major}.{_minor}.{_build} ({_label})")

        # Entities tables.
        self.EntitiesTab.tabBar().setStatusTip("Switch the tabs to change to another view mode.")

        self.EntitiesPoint = PointTableWidget(self.EntitiesPoint_widget)
        self.EntitiesPoint.cellDoubleClicked.connect(self.edit_point)
        self.EntitiesPoint.delete_request.connect(self.delete_points)
        self.EntitiesPoint_layout.addWidget(self.EntitiesPoint)

        self.EntitiesLink = LinkTableWidget(self.EntitiesLink_widget)
        self.EntitiesLink.cellDoubleClicked.connect(self.edit_link)
        self.EntitiesLink.delete_request.connect(self.delete_links)
        self.EntitiesLink_layout.addWidget(self.EntitiesLink)

        self.EntitiesExpr = ExprTableWidget(self.EntitiesExpr_widget)
        self.EntitiesExpr_layout.insertWidget(0, self.EntitiesExpr)

        # Select all button on the Point and Link tab as corner widget.
        select_all_button = QPushButton()
        select_all_button.setIcon(QIcon(QPixmap(":/icons/select_all.png")))
        select_all_button.setToolTip("Select all")
        select_all_button.setStatusTip("Select all item of point table.")

        @Slot()
        def table_select_all():
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.EntitiesPoint,
                self.EntitiesLink,
                self.EntitiesExpr,
            ]
            tables[self.EntitiesTab.currentIndex()].selectAll()

        select_all_button.clicked.connect(table_select_all)
        self.EntitiesTab.setCornerWidget(select_all_button)
        select_all_action = QAction("Select all point", self)
        select_all_action.triggered.connect(table_select_all)
        select_all_action.setShortcut("Ctrl+A")
        select_all_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(select_all_action)

        # QPainter canvas window
        self.MainCanvas = DynamicCanvas(self)
        self.EntitiesTab.currentChanged.connect(self.MainCanvas.set_selection_mode)

        @Slot(tuple, bool)
        def table_set_selection(selections: Tuple[int], key_detect: bool):
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.EntitiesPoint,
                self.EntitiesLink,
                self.EntitiesExpr,
            ]
            tables[self.EntitiesTab.currentIndex()].set_selections(selections, key_detect)

        self.MainCanvas.selected.connect(table_set_selection)
        self.EntitiesPoint.row_selection_changed.connect(self.MainCanvas.set_selection)

        @Slot()
        def table_clear_selection():
            """Distinguish table by tab index."""
            tables: List[BaseTableWidget] = [
                self.EntitiesPoint,
                self.EntitiesLink,
                self.EntitiesExpr,
            ]
            tables[self.EntitiesTab.currentIndex()].clearSelection()

        self.MainCanvas.noselected.connect(table_clear_selection)

        clean_selection_action = QAction("Clean selection", self)
        clean_selection_action.triggered.connect(table_clear_selection)
        clean_selection_action.setShortcut("Esc")
        clean_selection_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(clean_selection_action)

        self.MainCanvas.free_moved.connect(self.set_free_move)
        self.MainCanvas.alt_add.connect(self.q_add_normal_point)
        self.MainCanvas.doubleclick_edit.connect(self.edit_point)
        self.MainCanvas.zoom_changed.connect(self.ZoomBar.setValue)
        self.MainCanvas.tracking.connect(self.set_mouse_pos)
        self.canvasSplitter.insertWidget(0, self.MainCanvas)
        self.canvasSplitter.setSizes([600, 10, 30])

        # Selection label on status bar right side.
        selection_label = SelectionLabel(self)
        self.EntitiesPoint.selectionLabelUpdate.connect(
            selection_label.update_select_point
        )
        self.MainCanvas.browse_tracking.connect(
            selection_label.update_mouse_position
        )
        self.status_bar.addPermanentWidget(selection_label)

        # FPS label on status bar right side.
        fps_label = FPSLabel(self)
        self.MainCanvas.fps_updated.connect(fps_label.update_text)
        self.status_bar.addPermanentWidget(fps_label)

        # Inputs widget.
        self.InputsWidget = InputsWidget(self)
        self.inputs_tab_layout.addWidget(self.InputsWidget)
        self.free_move_button.toggled.connect(self.InputsWidget.variable_value_reset)
        self.InputsWidget.about_to_resolve.connect(self.resolve)

        @Slot(tuple, bool)
        def inputs_set_selection(selections: Tuple[int], _: bool):
            """Distinguish table by tab index."""
            self.InputsWidget.clear_selection()
            if self.EntitiesTab.currentIndex() == 0:
                self.InputsWidget.set_selection(selections)

        self.MainCanvas.selected.connect(inputs_set_selection)
        self.MainCanvas.noselected.connect(self.InputsWidget.clear_selection)
        self.InputsWidget.update_preview_button.clicked.connect(self.MainCanvas.update_preview_path)

        # Number and type synthesis.
        self.StructureSynthesis = StructureSynthesis(self)
        self.SynthesisTab.addTab(
            self.StructureSynthesis,
            self.StructureSynthesis.windowIcon(),
            "Structural"
        )

        # Synthesis collections
        self.CollectionTabPage = Collections(self)
        self.SynthesisTab.addTab(
            self.CollectionTabPage,
            self.CollectionTabPage.windowIcon(),
            "Collections"
        )
        self.StructureSynthesis.addCollection = (
            self.CollectionTabPage.StructureWidget.add_collection
        )

        # Dimensional synthesis
        self.DimensionalSynthesis = DimensionalSynthesis(self)
        self.MainCanvas.set_target_point.connect(self.DimensionalSynthesis.set_point)
        self.SynthesisTab.addTab(
            self.DimensionalSynthesis,
            self.DimensionalSynthesis.windowIcon(),
            "Dimensional"
        )

        # File widget settings.
        self.DatabaseWidget = DatabaseWidget(self)
        self.SCMLayout.addWidget(self.DatabaseWidget)
        self.DatabaseWidget.commit_add.clicked.connect(self.commit)
        self.DatabaseWidget.branch_add.clicked.connect(self.commit_branch)
        self.action_stash.triggered.connect(self.DatabaseWidget.stash)

        # YAML editor.
        self.YamlEditor = YamlEditor(self)

        # Console dock will hide when startup.
        self.ConsoleWidget.hide()

        # Connect to GUI button switching.
        self.console_disconnect_button.setEnabled(not ARGUMENTS.debug_mode)
        self.console_connect_button.setEnabled(ARGUMENTS.debug_mode)

        # Splitter stretch factor.
        self.MainSplitter.setStretchFactor(0, 4)
        self.MainSplitter.setStretchFactor(1, 15)
        self.MechanismPanelSplitter.setSizes([500, 200])
        self.synthesis_splitter.setSizes([100, 500])

        # Enable mechanism menu actions when shows.
        self.menu_Mechanism.aboutToShow.connect(self.enable_mechanism_actions)

        # Start a new window.
        @Slot()
        def new_main_window():
            run = self.__class__()
            run.show()

        self.action_new_window.triggered.connect(new_main_window)

    def __free_move(self):
        """Menu of free move mode."""
        free_move_mode_menu = QMenu(self)

        def free_move_mode_func(j: int, icon_qt: QIcon):

            @Slot()
            def func():
                self.free_move_button.setIcon(icon_qt)
                self.MainCanvas.set_free_move(j)
                self.EntitiesTab.setCurrentIndex(0)
                self.InputsWidget.variable_stop.click()

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

        # "Link adjust" function
        self.link_free_move_confirm.clicked.connect(self.MainCanvas.emit_free_move_all)

    def __options(self):
        """Signal connection for option widgets.

        + Spin boxes
        + Combo boxes
        + Check boxes
        """
        # While value change, update the canvas widget.
        self.settings = QSettings('Kmol', 'Pyslvs')
        self.ZoomBar.valueChanged.connect(self.MainCanvas.set_zoom)
        self.linewidth_option.valueChanged.connect(self.MainCanvas.set_link_width)
        self.pathwidth_option.valueChanged.connect(self.MainCanvas.set_path_width)
        self.fontsize_option.valueChanged.connect(self.MainCanvas.set_font_size)
        self.action_show_point_mark.toggled.connect(self.MainCanvas.set_point_mark)
        self.action_show_dimensions.toggled.connect(self.MainCanvas.set_show_dimension)
        self.selectionradius_option.valueChanged.connect(self.MainCanvas.set_selection_radius)
        self.linktrans_option.valueChanged.connect(self.MainCanvas.set_transparency)
        self.marginfactor_option.valueChanged.connect(self.MainCanvas.set_margin_factor)
        self.jointsize_option.valueChanged.connect(self.MainCanvas.set_joint_size)
        self.zoomby_option.currentIndexChanged.connect(self.MainCanvas.set_zoom_by)
        self.snap_option.valueChanged.connect(self.MainCanvas.set_snap)
        self.background_option.textChanged.connect(self.MainCanvas.set_background)
        self.background_opacity_option.valueChanged.connect(self.MainCanvas.set_background_opacity)
        self.background_scale_option.valueChanged.connect(self.MainCanvas.set_background_scale)
        self.background_offset_x_option.valueChanged.connect(self.MainCanvas.set_background_offset_x)
        self.background_offset_y_option.valueChanged.connect(self.MainCanvas.set_background_offset_y)
        # Resolve after change current kernel.
        self.planarsolver_option.addItems(kernel_list)
        self.pathpreview_option.addItems(kernel_list + ("Same as solver kernel",))
        self.planarsolver_option.currentIndexChanged.connect(self.solve)
        self.pathpreview_option.currentIndexChanged.connect(self.solve)
        self.settings_reset.clicked.connect(self.reset_options)

    def __zoom(self):
        """Zoom functions.

        + 'zoom to fit' function connections.
        + Zoom text buttons
        """
        self.action_zoom_to_fit.triggered.connect(
            self.MainCanvas.zoom_to_fit
        )
        self.ResetCanvas.clicked.connect(self.MainCanvas.zoom_to_fit)

        zoom_menu = QMenu(self)

        def zoom_level(value: int):
            """Return a function that set the specified zoom value."""

            @Slot()
            def func():
                return self.ZoomBar.setValue(value)

            return func

        for level in range(
            self.ZoomBar.minimum() - self.ZoomBar.minimum() % 100 + 100,
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

    def __point_context_menu(self):
        """EntitiesPoint context menu

        + Add
        ///////
        + New Link
        + Edit
        + Grounded
        + Multiple joint
            - Point0
            - Point1
            - ...
        + Copy table data
        + Clone
        -------
        + Delete
        """
        self.EntitiesPoint_widget.customContextMenuRequested.connect(
            self.point_context_menu
        )
        self.pop_menu_point = QMenu(self)
        self.pop_menu_point.setSeparatorsCollapsible(True)
        self.action_point_context_add = QAction("&Add", self)
        self.action_point_context_add.triggered.connect(self.new_point)
        self.pop_menu_point.addAction(self.action_point_context_add)
        # New Link
        self.pop_menu_point.addAction(self.action_new_link)
        self.action_point_context_edit = QAction("&Edit", self)
        self.action_point_context_edit.triggered.connect(self.edit_point)
        self.pop_menu_point.addAction(self.action_point_context_edit)
        self.action_point_context_lock = QAction("&Grounded", self)
        self.action_point_context_lock.setCheckable(True)
        self.action_point_context_lock.triggered.connect(self.lock_points)
        self.pop_menu_point.addAction(self.action_point_context_lock)
        self.pop_menu_point_merge = QMenu(self)
        self.pop_menu_point_merge.setTitle("Multiple joint")
        self.pop_menu_point.addMenu(self.pop_menu_point_merge)
        self.action_point_context_copydata = QAction("&Copy table data", self)
        self.action_point_context_copydata.triggered.connect(self.copy_points_table)
        self.pop_menu_point.addAction(self.action_point_context_copydata)
        self.action_point_context_copyCoord = QAction("&Copy coordinate", self)
        self.action_point_context_copyCoord.triggered.connect(self.copy_coord)
        self.pop_menu_point.addAction(self.action_point_context_copyCoord)
        self.action_point_context_copyPoint = QAction("C&lone", self)
        self.action_point_context_copyPoint.triggered.connect(self.clone_point)
        self.pop_menu_point.addAction(self.action_point_context_copyPoint)
        self.pop_menu_point.addSeparator()
        self.action_point_context_delete = QAction("&Delete", self)
        self.action_point_context_delete.triggered.connect(self.delete_points)
        self.pop_menu_point.addAction(self.action_point_context_delete)

    def __link_context_menu(self):
        """EntitiesLink context menu

        + Add
        + Edit
        + Merge links
            - Link0
            - Link1
            - ...
        + Copy table data
        + Release / Constrain
        -------
        + Delete
        """
        self.EntitiesLink_widget.customContextMenuRequested.connect(
            self.link_context_menu
        )
        self.pop_menu_link = QMenu(self)
        self.pop_menu_link.setSeparatorsCollapsible(True)
        self.action_link_context_add = QAction("&Add", self)
        self.action_link_context_add.triggered.connect(self.new_link)
        self.pop_menu_link.addAction(self.action_link_context_add)
        self.action_link_context_edit = QAction("&Edit", self)
        self.action_link_context_edit.triggered.connect(self.edit_link)
        self.pop_menu_link.addAction(self.action_link_context_edit)
        self.pop_menu_link_merge = QMenu(self)
        self.pop_menu_link_merge.setTitle("Merge links")
        self.pop_menu_link.addMenu(self.pop_menu_link_merge)
        self.action_link_context_copydata = QAction("&Copy table data", self)
        self.action_link_context_copydata.triggered.connect(self.copy_links_table)
        self.pop_menu_link.addAction(self.action_link_context_copydata)
        self.action_link_context_release = QAction("&Release", self)
        self.action_link_context_release.triggered.connect(self.release_ground)
        self.pop_menu_link.addAction(self.action_link_context_release)
        self.action_link_context_constrain = QAction("C&onstrain", self)
        self.action_link_context_constrain.triggered.connect(self.constrain_link)
        self.pop_menu_link.addAction(self.action_link_context_constrain)
        self.pop_menu_link.addSeparator()
        self.action_link_context_delete = QAction("&Delete", self)
        self.action_link_context_delete.triggered.connect(self.delete_links)
        self.pop_menu_link.addAction(self.action_link_context_delete)

    def __canvas_context_menu(self):
        """MainCanvas context menus,
            switch the actions when selection mode changed.

        + Actions set of points.
        + Actions set of links.
        """
        self.MainCanvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.MainCanvas.customContextMenuRequested.connect(self.canvas_context_menu)
        """
        Actions set of points:
        
        + Add
        ///////
        + New Link
        + Add [fixed]
        + Add [target path]
        ///////
        + Edit
        + Grounded
        + Multiple joint
            - Point0
            - Point1
            - ...
        + Clone
        + Copy coordinate
        -------
        + Delete
        """
        self.pop_menu_canvas_p = QMenu(self)
        self.pop_menu_canvas_p.setSeparatorsCollapsible(True)
        self.action_canvas_context_add = QAction("&Add", self)
        self.action_canvas_context_add.triggered.connect(self.add_normal_point)
        self.pop_menu_canvas_p.addAction(self.action_canvas_context_add)
        # New Link
        self.pop_menu_canvas_p.addAction(self.action_new_link)
        self.action_canvas_context_grounded_add = QAction("Add [grounded]", self)
        self.action_canvas_context_grounded_add.triggered.connect(self.add_fixed_point)
        self.pop_menu_canvas_p.addAction(self.action_canvas_context_grounded_add)
        self.action_canvas_context_path = QAction("Add [target path]", self)
        self.action_canvas_context_path.triggered.connect(self.add_target_point)
        self.pop_menu_canvas_p.addAction(self.action_canvas_context_path)
        # The following actions will be shown when points selected.
        self.pop_menu_canvas_p.addAction(self.action_point_context_edit)
        self.pop_menu_canvas_p.addAction(self.action_point_context_lock)
        self.pop_menu_canvas_p.addMenu(self.pop_menu_point_merge)
        self.pop_menu_canvas_p.addAction(self.action_point_context_copyCoord)
        self.pop_menu_canvas_p.addAction(self.action_point_context_copyPoint)
        self.pop_menu_canvas_p.addSeparator()
        self.pop_menu_canvas_p.addAction(self.action_point_context_delete)
        """
        Actions set of links:
        
        + Add
        ///////
        + Add [target path]
        ///////
        + Edit
        + Merge links
            - Link0
            - Link1
            - ...
        + Release / Constrain
        -------
        + Delete
        """
        self.pop_menu_canvas_l = QMenu(self)
        self.pop_menu_canvas_l.setSeparatorsCollapsible(True)
        self.pop_menu_canvas_l.addAction(self.action_link_context_add)
        self.pop_menu_canvas_l.addAction(self.action_link_context_edit)
        self.pop_menu_canvas_l.addMenu(self.pop_menu_link_merge)
        self.pop_menu_canvas_l.addAction(self.action_link_context_constrain)
        self.pop_menu_canvas_l.addSeparator()
        self.pop_menu_canvas_l.addAction(self.action_link_context_delete)

    @Slot(int, name='on_EntitiesTab_currentChanged')
    def __set_selection_mode(self, index: int):
        """Connect selection signal for main canvas."""
        # Set selection from click table items.
        tables: List[BaseTableWidget] = [
            self.EntitiesPoint,
            self.EntitiesLink,
            self.EntitiesExpr,
        ]
        try:
            for table in tables:
                table.row_selection_changed.disconnect()
        except TypeError:
            pass

        tables[index].row_selection_changed.connect(self.MainCanvas.set_selection)
        # Double click signal.
        try:
            self.MainCanvas.doubleclick_edit.disconnect()
        except TypeError:
            pass
        if index == 0:
            self.MainCanvas.doubleclick_edit.connect(self.edit_point)
        elif index == 1:
            self.MainCanvas.doubleclick_edit.connect(self.edit_link)
        # Clear all selections.
        for table in tables:
            table.clearSelection()
        self.InputsWidget.clear_selection()

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
    def delete_points(self) -> None:
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
    def delete_links(self) -> None:
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
    def q_add_normal_point(self, x: float, y: float) -> None:
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
        auto_preview: List[List[Tuple[float, float]]],
        slider_auto_preview: Dict[int, List[Tuple[float, float]]],
        vpoints: Tuple[VPoint, ...]
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
        row: int,
        path: Sequence[Sequence[Tuple[float, float]]]
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
