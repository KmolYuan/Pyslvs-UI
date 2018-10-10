# -*- coding: utf-8 -*-

"""The custom widgets of main window.

+ Sub widgets.
+ Context menus.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence
from abc import abstractmethod
from core.QtModules import (
    pyqtSlot,
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
    QAbcMeta,
)
from core.info import __version__, ARGUMENTS
from core.libs import kernel_list
from core.io import YamlEditor, DatabaseWidget
from core.synthesis import (
    StructureSynthesis,
    Collections,
    DimensionalSynthesis,
)
from .Ui_main import Ui_MainWindow
from .main_canvas import DynamicCanvas
from .tables import (
    PointTableWidget,
    LinkTableWidget,
    ExprTableWidget,
    SelectionLabel,
    FPSLabel,
)
from .inputs import InputsWidget
_major, _minor, _build, _label = __version__


class MainWindowUiInterface(QMainWindow, Ui_MainWindow, metaclass=QAbcMeta):

    """External UI settings."""

    def __init__(self):
        super(MainWindowUiInterface, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.env = ""

        self.setLocate(
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
        super(MainWindowUiInterface, self).show()
        self.MainCanvas.zoomToFit()

    def setLocate(self, locate: str):
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
        self.CommandStack.indexChanged.connect(self.commandReload)
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
        self.EntitiesPoint.cellDoubleClicked.connect(self.editPoint)
        self.EntitiesPoint.deleteRequest.connect(self.deletePoints)
        self.EntitiesPoint_layout.addWidget(self.EntitiesPoint)

        self.EntitiesLink = LinkTableWidget(self.EntitiesLink_widget)
        self.EntitiesLink.cellDoubleClicked.connect(self.editLink)
        self.EntitiesLink.deleteRequest.connect(self.deleteLinks)
        self.EntitiesLink_layout.addWidget(self.EntitiesLink)

        self.EntitiesExpr = ExprTableWidget(self.EntitiesExpr_widget)
        self.EntitiesExpr.reset.connect(self.link_free_move_widget.setEnabled)
        self.EntitiesExpr.free_move_request.connect(self.setLinkFreeMove)
        self.EntitiesExpr_layout.insertWidget(0, self.EntitiesExpr)

        # Link free mode slide bar.
        self.link_free_move_slider.valueChanged.connect(
            self.link_free_move_spinbox.setValue
        )
        self.link_free_move_spinbox.valueChanged.connect(
            self.link_free_move_slider.setValue
        )
        self.link_free_move_slider.rangeChanged.connect(
            self.link_free_move_spinbox.setRange
        )

        # Select all button on the Point and Link tab as corner widget.
        select_all_button = QPushButton()
        select_all_button.setIcon(QIcon(QPixmap(":/icons/select_all.png")))
        select_all_button.setToolTip("Select all")
        select_all_button.setStatusTip("Select all item of point table.")

        @pyqtSlot()
        def table_select_all():
            """Distinguish table by tab index."""
            tables = (self.EntitiesPoint, self.EntitiesLink, self.EntitiesExpr)
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
        self.EntitiesTab.currentChanged.connect(self.MainCanvas.setSelectionMode)

        @pyqtSlot(tuple, bool)
        def table_set_selection(selections: Tuple[int], key_detect: bool):
            """Distinguish table by tab index."""
            tables = (self.EntitiesPoint, self.EntitiesLink, self.EntitiesExpr)
            tables[self.EntitiesTab.currentIndex()].setSelections(selections, key_detect)

        self.MainCanvas.selected.connect(table_set_selection)
        self.EntitiesPoint.rowSelectionChanged.connect(self.MainCanvas.setSelection)

        @pyqtSlot()
        def table_clear_selection():
            """Distinguish table by tab index."""
            tables = (self.EntitiesPoint, self.EntitiesLink, self.EntitiesExpr)
            tables[self.EntitiesTab.currentIndex()].clearSelection()

        self.MainCanvas.noselected.connect(table_clear_selection)

        clean_selection_action = QAction("Clean selection", self)
        clean_selection_action.triggered.connect(table_clear_selection)
        clean_selection_action.setShortcut("Esc")
        clean_selection_action.setShortcutContext(Qt.WindowShortcut)
        self.addAction(clean_selection_action)

        self.MainCanvas.free_moved.connect(self.setFreeMove)
        self.MainCanvas.alt_add.connect(self.qAddNormalPoint)
        self.MainCanvas.doubleclick_edit.connect(self.editPoint)
        self.MainCanvas.zoom_changed.connect(self.ZoomBar.setValue)
        self.MainCanvas.tracking.connect(self.setMousePos)
        self.canvasSplitter.insertWidget(0, self.MainCanvas)
        self.canvasSplitter.setSizes([600, 10, 30])

        # Selection label on status bar right side.
        selection_label = SelectionLabel(self)
        self.EntitiesPoint.selectionLabelUpdate.connect(
            selection_label.updateSelectPoint
        )
        self.MainCanvas.browse_tracking.connect(selection_label.updateMousePosition)
        self.status_bar.addPermanentWidget(selection_label)

        # FPS label on status bar right side.
        fps_label = FPSLabel(self)
        self.MainCanvas.fps_updated.connect(fps_label.updateText)
        self.status_bar.addPermanentWidget(fps_label)

        # Inputs widget.
        self.InputsWidget = InputsWidget(self)
        self.inputs_tab_layout.addWidget(self.InputsWidget)
        self.free_move_button.toggled.connect(self.InputsWidget.variableValueReset)
        self.InputsWidget.aboutToResolve.connect(self.resolve)

        @pyqtSlot(tuple, bool)
        def inputs_set_selection(selections: Tuple[int], _: bool):
            """Distinguish table by tab index."""
            self.InputsWidget.clearSelection()
            if self.EntitiesTab.currentIndex() == 0:
                self.InputsWidget.setSelection(selections)

        self.MainCanvas.selected.connect(inputs_set_selection)
        self.MainCanvas.noselected.connect(self.InputsWidget.clearSelection)
        self.InputsWidget.update_preview_button.clicked.connect(self.MainCanvas.updatePreviewPath)

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
            self.CollectionTabPage.StructureWidget.addCollection
        )

        # Dimensional synthesis
        self.DimensionalSynthesis = DimensionalSynthesis(self)
        self.MainCanvas.set_target_point.connect(self.DimensionalSynthesis.setPoint)
        self.SynthesisTab.addTab(
            self.DimensionalSynthesis,
            self.DimensionalSynthesis.windowIcon(),
            "Dimensional"
        )

        # YAML editor.
        self.YamlEditor = YamlEditor(self)

        # File widget settings.
        self.DatabaseWidget = DatabaseWidget(self)
        self.SCMLayout.addWidget(self.DatabaseWidget)
        self.DatabaseWidget.commit_add.clicked.connect(self.commit)
        self.DatabaseWidget.branch_add.clicked.connect(self.commit_branch)
        self.action_stash.triggered.connect(self.DatabaseWidget.stash)

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
        self.menu_Mechanism.aboutToShow.connect(self.enableMechanismActions)

        # Start a new window.
        @pyqtSlot()
        def new_main_window():
            run = self.__class__()
            run.show()

        self.action_new_window.triggered.connect(new_main_window)

    def __free_move(self):
        """Menu of free move mode."""
        free_move_mode_menu = QMenu(self)

        def free_move_mode_func(j: int, icon_qt: QIcon):

            @pyqtSlot()
            def func():
                self.free_move_button.setIcon(icon_qt)
                self.MainCanvas.setFreeMove(j)
                self.EntitiesTab.setCurrentIndex(0)
                self.InputsWidget.variable_stop.click()

            return func

        for i, (text, icon, tip) in enumerate((
            ("View mode", "free_move_off", "Disable free move mode."),
            ("Translate mode", "translate", "Edit by 2 DOF moving."),
            ("Rotate mode", "rotate", "Edit by 1 DOF moving."),
            ("Reflect mode", "reflect", "Edit by flip axis."),
        )):
            action = QAction(QIcon(QPixmap(f":/icons/{icon}.png")), text, self)
            action.triggered.connect(free_move_mode_func(i, action.icon()))
            action.setShortcut(QKeySequence(f"Ctrl+{i + 1}"))
            action.setShortcutContext(Qt.WindowShortcut)
            action.setStatusTip(tip)
            free_move_mode_menu.addAction(action)
            if i == 0:
                self.free_move_disable = action
        self.free_move_button.setMenu(free_move_mode_menu)

        # Link free move by expression table.
        self.link_free_move_slider.sliderReleased.connect(
            self.MainCanvas.emit_free_move_all
        )

    def __options(self):
        """Signal connection for option widgets.

        + Spin boxes
        + Combo boxes
        + Check boxes
        """
        # While value change, update the canvas widget.
        self.settings = QSettings('Kmol', 'Pyslvs')
        self.ZoomBar.valueChanged.connect(self.MainCanvas.setZoom)
        self.linewidth_option.valueChanged.connect(self.MainCanvas.setLinkWidth)
        self.pathwidth_option.valueChanged.connect(self.MainCanvas.setPathWidth)
        self.fontsize_option.valueChanged.connect(self.MainCanvas.setFontSize)
        self.action_show_point_mark.toggled.connect(self.MainCanvas.setPointMark)
        self.action_show_dimensions.toggled.connect(self.MainCanvas.setShowDimension)
        self.selectionradius_option.valueChanged.connect(self.MainCanvas.setSelectionRadius)
        self.linktrans_option.valueChanged.connect(self.MainCanvas.setTransparency)
        self.marginfactor_option.valueChanged.connect(self.MainCanvas.setMarginFactor)
        self.jointsize_option.valueChanged.connect(self.MainCanvas.setJointSize)
        self.zoomby_option.currentIndexChanged.connect(self.MainCanvas.setZoomBy)
        self.snap_option.valueChanged.connect(self.MainCanvas.setSnap)
        self.background_option.textChanged.connect(self.MainCanvas.setBackground)
        self.background_opacity_option.valueChanged.connect(self.MainCanvas.setBackgroundOpacity)
        self.background_scale_option.valueChanged.connect(self.MainCanvas.setBackgroundScale)
        self.background_offset_x_option.valueChanged.connect(self.MainCanvas.setBackgroundOffsetX)
        self.background_offset_y_option.valueChanged.connect(self.MainCanvas.setBackgroundOffsetY)
        # Resolve after change current kernel.
        self.planarsolver_option.addItems(kernel_list)
        self.pathpreview_option.addItems(kernel_list + ("Same as solver kernel",))
        self.planarsolver_option.currentIndexChanged.connect(self.solve)
        self.pathpreview_option.currentIndexChanged.connect(self.solve)
        self.settings_reset.clicked.connect(self.resetOptions)

    def __zoom(self):
        """Zoom functions.

        + 'zoom to fit' function connections.
        + Zoom text buttons
        """
        self.action_zoom_to_fit.triggered.connect(
            self.MainCanvas.zoomToFit
        )
        self.ResetCanvas.clicked.connect(self.MainCanvas.zoomToFit)

        zoom_menu = QMenu(self)

        def zoom_level(value: int):
            """Return a function that set the specified zoom value."""

            @pyqtSlot()
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
        action.triggered.connect(self.customizeZoom)
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
        self.popMenu_point = QMenu(self)
        self.popMenu_point.setSeparatorsCollapsible(True)
        self.action_point_context_add = QAction("&Add", self)
        self.action_point_context_add.triggered.connect(self.newPoint)
        self.popMenu_point.addAction(self.action_point_context_add)
        # New Link
        self.popMenu_point.addAction(self.action_new_link)
        self.action_point_context_edit = QAction("&Edit", self)
        self.action_point_context_edit.triggered.connect(self.editPoint)
        self.popMenu_point.addAction(self.action_point_context_edit)
        self.action_point_context_lock = QAction("&Grounded", self)
        self.action_point_context_lock.setCheckable(True)
        self.action_point_context_lock.triggered.connect(self.lockPoints)
        self.popMenu_point.addAction(self.action_point_context_lock)
        self.popMenu_point_merge = QMenu(self)
        self.popMenu_point_merge.setTitle("Multiple joint")
        self.popMenu_point.addMenu(self.popMenu_point_merge)
        self.action_point_context_copydata = QAction("&Copy table data", self)
        self.action_point_context_copydata.triggered.connect(self.copyPointsTable)
        self.popMenu_point.addAction(self.action_point_context_copydata)
        self.action_point_context_copyCoord = QAction("&Copy coordinate", self)
        self.action_point_context_copyCoord.triggered.connect(self.copyCoord)
        self.popMenu_point.addAction(self.action_point_context_copyCoord)
        self.action_point_context_copyPoint = QAction("C&lone", self)
        self.action_point_context_copyPoint.triggered.connect(self.clonePoint)
        self.popMenu_point.addAction(self.action_point_context_copyPoint)
        self.popMenu_point.addSeparator()
        self.action_point_context_delete = QAction("&Delete", self)
        self.action_point_context_delete.triggered.connect(self.deletePoints)
        self.popMenu_point.addAction(self.action_point_context_delete)

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
        self.popMenu_link = QMenu(self)
        self.popMenu_link.setSeparatorsCollapsible(True)
        self.action_link_context_add = QAction("&Add", self)
        self.action_link_context_add.triggered.connect(self.newLink)
        self.popMenu_link.addAction(self.action_link_context_add)
        self.action_link_context_edit = QAction("&Edit", self)
        self.action_link_context_edit.triggered.connect(self.editLink)
        self.popMenu_link.addAction(self.action_link_context_edit)
        self.popMenu_link_merge = QMenu(self)
        self.popMenu_link_merge.setTitle("Merge links")
        self.popMenu_link.addMenu(self.popMenu_link_merge)
        self.action_link_context_copydata = QAction("&Copy table data", self)
        self.action_link_context_copydata.triggered.connect(self.copyLinksTable)
        self.popMenu_link.addAction(self.action_link_context_copydata)
        self.action_link_context_release = QAction("&Release", self)
        self.action_link_context_release.triggered.connect(self.releaseGround)
        self.popMenu_link.addAction(self.action_link_context_release)
        self.action_link_context_constrain = QAction("C&onstrain", self)
        self.action_link_context_constrain.triggered.connect(self.constrainLink)
        self.popMenu_link.addAction(self.action_link_context_constrain)
        self.popMenu_link.addSeparator()
        self.action_link_context_delete = QAction("&Delete", self)
        self.action_link_context_delete.triggered.connect(self.deleteLinks)
        self.popMenu_link.addAction(self.action_link_context_delete)

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
        self.popMenu_canvas_p = QMenu(self)
        self.popMenu_canvas_p.setSeparatorsCollapsible(True)
        self.action_canvas_context_add = QAction("&Add", self)
        self.action_canvas_context_add.triggered.connect(self.addNormalPoint)
        self.popMenu_canvas_p.addAction(self.action_canvas_context_add)
        # New Link
        self.popMenu_canvas_p.addAction(self.action_new_link)
        self.action_canvas_context_grounded_add = QAction("Add [grounded]", self)
        self.action_canvas_context_grounded_add.triggered.connect(self.addFixedPoint)
        self.popMenu_canvas_p.addAction(self.action_canvas_context_grounded_add)
        self.action_canvas_context_path = QAction("Add [target path]", self)
        self.action_canvas_context_path.triggered.connect(self.addTargetPoint)
        self.popMenu_canvas_p.addAction(self.action_canvas_context_path)
        # The following actions will be shown when points selected.
        self.popMenu_canvas_p.addAction(self.action_point_context_edit)
        self.popMenu_canvas_p.addAction(self.action_point_context_lock)
        self.popMenu_canvas_p.addMenu(self.popMenu_point_merge)
        self.popMenu_canvas_p.addAction(self.action_point_context_copyCoord)
        self.popMenu_canvas_p.addAction(self.action_point_context_copyPoint)
        self.popMenu_canvas_p.addSeparator()
        self.popMenu_canvas_p.addAction(self.action_point_context_delete)
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
        self.popMenu_canvas_l = QMenu(self)
        self.popMenu_canvas_l.setSeparatorsCollapsible(True)
        self.popMenu_canvas_l.addAction(self.action_link_context_add)
        self.popMenu_canvas_l.addAction(self.action_link_context_edit)
        self.popMenu_canvas_l.addMenu(self.popMenu_link_merge)
        self.popMenu_canvas_l.addAction(self.action_link_context_constrain)
        self.popMenu_canvas_l.addSeparator()
        self.popMenu_canvas_l.addAction(self.action_link_context_delete)

    @abstractmethod
    def commandReload(self, index: int) -> None:
        ...

    @abstractmethod
    def newPoint(self) -> None:
        ...

    @abstractmethod
    def addNormalPoint(self) -> None:
        ...

    @abstractmethod
    def addFixedPoint(self) -> None:
        ...

    @abstractmethod
    def editPoint(self) -> None:
        ...

    @abstractmethod
    def deletePoints(self) -> None:
        ...

    @abstractmethod
    def lockPoints(self) -> None:
        ...

    @abstractmethod
    def newLink(self) -> None:
        ...

    @abstractmethod
    def editLink(self) -> None:
        ...

    @abstractmethod
    def deleteLinks(self) -> None:
        ...

    @abstractmethod
    def constrainLink(self) -> None:
        ...

    @abstractmethod
    def releaseGround(self) -> None:
        ...

    @abstractmethod
    def addTargetPoint(self) -> None:
        ...

    @abstractmethod
    def setLinkFreeMove(self, enable: bool) -> None:
        ...

    @abstractmethod
    def setFreeMove(self, args: Sequence[Tuple[int, Tuple[float, float, float]]]) -> None:
        ...

    @abstractmethod
    def qAddNormalPoint(self, x: float, y: float) -> None:
        ...

    @abstractmethod
    def setMousePos(self, x: float, y: float) -> None:
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
    def enableMechanismActions(self) -> None:
        ...

    @abstractmethod
    def clonePoint(self) -> None:
        ...

    @abstractmethod
    def copyCoord(self) -> None:
        ...

    @abstractmethod
    def copyPointsTable(self) -> None:
        ...

    @abstractmethod
    def copyLinksTable(self) -> None:
        ...

    @abstractmethod
    def canvas_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def link_context_menu(self, point: QPoint) -> None:
        ...

    @abstractmethod
    def customizeZoom(self) -> None:
        ...

    @abstractmethod
    def resetOptions(self) -> None:
        ...
