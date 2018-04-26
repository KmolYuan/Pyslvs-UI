# -*- coding: utf-8 -*-

"""The custom widgets of main window.

+ Sub eidgets.
+ Context menus.
"""

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
from .tables import (
    PointTableWidget,
    LinkTableWidget,
    ExprTableWidget,
    SelectionLabel,
)
from .inputs import InputsWidget


def initCustomWidgets(self):
    """Start up custom widgets."""
    _undo_redo(self)
    _appearance(self)
    _context_menu(self)

def _undo_redo(self):
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

def _appearance(self):
    """Start up and initialize custom widgets."""
    #Version label
    self.version_label.setText("v{}.{}.{} ({})".format(*VERSION))
    
    #Entities tables.
    self.EntitiesPoint = PointTableWidget(self.Entities_Point_Widget)
    self.EntitiesPoint.cellDoubleClicked.connect(
        self.on_action_Edit_Point_triggered
    )
    self.EntitiesPoint.deleteRequest.connect(
        self.on_action_Delete_Point_triggered
    )
    self.Entities_Point_Layout.addWidget(self.EntitiesPoint)
    self.EntitiesLink = LinkTableWidget(self.Entities_Link_Widget)
    self.EntitiesLink.cellDoubleClicked.connect(
        self.on_action_Edit_Link_triggered
    )
    self.EntitiesLink.deleteRequest.connect(
        self.on_action_Delete_Link_triggered
    )
    self.Entities_Link_Layout.addWidget(self.EntitiesLink)
    self.Entities_Expr = ExprTableWidget(self.Expression_Widget)
    self.Expression_Layout.addWidget(self.Entities_Expr)
    
    #Selection label on status bar right side.
    selectionLabel = SelectionLabel(self)
    self.EntitiesPoint.selectionLabelUpdate.connect(
        selectionLabel.updateSelectPoint
    )
    self.statusBar.addPermanentWidget(selectionLabel)
    
    #QPainter canvas window
    self.MainCanvas = DynamicCanvas(self)
    self.MainCanvas.mouse_getSelection.connect(
        self.EntitiesPoint.setSelections
    )
    self.MainCanvas.mouse_freemoveSelection.connect(
        self.setFreemoved
    )
    self.MainCanvas.mouse_noSelection.connect(
        self.EntitiesPoint.clearSelection
    )
    CleanSelectionAction = QAction("Clean selection", self)
    CleanSelectionAction.triggered.connect(self.EntitiesPoint.clearSelection)
    CleanSelectionAction.setShortcut("Esc")
    CleanSelectionAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(CleanSelectionAction)
    self.MainCanvas.mouse_getAltAdd.connect(self.qAddNormalPoint)
    self.MainCanvas.mouse_getDoubleClickEdit.connect(
        self.on_action_Edit_Point_triggered
    )
    self.MainCanvas.zoom_change.connect(self.ZoomBar.setValue)
    self.MainCanvas.mouse_track.connect(self.setMousePos)
    self.MainCanvas.mouse_browse_track.connect(
        selectionLabel.updateMousePosition
    )
    self.canvasSplitter.insertWidget(0, self.MainCanvas)
    self.canvasSplitter.setSizes([600, 10, 30])
    
    #Menu of free move mode.
    FreeMoveMode_menu = QMenu(self)
    def freeMoveMode_func(j, qicon):
        @pyqtSlot()
        def func():
            self.FreeMoveMode.setIcon(qicon)
            self.MainCanvas.setFreeMove(j)
            self.InputsWidget.variable_stop.click()
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
    self.MainCanvas.mouse_getSelection.connect(
        self.InputsWidget.setSelection
    )
    self.MainCanvas.mouse_noSelection.connect(
        self.InputsWidget.clearSelection
    )
    
    #Number and type synthesis.
    self.NumberAndTypeSynthesis = NumberAndTypeSynthesis(self)
    self.SynthesisTab.addTab(
        self.NumberAndTypeSynthesis,
        self.NumberAndTypeSynthesis.windowIcon(),
        "Structural"
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
        for variable in self.InputsWidget.getInputsVariables()
    )) #Call to get inputs variables data.
    self.FileWidget.loadCollectFunc = (
        self.CollectionTabPage.CollectionsStructure.addCollections
    ) #Call to load collections data.
    self.FileWidget.loadTriangleFunc = (
        self.CollectionTabPage.CollectionsTriangularIteration.addCollections
    ) #Call to load triangle data.
    self.FileWidget.loadInputsFunc = (
        self.InputsWidget.addInputsVariables
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
        self.MainCanvas.updateRanges
    )
    self.DimensionalSynthesis.pathChanged.connect(
        self.MainCanvas.setSolvingPath
    )
    self.DimensionalSynthesis.mergeResult.connect(self.mergeResult)
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
    SelectAllButton.clicked.connect(self.EntitiesPoint.selectAll)
    self.EntitiesTab.setCornerWidget(SelectAllButton)
    SelectAllAction = QAction("Select all point", self)
    SelectAllAction.triggered.connect(self.EntitiesPoint.selectAll)
    SelectAllAction.setShortcut("Ctrl+A")
    SelectAllAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(SelectAllAction)
    
    #While value change, update the canvas widget.
    self.EntitiesPoint.rowSelectionChanged.connect(
        self.MainCanvas.changePointsSelection
    )
    self.ZoomBar.valueChanged.connect(self.MainCanvas.setZoom)
    self.LineWidth.valueChanged.connect(self.MainCanvas.setLinkWidth)
    self.PathWidth.valueChanged.connect(self.MainCanvas.setPathWidth)
    self.Font_size.valueChanged.connect(self.MainCanvas.setFontSize)
    self.action_Display_Point_Mark.toggled.connect(
        self.MainCanvas.setPointMark
    )
    self.action_Display_Dimensions.toggled.connect(
        self.MainCanvas.setShowDimension
    )
    self.SelectionRadius.valueChanged.connect(
        self.MainCanvas.setSelectionRadius
    )
    self.LinkageTransparency.valueChanged.connect(
        self.MainCanvas.setTransparency
    )
    self.MarginFactor.valueChanged.connect(
        self.MainCanvas.setMarginFactor
    )
    
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 4)
    self.MainSplitter.setStretchFactor(1, 15)
    self.MechanismPanelSplitter.setSizes([500, 200])
    self.synthesis_splitter.setSizes([100, 500])
    
    #Enable mechanism menu actions when shows.
    self.menu_Mechanism.aboutToShow.connect(self.enableMechanismActions)
    
    #'zoom to fit' function connections.
    self.action_Zoom_to_fit.triggered.connect(
        self.MainCanvas.zoomToFit
    )
    self.ResetCanvas.clicked.connect(self.MainCanvas.zoomToFit)
    
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
    action.triggered.connect(self.customizeZoom)
    Zoom_menu.addAction(action)
    self.ZoomText.setMenu(Zoom_menu)

def _context_menu(self):
    '''EntitiesPoint context menu
    
    + Add
    ///////
    + New Linkage
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
    self.action_point_context_delete.triggered.connect(
        self.on_action_Delete_Point_triggered
    )
    self.popMenu_point.addAction(self.action_point_context_delete)
    '''EntitiesLink context menu
    
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
    self.action_link_context_delete.triggered.connect(
        self.on_action_Delete_Link_triggered
    )
    self.popMenu_link.addAction(self.action_link_context_delete)
    '''MainCanvas context menu
    
    + Add
    ///////
    + New Linkage
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
    + Copy coordinate
    -------
    + Delete
    '''
    self.MainCanvas.setContextMenuPolicy(Qt.CustomContextMenu)
    self.MainCanvas.customContextMenuRequested.connect(
        self.on_canvas_context_menu
    )
    self.popMenu_canvas = QMenu(self)
    self.popMenu_canvas.setSeparatorsCollapsible(True)
    self.action_canvas_context_add = QAction("&Add", self)
    self.action_canvas_context_add.triggered.connect(self.addNormalPoint)
    self.popMenu_canvas.addAction(self.action_canvas_context_add)
    #New Link
    self.popMenu_canvas.addAction(self.action_New_Link)
    self.action_canvas_context_fix_add = QAction("Add [fixed]", self)
    self.action_canvas_context_fix_add.triggered.connect(
        self.addFixedPoint
    )
    self.popMenu_canvas.addAction(self.action_canvas_context_fix_add)
    self.action_canvas_context_path = QAction("Add [target path]", self)
    self.action_canvas_context_path.triggered.connect(
        self.addTargetPoint
    )
    self.popMenu_canvas.addAction(self.action_canvas_context_path)
    #The following actions will be shown when points selected.
    self.popMenu_canvas.addAction(self.action_point_context_edit)
    self.popMenu_canvas.addAction(self.action_point_context_lock)
    self.popMenu_canvas.addMenu(self.popMenu_point_merge)
    self.popMenu_canvas.addAction(self.action_point_context_copyCoord)
    self.popMenu_canvas.addAction(self.action_point_context_copyPoint)
    self.popMenu_canvas.addSeparator()
    self.popMenu_canvas.addAction(self.action_point_context_delete)
