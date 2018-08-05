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

from typing import (
    Tuple,
    List,
    Dict,
    Any,
    Union,
    Optional,
)
from argparse import Namespace
from networkx import Graph
from core.QtModules import (
    pyqtSlot,
    Qt,
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
from core.io import XStream, strbetween, QTIMAGES
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
    to wrapper function in 'main_method' module.
    """
    
    def __init__(self, args: Namespace):
        """Notes:
        
        + Input command line arguments object from Python parser.
        + Command line arguments excluding any Qt startup option.
        + Start main window with no parent.
        """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.args = args
        self.env = ""
        self.DOF = 0
        self.autopreview = []
        
        self.setLocate(
            QFileInfo(self.args.i).canonicalFilePath()
            if self.args.i else
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )
        
        #Undo stack streem.
        self.CommandStack = QUndoStack(self)
        
        #Initialize custom UI.
        initCustomWidgets(self)
        self.restoreSettings()
        
        #Console widget.
        self.consoleerror_option.setChecked(self.args.debug_mode)
        if not self.args.debug_mode:
            self.__consoleConnect()
        
        #Start first solve function calling.
        self.solve()
        
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
        self.solve()

    def solve(self):
        _solver.solve(self)
    
    @pyqtSlot()
    def resolve(self):
        _solver.resolve(self)
    
    def previewpath(self, autopreview: List[Any], vpoints: Tuple[VPoint]):
        _solver.previewpath(self, autopreview, vpoints)
    
    def getGraph(self) -> List[Tuple[int, int]]:
        return _solver.getGraph(self)
    
    def getCollection(self) -> Dict[str, Union[
        Dict[str, None], #Driver
        Dict[str, None], #Follower
        Dict[str, List[Tuple[float, float]]], #Target
        str, #Link_expr
        str, #Expression
        Tuple[Tuple[int, int]], #Graph
        Dict[int, Tuple[float, float]], #pos
        Dict[str, int], #cus
        Dict[int, int] #same
    ]]:
        return _solver.getCollection(self)
    
    def getTriangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str]]:
        return _solver.getTriangle(self, vpoints)
    
    def rightInput(self) -> bool:
        return _solver.rightInput(self)
    
    def reloadCanvas(self):
        _solver.reloadCanvas(self)
    
    @pyqtSlot(int, name='on_ZoomBar_valueChanged')
    def setZoom(self, value: int):
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
    
    @pyqtSlot(bool, name='on_action_Display_Dimensions_toggled')
    def __setShowDimensions(self, toggled: bool):
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_Display_Point_Mark.setChecked(True)
    
    @pyqtSlot(bool, name='on_action_Display_Point_Mark_toggled')
    def __setShowPointMark(self, toggled: bool):
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_Display_Dimensions.setChecked(False)
    
    @pyqtSlot(name='on_action_Path_style_triggered')
    def __setCurveMode(self):
        """Set path style as curve (true) or dots (false)."""
        self.MainCanvas.setCurveMode(self.action_Path_style.isChecked())
    
    @pyqtSlot(int, name='on_SynthesisTab_currentChanged')
    def __setShowTargetPath(self, index: int):
        """Dimensional synthesis information will show on the canvas."""
        self.MainCanvas.setShowTargetPath(index == 2)
    
    def addTargetPoint(self):
        """Use context menu to add a target path coordinate."""
        self.DimensionalSynthesis.addPoint(self.mouse_pos_x, self.mouse_pos_y)
    
    @pyqtSlot(int, tuple)
    def mergeResult(self, row: int, path: Tuple[Tuple[float, float]]):
        """Merge result function of dimensional synthesis."""
        result = self.DimensionalSynthesis.mechanismData(row)
        #exp_symbol = ['A', 'B', 'C', 'D', 'E']
        exp_symbol = []
        for exp in result['Link_expr'].split(';'):
            for name in strbetween(exp, '[', ']').split(','):
                if name not in exp_symbol:
                    exp_symbol.append(name)
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Dimensional Synthesis}"
        )
        tmp_dict = {}
        for tag in sorted(exp_symbol):
            tmp_dict[tag] = self.addPoint(
                result[tag][0],
                result[tag][1],
                color=("Dark-Orange" if (tag in result['Target']) else None)
            )
        for i, exp in enumerate(result['Link_expr'].split(';')):
            self.addNormalLink(
                tmp_dict[name]
                for name in strbetween(exp, '[', ']').split(',')
            )
            if i == 0:
                self.constrainLink(self.EntitiesLink.rowCount()-1)
        self.CommandStack.endMacro()
        #Add the path.
        i = 0
        while "Algorithm_{}".format(i) in self.InputsWidget.pathData():
            i += 1
        self.InputsWidget.addPath("Algorithm_{}".format(i), path)
        self.MainCanvas.zoomToFit()
    
    @pyqtSlot(int, name='on_EntitiesTab_currentChanged')
    def __setSelectionMode(self, index: int):
        """Connect selection signal for main canvas."""
        #Set selection from click table items.
        tables = (self.EntitiesPoint, self.EntitiesLink, self.EntitiesExpr)
        try:
            for table in tables:
                table.rowSelectionChanged.disconnect()
        except TypeError:
            pass
        tables[index].rowSelectionChanged.connect(self.MainCanvas.setSelection)
        #Double click signal.
        try:
            self.MainCanvas.doubleclick_edit.disconnect()
        except TypeError:
            pass
        if index == 0:
            self.MainCanvas.doubleclick_edit.connect(self.editPoint)
        elif index == 1:
            self.MainCanvas.doubleclick_edit.connect(self.editLink)
        #Clear all selections.
        for table in tables:
            table.clearSelection()
        self.InputsWidget.clearSelection()
    
    @pyqtSlot(name='on_background_choosedir_clicked')
    def __setBackground(self):
        """Show up dialog to set the background file path."""
        file_name = self.inputFrom("Background", QTIMAGES)
        if file_name:
            self.background_option.setText(file_name)
    
    @pyqtSlot(name='on_console_connect_button_clicked')
    def __consoleConnect(self):
        """Turn the OS command line (stdout) log to console."""
        print("Connect to GUI console.")
        XStream.stdout().messageWritten.connect(self.__append_to_console)
        XStream.stderr().messageWritten.connect(self.__append_to_console)
        self.console_connect_button.setEnabled(False)
        self.console_disconnect_button.setEnabled(True)
        print("Connect to GUI console.")
    
    @pyqtSlot(name='on_console_disconnect_button_clicked')
    def __consoleDisconnect(self):
        """Turn the console log to OS command line (stdout)."""
        print("Disconnect from GUI console.")
        XStream.back()
        self.console_connect_button.setEnabled(True)
        self.console_disconnect_button.setEnabled(False)
        print("Disconnect from GUI console.")
    
    @pyqtSlot(str)
    def __append_to_console(self, log: str):
        """After inserted the text, move cursor to end."""
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
        self.consoleWidgetBrowser.insertPlainText(log)
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
    
    @pyqtSlot(bool, name='on_action_Full_Screen_toggled')
    def __fullScreen(self, fullscreen: bool):
        """Show fullscreen or not."""
        if fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()
    
    @pyqtSlot(float, float)
    def setMousePos(self, x: float, y: float):
        _actions.setMousePos(self, x, y)
    
    @pyqtSlot(QPoint)
    def point_context_menu(self, point: QPoint):
        _actions.point_context_menu(self, point)
    
    @pyqtSlot(QPoint)
    def link_context_menu(self, point: QPoint):
        _actions.link_context_menu(self, point)
    
    @pyqtSlot(QPoint)
    def canvas_context_menu(self, point: QPoint):
        _actions.canvas_context_menu(self, point)
    
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
    
    @pyqtSlot(name='on_windowTitle_fullpath_clicked')
    def setWindowTitleFullpath(self):
        _io.setWindowTitleFullpath(self)
    
    @pyqtSlot(name='on_action_Get_Help_triggered')
    def __showHelp(self):
        _io.showHelp(self)
    
    @pyqtSlot(name='on_action_Pyslvs_com_triggered')
    def __showDotCOM(self):
        _io.showDotCOM(self)
    
    @pyqtSlot(name='on_action_github_repository_triggered')
    def __showGithub(self):
        _io.showGithub(self)
    
    @pyqtSlot(name='on_action_About_Pyslvs_triggered')
    def __about(self):
        _io.about(self)
    
    @pyqtSlot(name='on_action_About_Qt_triggered')
    def aboutQt(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)
    
    @pyqtSlot(name='on_action_Console_triggered')
    def __showConsole(self):
        _io.showConsole(self)
    
    @pyqtSlot(name='on_action_Example_triggered')
    def __loadExample(self):
        _io.loadExample(self)
    
    @pyqtSlot(name='on_action_Import_Example_triggered')
    def __importExample(self):
        _io.importExample(self)
    
    @pyqtSlot(name='on_action_New_Workbook_triggered')
    def __newWorkbook(self):
        _io.newWorkbook(self)
    
    def clear(self):
        _io.clear(self)
    
    @pyqtSlot(name='on_action_Import_PMKS_server_triggered')
    def __importPmksURL(self):
        _io.importPmksURL(self)
    
    def parseExpression(self, expr: str):
        _io.parseExpression(self, expr)
    
    def addEmptyLinks(self, linkcolor: Dict[str, str]):
        _io.addEmptyLinks(self, linkcolor)
    
    @pyqtSlot(name='on_action_Load_File_triggered')
    def loadFile(self):
        _io.loadFile(self)
    
    @pyqtSlot(name='on_action_Import_Workbook_triggered')
    def importWorkbook(self):
        _io.importWorkbook(self)
    
    @pyqtSlot(name='on_action_Save_triggered')
    def save(self, isBranch: bool = False):
        _io.save(self, isBranch)
    
    @pyqtSlot(name='on_action_Save_as_triggered')
    def saveAs(self, isBranch: bool = False):
        _io.saveAs(self, isBranch)
    
    @pyqtSlot(name='on_action_Save_branch_triggered')
    def saveBranch(self):
        """Save as new branch action."""
        self.save(True)
    
    @pyqtSlot(name='on_action_Output_to_Solvespace_triggered')
    def __saveSlvs(self):
        _io.saveSlvs(self)
    
    @pyqtSlot(name='on_action_Output_to_DXF_triggered')
    def __saveDXF(self):
        _io.saveDXF(self)
    
    @pyqtSlot(name='on_action_Output_to_Picture_triggered')
    def __savePicture(self):
        _io.savePicture(self)
    
    @pyqtSlot(name='on_action_Output_to_Picture_clipboard_triggered')
    def __savePictureClipboard(self):
        _io.savePictureClipboard(self)
    
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
    
    @pyqtSlot(name='on_action_Output_to_PMKS_triggered')
    def __savePMKS(self):
        _io.savePMKS(self)
    
    @pyqtSlot(name='on_action_See_expr_triggered')
    def showExpr(self):
        _io.showExpr(self)
    
    @pyqtSlot(name='on_action_See_Python_Scripts_triggered')
    def __showPyScript(self):
        _io.showPyScript(self)
    
    @pyqtSlot(name='on_action_Check_update_triggered')
    def __checkUpdate(self):
        _io.checkUpdate(self)
    
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
        graph: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: int
    ):
        _entities.addPointsByGraph(self, graph, pos, ground_link)
    
    @pyqtSlot(list)
    def addNormalLink(self, points: List[int]):
        _entities.addNormalLink(self, points)
    
    def addLink(self, name: str, color: str, points: Tuple[int] = ()):
        _entities.addLink(self, name, color, points)
    
    @pyqtSlot(name='on_action_New_Point_triggered')
    def newPoint(self):
        _entities.newPoint(self)
    
    @pyqtSlot(name='on_action_Edit_Point_triggered')
    def editPoint(self):
        _entities.editPoint(self)
    
    def lockPoints(self):
        _entities.lockPoints(self)
    
    def clonePoint(self):
        _entities.clonePoint(self)
    
    @pyqtSlot(tuple)
    def setFreemove(self, coords: Tuple[Tuple[int, Tuple[float, float, float]]]):
        _entities.setFreemove(self, coords)
    
    @pyqtSlot(bool)
    def setLinkFreemove(self, enable: bool):
        _entities.setLinkFreemove(self, enable)
    
    @pyqtSlot(int)
    def adjustLink(self, value: int):
        _entities.adjustLink(self, value)
    
    def setCoordsAsCurrent(self):
        _entities.setCoordsAsCurrent(self)
    
    @pyqtSlot(name='on_action_New_Link_triggered')
    def newLink(self):
        _entities.newLink(self)
    
    @pyqtSlot(name='on_action_Edit_Link_triggered')
    def editLink(self):
        _entities.editLink(self)
    
    @pyqtSlot()
    def releaseGround(self):
        _entities.releaseGround(self)
    
    @pyqtSlot()
    def constrainLink(self, row1: Optional[int] = None, row2: int = 0):
        _entities.constrainLink(self, row1, row2)
    
    @pyqtSlot(name='on_action_Delete_Point_triggered')
    def deletePoint(self):
        _entities.deletePoint(self)
    
    @pyqtSlot(name='on_action_Delete_Link_triggered')
    def deleteLink(self):
        _entities.deleteLink(self)
    
    @pyqtSlot(name='on_mechanism_storage_add_clicked')
    def __addStorage(self):
        _storage.addStorage(self)
    
    @pyqtSlot(name='on_mechanism_storage_copy_clicked')
    def __copyStorage(self):
        _storage.copyStorage(self)
    
    @pyqtSlot(name='on_mechanism_storage_paste_clicked')
    def __pasteStorage(self):
        _storage.pasteStorage(self)
    
    @pyqtSlot(name='on_mechanism_storage_delete_clicked')
    def __deleteStorage(self):
        _storage.deleteStorage(self)
    
    @pyqtSlot(QListWidgetItem, name='on_mechanism_storage_itemDoubleClicked')
    def __doubleClickStorage(self, item):
        """Restore the storage data as below."""
        self.__restoreStorage(item)
    
    @pyqtSlot(name='on_mechanism_storage_restore_clicked')
    def __restoreStorage(self, item: QListWidgetItem = None):
        _storage.restoreStorage(self, item)
    
    def getStorage(self) -> Tuple[Tuple[str, str]]:
        return _storage.getStorage(self)
    
    def addStorages(self, exprs: Tuple[Tuple[str, str]]):
        _storage.addStorages(self, exprs)
