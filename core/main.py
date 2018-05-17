# -*- coding: utf-8 -*-

"""This module contains the declaration of main window.

+ class MainWindow:
    
    + Events and Overridden method.
    + Solver method.
    + Actions method.
    + IO method.
    + Entities method.
    + Storage method.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from networkx import Graph
from typing import (
    Tuple,
    List,
    Dict,
    Union,
    Optional,
)
from argparse import Namespace
from core.QtModules import (
    Qt,
    pyqtSlot,
    QMainWindow,
    QUndoStack,
    QFileInfo,
    QStandardPaths,
    QPoint,
    QMessageBox,
    QInputDialog,
    QTextCursor,
    QListWidgetItem,
)
from core.io import XStream, strbetween
from core.widgets import initCustomWidgets
from core.main_method import (
    _solver,
    _actions,
    _io,
    _entities,
    _storage,
)
from core.libs import VPoint
from .Ui_main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    
    """The main window of Pyslvs.
    
    Inherited from QMainWindow.
    Exit with QApplication.
    
    The main window is so much method that was been split it
    into wrapper function as 'widgets.custom_xxx' module.
    """
    
    def __init__(self, args: Namespace):
        """Notes:
        
        + Input command line arguments object from Python parser.
        + Command line arguments excluding any Qt startup option.
        + Start main window with no parent.
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.args = args
        self.env = ""
        
        self.setLocate(
            QFileInfo(self.args.i).canonicalFilePath() if self.args.i else
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )
        
        #Console widget.
        self.consoleerror_option.setChecked(self.args.w)
        if not self.args.debug_mode:
            self.on_connectConsoleButton_clicked()
        
        #Undo stack streem.
        self.CommandStack = QUndoStack(self)
        
        #Initialize custom UI.
        initCustomWidgets(self)
        self.restoreSettings()
        self.resolve()
        
        #Load workbook from argument.
        _io.readFromArgs(self)
    
    def show(self):
        """Overridden function to zoom the canvas's size after startup."""
        super(MainWindow, self).show()
        self.MainCanvas.zoomToFit()
    
    def setLocate(self, locate: str):
        """Set environment variables."""
        if locate == self.env:
            return
        self.env = locate
        print("~Set workplace to: [\"{}\"]".format(self.env))
    
    def dragEnterEvent(self, event):
        _io.dragEnterEvent(self, event)
    
    def dropEvent(self, event):
        _io.dropEvent(self, event)
    
    def closeEvent(self, event):
        """Close event to avoid user close the window accidentally."""
        if self.checkFileChanged():
            event.ignore()
            return
        if self.InputsWidget.inputs_playShaft.isActive():
            self.InputsWidget.inputs_playShaft.stop()
        self.saveSettings()
        XStream.back()
        self.setAttribute(Qt.WA_DeleteOnClose)
        print("Exit.")
        event.accept()
    
    @pyqtSlot(int)
    def commandReload(self, index: int):
        """The time of withdrawal and redo action."""
        if index != self.FileWidget.Stack:
            self.workbookNoSave()
        else:
            self.workbookSaved()
        self.EntitiesPoint.clearSelection()
        self.InputsWidget.variableReload()
        self.resolve()
    
    @pyqtSlot()
    def resolve(self):
        _solver.resolve(self)
    
    def getGraph(self) -> List[Tuple[int, int]]:
        return _solver.getGraph(self)
    
    def getCollection(self) -> Dict[str, Union[
        Dict[str, None], #Driver
        Dict[str, None], #Follower
        Dict[str, List[Tuple[float, float]]], #Target
        str, #Link_Expression
        str, #Expression
        Tuple[Tuple[int, int]], #Graph
        Dict[int, Tuple[float, float]], #pos
        Dict[str, int], #cus
        Dict[int, int] #same
    ]]:
        return _solver.getCollection(self)
    
    def getTriangle(self,
        vpoints: Optional[Tuple[VPoint]] = None
    ) -> List[Tuple[str]]:
        return _solver.getTriangle(self, vpoints)
    
    def rightInput(self) -> bool:
        return _solver.rightInput(self)
    
    def pathInterval(self) -> float:
        return _solver.pathInterval(self)
    
    def reloadCanvas(self):
        _solver.reloadCanvas(self)
    
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value: int):
        """Reset the text when zoom bar changed."""
        self.zoom_button.setText('{}%'.format(value))
    
    @pyqtSlot()
    def customizeZoom(self):
        """Customize zoom value."""
        value, ok = QInputDialog.getInt(self,
            "Zoom",
            "Enter a zoom value:",
            self.ZoomBar.minimum(),
            self.ZoomBar.value(),
            self.ZoomBar.maximum(),
            10
        )
        if ok:
            self.ZoomBar.setValue(value)
    
    @pyqtSlot(bool)
    def on_action_Display_Dimensions_toggled(self, toggled: bool):
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_Display_Point_Mark.setChecked(True)
    
    @pyqtSlot(bool)
    def on_action_Display_Point_Mark_toggled(self, toggled: bool):
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_Display_Dimensions.setChecked(False)
    
    @pyqtSlot()
    def on_action_Path_style_triggered(self):
        """Set path style as curve (true) or dots (false)."""
        self.MainCanvas.setCurveMode(self.action_Path_style.isChecked())
    
    @pyqtSlot(int)
    def on_SynthesisTab_currentChanged(self, index: int):
        """Dimensional synthesis information will show on the canvas."""
        self.MainCanvas.setShowTargetPath(
            self.SynthesisTab.tabText(index)=="Dimensional"
        )
    
    def addTargetPoint(self):
        """Use context menu to add a target path coordinate."""
        self.DimensionalSynthesis.addPoint(self.mouse_pos_x, self.mouse_pos_y)
    
    @pyqtSlot(int, tuple)
    def mergeResult(self, row: int, path: Tuple[Tuple[float, float]]):
        """Merge result function of dimensional synthesis."""
        Result = self.DimensionalSynthesis.mechanism_data[row]
        #exp_symbol = ['A', 'B', 'C', 'D', 'E']
        exp_symbol = []
        for exp in Result['Link_Expression'].split(';'):
            for name in strbetween(exp, '[', ']').split(','):
                if name not in exp_symbol:
                    exp_symbol.append(name)
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Dimensional Synthesis}"
        )
        tmp_dict = {}
        for tag in sorted(exp_symbol):
            tmp_dict[tag] = self.addPoint(
                Result[tag][0],
                Result[tag][1],
                color=("Dark-Orange" if (tag in Result['Target']) else None)
            )
        for i, exp in enumerate(Result['Link_Expression'].split(';')):
            self.addNormalLink(
                tmp_dict[name]
                for name in strbetween(exp, '[', ']').split(',')
            )
            if i == 0:
                self.constrainLink(self.EntitiesLink.rowCount()-1)
        self.CommandStack.endMacro()
        #Add the path.
        i = 0
        while "Algorithm_{}".format(i) in self.InputsWidget.pathData:
            i += 1
        self.InputsWidget.addPath("Algorithm_{}".format(i), path)
        self.MainCanvas.zoomToFit()
    
    @pyqtSlot()
    def on_connectConsoleButton_clicked(self):
        """Turn the OS command line (stdout) log to console."""
        print("Connect to GUI console.")
        XStream.stdout().messageWritten.connect(self.__appendToConsole)
        XStream.stderr().messageWritten.connect(self.__appendToConsole)
        self.connectConsoleButton.setEnabled(False)
        self.disconnectConsoleButton.setEnabled(True)
        print("Connect to GUI console.")
    
    @pyqtSlot()
    def on_disconnectConsoleButton_clicked(self):
        """Turn the console log to OS command line (stdout)."""
        print("Disconnect from GUI console.")
        XStream.back()
        self.connectConsoleButton.setEnabled(True)
        self.disconnectConsoleButton.setEnabled(False)
        print("Disconnect from GUI console.")
    
    @pyqtSlot(str)
    def __appendToConsole(self, log):
        """After inserted the text, move cursor to end."""
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
        self.consoleWidgetBrowser.insertPlainText(log)
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
    
    @pyqtSlot(bool)
    def on_action_Full_Screen_toggled(self, fullscreen):
        """Show fullscreen or not."""
        if fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()
    
    @pyqtSlot(int)
    def on_EntitiesTab_currentChanged(self, index: int):
        self.MainCanvas.setSolutionShow(
            self.EntitiesTab.tabText(index) == "Formulas"
        )
    
    @pyqtSlot(float, float)
    def setMousePos(self, x: float, y: float):
        _actions.setMousePos(self, x, y)
    
    @pyqtSlot(QPoint)
    def on_point_context_menu(self, point: QPoint):
        _actions.on_point_context_menu(self, point)
    
    @pyqtSlot(QPoint)
    def on_link_context_menu(self, point: QPoint):
        _actions.on_link_context_menu(self, point)
    
    @pyqtSlot(QPoint)
    def on_canvas_context_menu(self, point: QPoint):
        _actions.on_canvas_context_menu(self, point)
    
    @pyqtSlot()
    def enableMechanismActions(self):
        _actions.enableMechanismActions(self)
    
    @pyqtSlot()
    def copyPointsTable(self):
        _actions.copyPointsTable(self)
    
    @pyqtSlot()
    def copyLinksTable(self):
        _actions.copyLinksTable(self)
    
    def copyCoord(self):
        _actions.copyCoord(self)
    
    def restoreSettings(self):
        _io.restoreSettings(self)
    
    def saveSettings(self):
        _io.saveSettings(self)
    
    def resetOptions(self):
        _io.resetOptions(self)
    
    def workbookNoSave(self):
        _io.workbookNoSave(self)
    
    def workbookSaved(self):
        _io.workbookSaved(self)
    
    def checkFileChanged(self) -> bool:
        return _io.checkFileChanged(self)
    
    @pyqtSlot()
    def on_windowTitle_fullpath_clicked(self):
        _io.on_windowTitle_fullpath_clicked(self)
    
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        _io.on_action_Get_Help_triggered(self)
    
    @pyqtSlot()
    def on_action_Pyslvs_com_triggered(self):
        _io.on_action_Pyslvs_com_triggered(self)
    
    @pyqtSlot()
    def on_action_github_repository_triggered(self):
        _io.on_action_github_repository_triggered(self)
    
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        _io.on_action_About_Pyslvs_triggered(self)
    
    @pyqtSlot()
    def on_action_About_Qt_triggered(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)
    
    @pyqtSlot()
    def on_action_Console_triggered(self):
        _io.on_action_Console_triggered(self)
    
    @pyqtSlot()
    def on_action_Example_triggered(self):
        _io.on_action_Example_triggered(self)
    
    @pyqtSlot()
    def on_action_Import_Example_triggered(self):
        _io.on_action_Import_Example_triggered(self)
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        _io.on_action_New_Workbook_triggered(self)
    
    def clear(self):
        _io.clear(self)
    
    @pyqtSlot()
    def on_action_Import_PMKS_server_triggered(self):
        _io.on_action_Import_PMKS_server_triggered(self)
    
    def parseExpression(self, expr: str):
        _io.parseExpression(self, expr)
    
    def addEmptyLinkGroup(self, linkcolor: Dict[str, str]):
        _io.addEmptyLinkGroup(self, linkcolor)
    
    @pyqtSlot()
    def on_action_Load_File_triggered(self):
        _io.on_action_Load_File_triggered(self)
    
    @pyqtSlot()
    def on_action_Import_Workbook_triggered(self):
        _io.on_action_Import_Workbook_triggered(self)
    
    @pyqtSlot()
    def on_action_Save_triggered(self, isBranch: bool = False):
        _io.on_action_Save_triggered(self, isBranch)
    
    @pyqtSlot()
    def on_action_Save_as_triggered(self, isBranch: bool = False):
        _io.on_action_Save_as_triggered(self, isBranch)
    
    @pyqtSlot()
    def on_action_Save_branch_triggered(self):
        _io.on_action_Save_branch_triggered(self)
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        _io.on_action_Output_to_Solvespace_triggered(self)
    
    @pyqtSlot()
    def on_action_Output_to_DXF_triggered(self):
        _io.on_action_Output_to_DXF_triggered(self)
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        _io.on_action_Output_to_Picture_triggered(self)
    
    def outputTo(self, formatName: str, formatChoose: List[str]) -> str:
        return _io.outputTo(self, formatName, formatChoose)
    
    def saveReplyBox(self, title: str, file_name: str):
        _io.saveReplyBox(self, title, file_name)
    
    def inputFrom(self,
        formatName: str,
        formatChoose: List[str],
        multiple: bool = False
    ) -> str:
        return _io.inputFrom(self, formatName, formatChoose, multiple)
    
    @pyqtSlot()
    def on_action_Output_to_PMKS_triggered(self):
        _io.on_action_Output_to_PMKS_triggered(self)
    
    @pyqtSlot()
    def on_action_Output_to_Picture_clipboard_triggered(self):
        _io.on_action_Output_to_Picture_clipboard_triggered(self)
    
    @pyqtSlot()
    def on_action_See_Expression_triggered(self):
        _io.on_action_See_Expression_triggered(self)
    
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        _io.on_action_See_Python_Scripts_triggered(self)
    
    @pyqtSlot()
    def on_action_Check_update_triggered(self):
        _io.on_action_Check_update_triggered(self)
    
    @pyqtSlot()
    def qAddNormalPoint(self):
        _entities.qAddNormalPoint(self)
    
    def addNormalPoint(self):
        _entities.addNormalPoint(self)
    
    def addFixedPoint(self):
        _entities.addFixedPoint(self)
    
    def addPoint(self,
        x: float,
        y: float,
        fixed: bool = False,
        color: str = None
    ) -> int:
        return _entities.addPoint(self, x, y, fixed, color)
    
    def addPointsByGraph(self,
        G: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: int
    ):
        _entities.addPointsByGraph(self, G, pos, ground_link)
    
    @pyqtSlot(list)
    def addNormalLink(self, points: List[int]):
        _entities.addNormalLink(self, points)
    
    def addLink(self, name: str, color: str, points: Tuple[int] = ()):
        _entities.addLink(self, name, color, points)
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        _entities.on_action_New_Point_triggered(self)
    
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self):
        _entities.on_action_Edit_Point_triggered(self)
    
    def lockPoints(self):
        _entities.lockPoints(self)
    
    def clonePoint(self):
        _entities.clonePoint(self)
    
    @pyqtSlot(tuple)
    def setFreemoved(self,
        coordinates: Tuple[Tuple[int, Tuple[float, float]]]
    ):
        _entities.setFreemoved(self, coordinates)
    
    def setCoordsAsCurrent(self):
        _entities.setCoordsAsCurrent(self)
    
    @pyqtSlot()
    def on_action_New_Link_triggered(self):
        _entities.on_action_New_Link_triggered(self)
    
    @pyqtSlot()
    def on_action_Edit_Link_triggered(self):
        _entities.on_action_Edit_Link_triggered(self)
    
    @pyqtSlot()
    def releaseGround(self):
        _entities.releaseGround(self)
    
    @pyqtSlot()
    def constrainLink(self, row: int = None):
        _entities.constrainLink(self, row)
    
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self):
        _entities.on_action_Delete_Point_triggered(self)
    
    @pyqtSlot()
    def on_action_Delete_Link_triggered(self):
        _entities.on_action_Delete_Link_triggered(self)
    
    @pyqtSlot()
    def on_mechanism_storage_add_clicked(self):
        _storage.on_mechanism_storage_add_clicked(self)
    
    @pyqtSlot()
    def on_mechanism_storage_copy_clicked(self):
        _storage.on_mechanism_storage_copy_clicked(self)
    
    @pyqtSlot()
    def on_mechanism_storage_paste_clicked(self):
        _storage.on_mechanism_storage_paste_clicked(self)
    
    @pyqtSlot()
    def on_mechanism_storage_delete_clicked(self):
        _storage.on_mechanism_storage_delete_clicked(self)
    
    @pyqtSlot(QListWidgetItem)
    def on_mechanism_storage_itemDoubleClicked(self, item):
        _storage.on_mechanism_storage_itemDoubleClicked(self, item)
    
    @pyqtSlot()
    def on_mechanism_storage_restore_clicked(self, item: QListWidgetItem = None):
        _storage.on_mechanism_storage_restore_clicked(self, item)
    
    def loadStorage(self, exprs: Tuple[Tuple[str, str]]):
        _storage.loadStorage(self, exprs)
