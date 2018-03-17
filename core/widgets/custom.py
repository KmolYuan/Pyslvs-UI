# -*- coding: utf-8 -*-

"""The custom widgets of main window."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QAction,
    Qt,
    QMenu,
    pyqtSlot,
    QIcon,
    QPixmap,
    QPushButton,
    QUndoView,
)
from core.info import VERSION
from core.io import FileWidget
from core.synthesis import (
    NumberAndTypeSynthesis,
    Collections,
    DimensionalSynthesis
)
from .main_canvas import DynamicCanvas
from .table import (
    PointTableWidget,
    LinkTableWidget,
    SelectionLabel
)
from .inputs import InputsWidget

def initCustomWidgets(self):
    """Start up custom widgets."""
    undo_redo(self)
    appearance(self)
    context_menu(self)

def undo_redo(self):
    """Undo list settings.
    
    + Undo stack.
    + Undo view widget.
    + Hot keys.
    """
    self.CommandStack.setUndoLimit(self.UndoLimit.value())
    self.UndoLimit.valueChanged.connect(self.CommandStack.setUndoLimit)
    self.CommandStack.indexChanged.connect(self.commandReload)
    self.undoView = QUndoView(self.CommandStack)
    self.undoView.setEmptyLabel("~ Start Pyslvs")
    self.UndoRedoLayout.addWidget(self.undoView)
    self.action_Redo = self.CommandStack.createRedoAction(self, "Redo")
    self.action_Undo = self.CommandStack.createUndoAction(self, "Undo")
    self.action_Redo.setShortcut("Ctrl+Shift+Z")
    self.action_Redo.setStatusTip("Backtracking undo action.")
    self.action_Redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
    self.action_Undo.setShortcut("Ctrl+Z")
    self.action_Undo.setStatusTip("Recover last action.")
    self.action_Undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
    self.menu_Edit.addAction(self.action_Undo)
    self.menu_Edit.addAction(self.action_Redo)

def appearance(self):
    """Start up and initialize custom widgets."""
    #Version label
    self.version_label.setText("v{}.{}.{} ({})".format(*VERSION))
    #Entities tables.
    self.Entities_Point = PointTableWidget(self.Entities_Point_Widget)
    self.Entities_Point.cellDoubleClicked.connect(
        self.on_action_Edit_Point_triggered
    )
    self.Entities_Point.deleteRequest.connect(
        self.on_action_Delete_Point_triggered
    )
    self.Entities_Point_Layout.addWidget(self.Entities_Point)
    self.Entities_Link = LinkTableWidget(self.Entities_Link_Widget)
    self.Entities_Link.cellDoubleClicked.connect(
        self.on_action_Edit_Link_triggered
    )
    self.Entities_Link.deleteRequest.connect(
        self.on_action_Delete_Link_triggered
    )
    self.Entities_Link_Layout.addWidget(self.Entities_Link)
    #Selection label on status bar right side.
    selectionLabel = SelectionLabel(self)
    self.Entities_Point.selectionLabelUpdate.connect(
        selectionLabel.updateSelectPoint
    )
    self.statusBar.addPermanentWidget(selectionLabel)
    #QPainter canvas window
    self.DynamicCanvasView = DynamicCanvas(self)
    self.DynamicCanvasView.mouse_getSelection.connect(
        self.Entities_Point.setSelections
    )
    self.DynamicCanvasView.mouse_freemoveSelection.connect(
        self.freemove_setCoordinate
    )
    self.DynamicCanvasView.mouse_noSelection.connect(
        self.Entities_Point.clearSelection
    )
    CleanSelectionAction = QAction("Clean selection", self)
    CleanSelectionAction.triggered.connect(self.Entities_Point.clearSelection)
    CleanSelectionAction.setShortcut("Esc")
    CleanSelectionAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(CleanSelectionAction)
    self.DynamicCanvasView.mouse_getAltAdd.connect(self.qAddPointGroup)
    self.DynamicCanvasView.mouse_getDoubleClickEdit.connect(
        self.on_action_Edit_Point_triggered
    )
    self.DynamicCanvasView.zoom_change.connect(self.ZoomBar.setValue)
    self.DynamicCanvasView.mouse_track.connect(self.context_menu_mouse_pos)
    self.DynamicCanvasView.mouse_browse_track.connect(
        selectionLabel.updateMousePosition
    )
    self.canvasSplitter.insertWidget(0, self.DynamicCanvasView)
    self.canvasSplitter.setSizes([600, 10, 30])
    #Menu of free move mode.
    FreeMoveMode_menu = QMenu(self)
    def freeMoveMode_func(j, qicon):
        @pyqtSlot()
        def func():
            self.FreeMoveMode.setIcon(qicon)
            self.DynamicCanvasView.setFreeMove(j)
            self.inputs_variable_stop.click()
        return func
    for i, (text, icon) in enumerate([
        ("View mode", "freemove_off"),
        ("Translate mode", "freemove_on"),
        ("Rotate mode", "freemove_on"),
        ("Reflect mode", "freemove_on"),
    ]):
        action = QAction(
            QIcon(QPixmap(":/icons/{}.png".format(icon))),
            text,
            self
        )
        action.triggered.connect(freeMoveMode_func(i, action.icon()))
        action.setShortcut("Ctrl+{}".format(i+1))
        action.setShortcutContext(Qt.WindowShortcut)
        FreeMoveMode_menu.addAction(action)
    self.FreeMoveMode.setMenu(FreeMoveMode_menu)
    #File table settings.
    self.FileWidget = FileWidget(self)
    self.SCMLayout.addWidget(self.FileWidget)
    self.FileWidget.commit_add.clicked.connect(self.on_action_Save_triggered)
    self.FileWidget.branch_add.clicked.connect(
        self.on_action_Save_branch_triggered
    )
    self.action_Stash.triggered.connect(self.FileWidget.on_commit_stash_clicked)
    #Inputs widget.
    self.InputsWidget = InputsWidget(self)
    self.inputs_tab_layout.addWidget(self.InputsWidget)
    self.FreeMoveMode.toggled.connect(self.InputsWidget.variableValueReset)
    self.DynamicCanvasView.mouse_getSelection.connect(
        self.InputsWidget.inputs_points_setSelection
    )
    self.DynamicCanvasView.mouse_noSelection.connect(
        self.InputsWidget.inputs_points_clearSelection
    )
    #Number and type synthesis.
    self.NumberAndTypeSynthesis = NumberAndTypeSynthesis(self)
    self.SynthesisTab.addTab(
        self.NumberAndTypeSynthesis,
        self.NumberAndTypeSynthesis.windowIcon(),
        "Structure"
    )
    #Synthesis collections
    self.CollectionTabPage = Collections(self)
    self.SynthesisTab.addTab(
        self.CollectionTabPage,
        self.CollectionTabPage.windowIcon(),
        "Collections"
    )
    self.NumberAndTypeSynthesis.addCollection = (
        self.CollectionTabPage.CollectionsStructure.addCollection
    )
    self.FileWidget.CollectDataFunc = (
        self.CollectionTabPage.CollectDataFunc
    ) #Call to get collections data.
    self.FileWidget.TriangleDataFunc = (
        self.CollectionTabPage.TriangleDataFunc
    ) #Call to get triangle data.
    self.FileWidget.InputsDataFunc = (lambda: tuple(
        variable[:-1]
        for variable in self.InputsWidget.get_inputs_variables()
    )) #Call to get inputs variables data.
    self.FileWidget.loadCollectFunc = (
        self.CollectionTabPage.CollectionsStructure.addCollections
    ) #Call to load collections data.
    self.FileWidget.loadTriangleFunc = (
        self.CollectionTabPage.CollectionsTriangularIteration.addCollections
    ) #Call to load triangle data.
    self.FileWidget.loadInputsFunc = (
        self.InputsWidget.add_inputs_variables
    ) #Call to load inputs variables data.
    self.FileWidget.loadPathFunc = (
        self.InputsWidget.loadPaths
    ) #Call after loaded paths.
    self.FileWidget.pathDataFunc = (
        lambda: self.InputsWidget.pathData
    ) #Call to get path data.
    #Dimensional synthesis
    self.DimensionalSynthesis = DimensionalSynthesis(self)
    self.DimensionalSynthesis.fixPointRange.connect(
        self.DynamicCanvasView.update_ranges
    )
    self.DimensionalSynthesis.pathChanged.connect(
        self.DynamicCanvasView.setSolvingPath
    )
    self.DimensionalSynthesis.mergeResult.connect(
        self.dimensional_synthesis_mergeResult
    )
    self.FileWidget.AlgorithmDataFunc = (
        lambda: self.DimensionalSynthesis.mechanism_data
    ) #Call to get algorithm data.
    self.FileWidget.loadAlgorithmFunc = (
        self.DimensionalSynthesis.loadResults
    ) #Call after loaded algorithm results.
    self.SynthesisTab.addTab(
        self.DimensionalSynthesis,
        self.DimensionalSynthesis.windowIcon(),
        "Dimensional"
    )
    #Console dock will hide when startup.
    self.ConsoleWidget.hide()
    #Connect to GUI button switching.
    self.disconnectConsoleButton.setEnabled(not self.args.debug_mode)
    self.connectConsoleButton.setEnabled(self.args.debug_mode)
    #Select all button on the Point and Link tab as corner widget.
    SelectAllButton = QPushButton()
    SelectAllButton.setIcon(QIcon(QPixmap(":/icons/select_all.png")))
    SelectAllButton.setToolTip("Select all")
    SelectAllButton.setStatusTip("Select all item of point table.")
    SelectAllButton.clicked.connect(self.Entities_Point.selectAll)
    self.EntitiesTab.setCornerWidget(SelectAllButton)
    SelectAllAction = QAction("Select all point", self)
    SelectAllAction.triggered.connect(self.Entities_Point.selectAll)
    SelectAllAction.setShortcut("Ctrl+A")
    SelectAllAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(SelectAllAction)
    #While value change, update the canvas widget.
    self.Entities_Point.rowSelectionChanged.connect(
        self.DynamicCanvasView.changePointsSelection
    )
    self.ZoomBar.valueChanged.connect(self.DynamicCanvasView.setZoom)
    self.LineWidth.valueChanged.connect(self.DynamicCanvasView.setLinkWidth)
    self.PathWidth.valueChanged.connect(self.DynamicCanvasView.setPathWidth)
    self.Font_size.valueChanged.connect(self.DynamicCanvasView.setFontSize)
    self.action_Display_Point_Mark.toggled.connect(
        self.DynamicCanvasView.setPointMark
    )
    self.action_Display_Dimensions.toggled.connect(
        self.DynamicCanvasView.setShowDimension
    )
    self.SelectionRadius.valueChanged.connect(
        self.DynamicCanvasView.setSelectionRadius
    )
    self.LinkageTransparency.valueChanged.connect(
        self.DynamicCanvasView.setTransparency
    )
    self.MarginFactor.valueChanged.connect(
        self.DynamicCanvasView.setMarginFactor
    )
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 4)
    self.MainSplitter.setStretchFactor(1, 15)
    self.MechanismPanelSplitter.setSizes([500, 200])
    self.synthesis_splitter.setSizes([100, 500])
    #Enable mechanism menu actions when shows.
    self.menu_Mechanism.aboutToShow.connect(self.enableMenu)
    #zoom_to_fit function connections.
    self.action_Zoom_to_fit.triggered.connect(
        self.DynamicCanvasView.zoom_to_fit
    )
    self.ResetCanvas.clicked.connect(self.DynamicCanvasView.zoom_to_fit)
    #Zoom text button
    Zoom_menu = QMenu(self)
    
    def zoom_level(level):
        @pyqtSlot()
        def func():
            self.ZoomBar.setValue(level)
        return func
    
    for level in range(
        self.ZoomBar.minimum() - self.ZoomBar.minimum()%100 + 100,
        500 + 1,
        100
    ):
        action = QAction('{}%'.format(level), self)
        action.triggered.connect(zoom_level(level))
        Zoom_menu.addAction(action)
    action = QAction("customize", self)
    action.triggered.connect(self.zoom_customize)
    Zoom_menu.addAction(action)
    self.ZoomText.setMenu(Zoom_menu)

def context_menu(self):
    '''Entities_Point context menu
    
    + Add
    + Edit
    + Fixed [v]
    + Multiple joint
      - Point0
      - Point1
      - ...
    + Copy table data
    + Clone
    -------
    + Delete
    '''
    self.Entities_Point_Widget.customContextMenuRequested.connect(
        self.on_point_context_menu
    )
    self.popMenu_point = QMenu(self)
    self.popMenu_point.setSeparatorsCollapsible(True)
    self.action_point_context_add = QAction("&Add", self)
    self.action_point_context_add.triggered.connect(
        self.on_action_New_Point_triggered
    )
    self.popMenu_point.addAction(self.action_point_context_add)
    #New Link
    self.popMenu_point.addAction(self.action_New_Link)
    self.action_point_context_edit = QAction("&Edit", self)
    self.action_point_context_edit.triggered.connect(
        self.on_action_Edit_Point_triggered
    )
    self.popMenu_point.addAction(self.action_point_context_edit)
    self.action_point_context_lock = QAction("&Fixed", self)
    self.action_point_context_lock.setCheckable(True)
    self.action_point_context_lock.triggered.connect(self.lockPoint)
    self.popMenu_point.addAction(self.action_point_context_lock)
    self.popMenu_point_merge = QMenu(self)
    self.popMenu_point_merge.setTitle("Multiple joint")
    self.popMenu_point.addMenu(self.popMenu_point_merge)
    self.action_point_context_copydata = QAction("&Copy table data", self)
    self.action_point_context_copydata.triggered.connect(self.tableCopy_Points)
    self.popMenu_point.addAction(self.action_point_context_copydata)
    self.action_point_context_copyPoint = QAction("C&lone", self)
    self.action_point_context_copyPoint.triggered.connect(self.clonePoint)
    self.popMenu_point.addAction(self.action_point_context_copyPoint)
    self.popMenu_point.addSeparator()
    self.action_point_context_delete = QAction("&Delete", self)
    self.action_point_context_delete.triggered.connect(
        self.on_action_Delete_Point_triggered
    )
    self.popMenu_point.addAction(self.action_point_context_delete)
    '''Entities_Link context menu
    
    + Add
    + Edit
    + Copy table data
    + Release / Constrain
    -------
    + Delete
    '''
    self.Entities_Link_Widget.customContextMenuRequested.connect(
        self.on_link_context_menu
    )
    self.popMenu_link = QMenu(self)
    self.popMenu_link.setSeparatorsCollapsible(True)
    self.action_link_context_add = QAction("&Add", self)
    self.action_link_context_add.triggered.connect(
        self.on_action_New_Link_triggered
    )
    self.popMenu_link.addAction(self.action_link_context_add)
    self.action_link_context_edit = QAction("&Edit", self)
    self.action_link_context_edit.triggered.connect(
        self.on_action_Edit_Link_triggered
    )
    self.popMenu_link.addAction(self.action_link_context_edit)
    self.action_link_context_copydata = QAction("&Copy table data", self)
    self.action_link_context_copydata.triggered.connect(self.tableCopy_Links)
    self.popMenu_link.addAction(self.action_link_context_copydata)
    self.action_link_context_release = QAction("&Release", self)
    self.action_link_context_release.triggered.connect(self.releaseGround)
    self.popMenu_link.addAction(self.action_link_context_release)
    self.action_link_context_constrain = QAction("C&onstrain", self)
    self.action_link_context_constrain.triggered.connect(self.constrainLink)
    self.popMenu_link.addAction(self.action_link_context_constrain)
    self.popMenu_link.addSeparator()
    self.action_link_context_delete = QAction("&Delete", self)
    self.action_link_context_delete.triggered.connect(
        self.on_action_Delete_Link_triggered
    )
    self.popMenu_link.addAction(self.action_link_context_delete)
    '''DynamicCanvasView context menu
    
    + Add
    + Add [fixed]
    + Add [target path]
    ///////
    + Edit
    + Fixed
    + Multiple joint
      - Point0
      - Point1
      - ...
    + Clone
    -------
    + Delete
    '''
    self.DynamicCanvasView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.DynamicCanvasView.customContextMenuRequested.connect(
        self.on_canvas_context_menu
    )
    self.popMenu_canvas = QMenu(self)
    self.popMenu_canvas.setSeparatorsCollapsible(True)
    self.action_canvas_context_add = QAction("&Add", self)
    self.action_canvas_context_add.triggered.connect(self.addPointGroup)
    self.popMenu_canvas.addAction(self.action_canvas_context_add)
    #New Link
    self.popMenu_canvas.addAction(self.action_New_Link)
    self.action_canvas_context_fix_add = QAction("Add [fixed]", self)
    self.action_canvas_context_fix_add.triggered.connect(
        self.addPointGroup_fixed
    )
    self.popMenu_canvas.addAction(self.action_canvas_context_fix_add)
    self.action_canvas_context_path = QAction("Add [target path]", self)
    self.action_canvas_context_path.triggered.connect(
        self.dimensional_synthesis_add_rightClick
    )
    self.popMenu_canvas.addAction(self.action_canvas_context_path)
    #The following actions will be shown when points selected.
    self.popMenu_canvas.addAction(self.action_point_context_edit)
    self.popMenu_canvas.addAction(self.action_point_context_lock)
    self.popMenu_canvas.addMenu(self.popMenu_point_merge)
    self.popMenu_canvas.addAction(self.action_point_context_copyPoint)
    self.popMenu_canvas.addSeparator()
    self.popMenu_canvas.addAction(self.action_point_context_delete)
