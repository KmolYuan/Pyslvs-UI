# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from .QtModules import *
from .graphics.canvas import DynamicCanvas
from .Ui_custom_table import (
    PointTableWidget,
    LinkTableWidget,
    SelectionLabel
)
from .info.info import VERSION
tr = QCoreApplication.translate

def initCustomWidgets(self):
    #Splitter stretch factor.
    self.MainSplitter.setStretchFactor(0, 2)
    self.MainSplitter.setStretchFactor(1, 5)
    self.ToolPanelSplitter.setStretchFactor(0, 4)
    self.ToolPanelSplitter.setStretchFactor(1, 5)
    self.tools_splitter.setSizes([100, 500])
    #Version text
    self.menuBar.setCornerWidget(QLabel("Version {}.{}.{} ({})".format(*VERSION)))
    #Entiteis tables
    self.Entiteis_Point = PointTableWidget(self.Entiteis_Point_Widget)
    self.Entiteis_Point.cellDoubleClicked.connect(self.on_action_Edit_Point_triggered)
    self.Entiteis_Point.itemSelectionChanged.connect(self.pointSelection)
    self.Entiteis_Point.deleteRequest.connect(self.on_action_Delete_Point_triggered)
    self.Entiteis_Point_Layout.addWidget(self.Entiteis_Point)
    self.Entiteis_Link = LinkTableWidget(self.Entiteis_Link_Widget)
    self.Entiteis_Link.cellDoubleClicked.connect(self.on_action_Edit_Linkage_triggered)
    self.Entiteis_Link.dragIn.connect(self.addLinkGroup)
    self.Entiteis_Link.deleteRequest.connect(self.on_action_Delete_Linkage_triggered)
    self.Entiteis_Link_Layout.addWidget(self.Entiteis_Link)
    #QPainter canvas window
    self.DynamicCanvasView = DynamicCanvas(self)
    self.DynamicCanvasView.mouse_getSelection.connect(self.Entiteis_Point.setSelections)
    self.DynamicCanvasView.mouse_noSelection.connect(self.Entiteis_Point.clearSelection)
    cleanAction = QAction("Clean selection", self)
    cleanAction.triggered.connect(self.Entiteis_Point.clearSelection)
    cleanAction.setShortcut(Qt.Key_Escape)
    cleanAction.setShortcutContext(Qt.WindowShortcut)
    self.addAction(cleanAction)
    self.DynamicCanvasView.mouse_getDoubleClickAdd.connect(self.addPointGroup)
    self.DynamicCanvasView.mouse_getDoubleClickEdit.connect(self.on_action_Edit_Point_triggered)
    self.DynamicCanvasView.zoom_change.connect(self.setZoomBar)
    self.canvasSplitter.insertWidget(0, self.DynamicCanvasView)
    self.canvasSplitter.setSizes([600, 10, 30])
    #Panel widget will hide when not using.
    self.panelWidget.hide()
    #Console dock will hide when startup.
    self.ConsoleWidget.hide()
    #Connect to GUI button switching.
    self.disconnectConsoleButton.setEnabled(not self.args.debug_mode)
    self.connectConsoleButton.setEnabled(self.args.debug_mode)
    #Properties button on the Point tab widget.
    propertiesButton = QPushButton()
    propertiesButton.setIcon(self.action_Property.icon())
    propertiesButton.setToolTip('Properties')
    propertiesButton.setStatusTip("Properties of this workbook.")
    propertiesButton.clicked.connect(self.on_action_Property_triggered)
    self.PointTab.setCornerWidget(propertiesButton)
    #PMKS button on the broswer bar.
    self.OutputToPMKS.clicked.connect(self.on_action_Output_to_PMKS_triggered)
    #Close all panels button on the panel tab widget.
    closeAllPanelButton = QPushButton()
    closeAllPanelButton.setIcon(QIcon(QPixmap(":/icons/close.png")))
    closeAllPanelButton.setToolTip("Close all opened panel.")
    closeAllPanelButton.clicked.connect(self.closeAllPanels)
    self.panelWidget.setCornerWidget(closeAllPanelButton)
    #Selection label on status bar right side.
    selectionLabel = SelectionLabel(self)
    self.Entiteis_Point.rowSelectionChanged.connect(selectionLabel.updateSelectPoint)
    self.statusBar.addPermanentWidget(selectionLabel)
    #While value change, update the canvas widget.
    self.ZoomBar.valueChanged.connect(self.DynamicCanvasView.setZoom)
    self.LineWidth.valueChanged.connect(self.DynamicCanvasView.setLinkWidth)
    self.PathWidth.valueChanged.connect(self.DynamicCanvasView.setPathWidth)
    self.Font_size.valueChanged.connect(self.DynamicCanvasView.setFontSize)
    self.rotateAngle.valueChanged.connect(self.DynamicCanvasView.setRotateAngle)
    self.action_Display_Point_Mark.toggled.connect(self.DynamicCanvasView.setPointMark)
    self.action_Display_Dimensions.toggled.connect(self.DynamicCanvasView.setShowDimension)
    '''
    Entiteis_Point context menu
    
    + Add
    + Edit
    + Fixed
    + Copy table data
    -------
    + Delete
    '''
    self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
    self.popMenu_point = QMenu(self)
    self.action_point_right_click_menu_add = QAction("&Add", self)
    self.action_point_right_click_menu_add.triggered.connect(self.on_action_New_Point_triggered)
    self.popMenu_point.addAction(self.action_point_right_click_menu_add)
    self.action_point_right_click_menu_edit = QAction("&Edit", self)
    self.action_point_right_click_menu_edit.triggered.connect(self.on_action_Edit_Point_triggered)
    self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
    self.action_point_right_click_menu_lock = QAction("&Fixed", self)
    self.action_point_right_click_menu_lock.setCheckable(True)
    self.action_point_right_click_menu_lock.triggered.connect(self.lockPoint)
    self.popMenu_point.addAction(self.action_point_right_click_menu_lock)
    self.action_point_right_click_menu_copydata = QAction("&Copy table data", self)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copydata)
    self.action_point_right_click_menu_copyPoint = QAction("Copy point", self)
    self.action_point_right_click_menu_copyPoint.triggered.connect(self.copyPoint)
    self.popMenu_point.addAction(self.action_point_right_click_menu_copyPoint)
    self.popMenu_point.addSeparator()
    self.action_point_right_click_menu_delete = QAction("&Delete", self)
    self.action_point_right_click_menu_delete.triggered.connect(self.on_action_Delete_Point_triggered)
    self.popMenu_point.addAction(self.action_point_right_click_menu_delete)
    '''
    Entiteis_Link context menu
    
    + Add
    + Edit
    + Copy table data
    -------
    + Delete
    '''
    self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
    self.popMenu_link = QMenu(self)
    self.action_link_right_click_menu_add = QAction("&Add", self)
    self.action_link_right_click_menu_add.triggered.connect(self.on_action_New_Line_triggered)
    self.popMenu_link.addAction(self.action_link_right_click_menu_add)
    self.action_link_right_click_menu_edit = QAction("&Edit", self)
    self.action_link_right_click_menu_edit.triggered.connect(self.on_action_Edit_Linkage_triggered)
    self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
    self.action_link_right_click_menu_copydata = QAction("&Copy table data", self)
    self.popMenu_link.addAction(self.action_link_right_click_menu_copydata)
    self.popMenu_link.addSeparator()
    self.action_link_right_click_menu_delete = QAction("&Delete", self)
    self.action_link_right_click_menu_delete.triggered.connect(self.on_action_Delete_Linkage_triggered)
    self.popMenu_link.addAction(self.action_link_right_click_menu_delete)
    '''
    DynamicCanvasView context menu
    
    + Add a Path Point [Path Solving]
    + Add
    + Add [fixed]
    -------
    + Edit
    + Fixed
    + Copy point
    -------
    + Delete
    '''
    self.DynamicCanvasView.setContextMenuPolicy(Qt.CustomContextMenu)
    self.DynamicCanvasView.customContextMenuRequested.connect(self.on_painter_context_menu)
    self.popMenu_painter = QMenu(self)
    self.action_painter_right_click_menu_path = QAction("Add a Path Point [Path Solving]", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_path)
    self.action_painter_right_click_menu_add = QAction("&Add", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_add)
    self.action_painter_right_click_menu_fix_add = QAction("Add [fixed]", self)
    self.popMenu_painter.addAction(self.action_painter_right_click_menu_fix_add)
    self.popMenu_painter.addSeparator()
    self.popMenu_painter.addAction(self.action_point_right_click_menu_edit)
    self.popMenu_painter.addAction(self.action_point_right_click_menu_lock)
    self.popMenu_painter.addAction(self.action_point_right_click_menu_copyPoint)
    self.popMenu_painter.addSeparator()
    self.popMenu_painter.addAction(self.action_point_right_click_menu_delete)
    self.DynamicCanvasView.mouse_track.connect(self.context_menu_mouse_pos)

def action_Enabled(self):
    ONE_POINT = self.Entiteis_Point.rowCount()>0
    ONE_LINK = self.Entiteis_Link.rowCount()>1
    #Edit
    self.action_Edit_Point.setEnabled(ONE_POINT)
    self.action_Edit_Linkage.setEnabled(ONE_LINK)
    #Delete
    self.action_Delete_Point.setEnabled(ONE_POINT)
    self.action_Delete_Linkage.setEnabled(ONE_LINK)
    self.action_point_right_click_menu_delete.setEnabled(ONE_POINT)
    self.action_link_right_click_menu_delete.setEnabled(ONE_LINK)
    #Others
    self.action_Output_to_Solvespace.setEnabled(ONE_LINK)
    self.action_DXF_2D_models.setEnabled(ONE_LINK)
    self.action_Batch_moving.setEnabled(ONE_POINT)

def showUndoWindow(self, FileState):
    self.undoView = QUndoView(FileState)
    self.undoView.setEmptyLabel("~ Start Pyslvs")
    self.UndoRedoLayout.addWidget(self.undoView)
    separator = QAction(self)
    separator.setSeparator(True)
    self.menu_Edit.insertAction(self.action_Batch_moving, separator)
    self.action_Redo = FileState.createRedoAction(self, 'Redo')
    self.action_Undo = FileState.createUndoAction(self, 'Undo')
    self.action_Redo.setShortcut("Ctrl+Shift+Z")
    self.action_Redo.setStatusTip("Backtracking undo action.")
    self.action_Redo.setIcon(QIcon(QPixmap(":/icons/redo.png")))
    self.action_Undo.setShortcut("Ctrl+Z")
    self.action_Undo.setStatusTip("Recover last action.")
    self.action_Undo.setIcon(QIcon(QPixmap(":/icons/undo.png")))
    self.menu_Edit.insertAction(separator, self.action_Undo)
    self.menu_Edit.insertAction(separator, self.action_Redo)
