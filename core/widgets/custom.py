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
    pyqtSlot,
    Qt,
    QAction,
    QMenu,
    QIcon,
    QPixmap,
    QPushButton,
    QKeySequence,
    QSettings,
    QUndoView,
)
from core.info import VERSION
from core.io import FileWidget
from core.synthesis import (
    NumberAndTypeSynthesis,
    Collections,
    DimensionalSynthesis,
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
    _freemove(self)
    _options(self)
    _zoom(self)
    _context_menu(self)


def _undo_redo(self):
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
    self.MainCanvas.selected.connect(
        self.EntitiesPoint.setSelections
    )
    self.MainCanvas.freemoved.connect(
        self.setFreemoved
    )
    self.MainCanvas.noselected.connect(
        self.EntitiesPoint.clearSelection
    )
    CleanSelectionAction = QAction("Clean selection", self)
    CleanSelectionAction.triggered.connect(self.EntitiesPoint.clearSelection)
    CleanSelectionAction.setShortcut("Esc")
    CleanSelectionAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(CleanSelectionAction)
    self.MainCanvas.alt_add.connect(self.qAddNormalPoint)
    self.MainCanvas.doubleclick_edit.connect(
        self.on_action_Edit_Point_triggered
    )
    self.MainCanvas.zoom_changed.connect(self.ZoomBar.setValue)
    self.MainCanvas.tracking.connect(self.setMousePos)
    self.MainCanvas.browse_tracking.connect(
        selectionLabel.updateMousePosition
    )
    self.canvasSplitter.insertWidget(0, self.MainCanvas)
    self.canvasSplitter.setSizes([600, 10, 30])
    
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
    self.freemode_button.toggled.connect(self.InputsWidget.variableValueReset)
    self.InputsWidget.aboutToResolve.connect(self.resolve)
    self.MainCanvas.selected.connect(
        self.InputsWidget.setSelection
    )
    self.MainCanvas.noselected.connect(
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
    select_all_button = QPushButton()
    select_all_button.setIcon(QIcon(QPixmap(":/icons/select_all.png")))
    select_all_button.setToolTip("Select all")
    select_all_button.setStatusTip("Select all item of point table.")
    select_all_button.clicked.connect(self.EntitiesPoint.selectAll)
    self.EntitiesTab.setCornerWidget(select_all_button)
    select_all_action = QAction("Select all point", self)
    select_all_action.triggered.connect(self.EntitiesPoint.selectAll)
    select_all_action.setShortcut("Ctrl+A")
    select_all_action.setShortcutContext(Qt.WindowShortcut)
    self.addAction(select_all_action)
    
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 4)
    self.MainSplitter.setStretchFactor(1, 15)
    self.MechanismPanelSplitter.setSizes([500, 200])
    self.synthesis_splitter.setSizes([100, 500])
    
    #Enable mechanism menu actions when shows.
    self.menu_Mechanism.aboutToShow.connect(self.enableMechanismActions)


def _freemove(self):
    """Menu of free move mode."""
    free_move_mode_menu = QMenu(self)
    
    def freeMoveMode_func(j: int, qicon: QIcon):
        
        @pyqtSlot()
        def func():
            self.freemode_button.setIcon(qicon)
            self.MainCanvas.setFreeMove(j)
            self.InputsWidget.variable_stop.click()
        
        return func
    
    for i, (text, icon) in enumerate((
        ("View mode", "freemove_off"),
        ("Translate mode", "freemove_on"),
        ("Rotate mode", "freemove_on"),
        ("Reflect mode", "freemove_on"),
    )):
        action = QAction(
            QIcon(QPixmap(":/icons/{}.png".format(icon))),
            text,
            self
        )
        action.triggered.connect(freeMoveMode_func(i, action.icon()))
        action.setShortcuts([
            QKeySequence("Ctrl+{}".format(i+1)),
            QKeySequence("Shift+{}".format(i+1)),
        ])
        action.setShortcutContext(Qt.WindowShortcut)
        free_move_mode_menu.addAction(action)
    self.freemode_button.setMenu(free_move_mode_menu)


def _options(self):
    """Signal connection for option widgets.
    
    + Spin boxes
    + Combo boxes
    + Check boxes
    """
    #While value change, update the canvas widget.
    self.settings = QSettings('Kmol', 'Pyslvs')
    self.EntitiesPoint.rowSelectionChanged.connect(
        self.MainCanvas.changePointsSelection
    )
    self.ZoomBar.valueChanged.connect(self.MainCanvas.setZoom)
    self.linewidth_option.valueChanged.connect(self.MainCanvas.setLinkWidth)
    self.pathwidth_option.valueChanged.connect(self.MainCanvas.setPathWidth)
    self.fontsize_option.valueChanged.connect(self.MainCanvas.setFontSize)
    self.action_Display_Point_Mark.toggled.connect(
        self.MainCanvas.setPointMark
    )
    self.action_Display_Dimensions.toggled.connect(
        self.MainCanvas.setShowDimension
    )
    self.selectionradius_option.valueChanged.connect(
        self.MainCanvas.setSelectionRadius
    )
    self.linktrans_option.valueChanged.connect(
        self.MainCanvas.setTransparency
    )
    self.marginfactor_option.valueChanged.connect(
        self.MainCanvas.setMarginFactor
    )
    self.jointsize_option.valueChanged.connect(self.MainCanvas.setJointSize)
    self.zoomby_option.currentIndexChanged.connect(self.MainCanvas.setZoomBy)
    self.snap_option.valueChanged.connect(self.MainCanvas.setSnap)
    self.settings_reset.clicked.connect(self.resetOptions)


def _zoom(self):
    """Zoom functions.
    
    + 'zoom to fit' function connections.
    + Zoom text buttons
    """
    self.action_Zoom_to_fit.triggered.connect(
        self.MainCanvas.zoomToFit
    )
    self.ResetCanvas.clicked.connect(self.MainCanvas.zoomToFit)
    
    zoom_menu = QMenu(self)
    
    def zoom_level(level):
        return pyqtSlot()(lambda: self.ZoomBar.setValue(level))
    
    for level in range(
        self.ZoomBar.minimum() - self.ZoomBar.minimum()%100 + 100,
        500 + 1,
        100
    ):
        action = QAction('{}%'.format(level), self)
        action.triggered.connect(zoom_level(level))
        zoom_menu.addAction(action)
    action = QAction("customize", self)
    action.triggered.connect(self.customizeZoom)
    zoom_menu.addAction(action)
    self.zoom_button.setMenu(zoom_menu)


def _context_menu(self):
    """EntitiesPoint context menu
    
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
    """
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
    """EntitiesLink context menu
    
    + Add
    + Edit
    + Copy table data
    + Release / Constrain
    -------
    + Delete
    """
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
    """MainCanvas context menu
    
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
    """
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
