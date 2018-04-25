# -*- coding: utf-8 -*-

"""This module contain all the functions we needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from networkx import Graph
from typing import (
    Tuple,
    List,
)
from argparse import Namespace
from core.QtModules import (
    QMainWindow,
    QUndoStack,
    QFileInfo,
    QStandardPaths,
    pyqtSlot,
    QPoint,
    QAction,
    QApplication,
    Qt,
    QMessageBox,
    QInputDialog,
    QTextCursor,
)
from core.graphics import edges_view
from core.io import (
    XStream,
    from_parenthesis,
)
from core.widgets import (
    CustomizeFunc,
    IOFunc,
    EntitiesCmds,
    StorageFunc,
)
from core.libs import (
    slvsProcess,
    SlvsException,
    vpoints_configure,
    VPoint,
)
from .Ui_main import Ui_MainWindow


class MainWindow(
    QMainWindow,
    Ui_MainWindow,
    CustomizeFunc,
    IOFunc,
    EntitiesCmds,
    StorageFunc,
):
    
    """The main window of Pyslvs.
    
    Inherited from QMainWindow.
    Exit with QApplication.
    """
    
    def __init__(self, args: Namespace, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.args = args
        self.env = ""
        #Console widget.
        self.showConsoleError.setChecked(self.args.w)
        if not self.args.debug_mode:
            self.on_connectConsoleButton_clicked()
        #Undo Stack
        self.CommandStack = QUndoStack()
        self.setLocate(
            QFileInfo(self.args.i).canonicalFilePath() if self.args.i else
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )
        #Initialize custom UI.
        self.initCustomWidgets()
        self.resolve()
        #Expression & DOF value.
        self.DOF = 0
        #Load workbook from argument.
        if self.args.r:
            self.FileWidget.read(self.args.r)
    
    def show(self):
        """Overrided function.
        
        Adjust the canvas size after display.
        """
        super(MainWindow, self).show()
        self.DynamicCanvasView.zoomToFit()
        self.DimensionalSynthesis.updateRange()
    
    def setLocate(self, locate: str):
        """Set environment variables."""
        if locate == self.env:
            return
        self.env = locate
        print("~Set workplace to: [\"{}\"]".format(self.env))
    
    def dragEnterEvent(self, event):
        """Drag file in to our window."""
        mimeData = event.mimeData()
        if not mimeData.hasUrls():
            return
        for url in mimeData.urls():
            file_name = url.toLocalFile()
            if QFileInfo(file_name).suffix() in ('pyslvs', 'db'):
                event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Drop file in to our window."""
        file_name = event.mimeData().urls()[-1].toLocalFile()
        self.FileWidget.read(file_name)
        event.acceptProposedAction()
    
    @pyqtSlot(float, float)
    def setMousePos(self, x, y):
        """Mouse position on canvas."""
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    
    @pyqtSlot(QPoint)
    def on_point_context_menu(self, point):
        """Entities_Point context menu."""
        self.__enablePointContext()
        self.popMenu_point.exec_(self.Entities_Point_Widget.mapToGlobal(point))
        self.action_New_Link.setVisible(True)
        self.popMenu_point_merge.clear()
    
    @pyqtSlot(QPoint)
    def on_link_context_menu(self, point):
        """Entities_Link context menu."""
        self.__enableLinkContext()
        self.popMenu_link.exec_(self.Entities_Link_Widget.mapToGlobal(point))
    
    @pyqtSlot(QPoint)
    def on_canvas_context_menu(self, point):
        """DynamicCanvasView context menu."""
        self.__enablePointContext()
        tabText = self.SynthesisTab.tabText(self.SynthesisTab.currentIndex())
        self.action_canvas_context_path.setVisible(tabText == "Dimensional")
        self.popMenu_canvas.exec_(self.DynamicCanvasView.mapToGlobal(point))
        self.action_New_Link.setVisible(True)
        self.popMenu_point_merge.clear()
    
    def __enablePointContext(self):
        """Adjust the status of QActions.
        
        What ever we have least one point or not,
        need to enable / disable QAction.
        """
        selectedRows = self.Entities_Point.selectedRows()
        selectionCount = len(selectedRows)
        row = self.Entities_Point.currentRow()
        #If connecting with the ground.
        if selectionCount:
            self.action_point_context_lock.setChecked(all(
                'ground' in self.Entities_Point.item(row, 1).text()
                for row in self.Entities_Point.selectedRows()
            ))
        #If no any points selected.
        for action in (
            self.action_point_context_add,
            self.action_canvas_context_add,
            self.action_canvas_context_fix_add,
        ):
            action.setVisible(selectionCount <= 0)
        self.action_point_context_lock.setVisible(row > -1)
        self.action_point_context_delete.setVisible(row > -1)
        #If a point selected.
        for action in (
            self.action_point_context_edit,
            self.action_point_context_copyPoint,
            self.action_point_context_copydata,
            self.action_point_context_copyCoord,
        ):
            action.setVisible(row > -1)
            action.setEnabled(selectionCount == 1)
        #If two or more points selected.
        self.action_New_Link.setVisible(selectionCount > 1)
        self.popMenu_point_merge.menuAction().setVisible(selectionCount > 1)
        
        def mjFunc(i):
            """Generate a merge function."""
            return lambda: self.__toMultipleJoint(i, selectedRows)
        
        for i, p in enumerate(selectedRows):
            action = QAction("Base on Point{}".format(p), self)
            action.triggered.connect(mjFunc(i))
            self.popMenu_point_merge.addAction(action)
    
    def __enableLinkContext(self):
        """Enable / disable link's QAction, same as point table."""
        selectionCount = len(self.Entities_Link.selectedRows())
        row = self.Entities_Link.currentRow()
        self.action_link_context_add.setVisible(selectionCount <= 0)
        selected_one = selectionCount == 1
        self.action_link_context_edit.setEnabled((row > -1) and selected_one)
        self.action_link_context_delete.setEnabled((row > 0) and selected_one)
        self.action_link_context_copydata.setEnabled((row > -1) and selected_one)
        self.action_link_context_release.setVisible((row == 0) and selected_one)
        self.action_link_context_constrain.setVisible((row > 0) and selected_one)
    
    @pyqtSlot()
    def enableMechanismActions(self):
        """Enable / disable 'mechanism' menu."""
        pointSelection = self.Entities_Point.selectedRows()
        linkSelection = self.Entities_Link.selectedRows()
        ONE_POINT = len(pointSelection) == 1
        ONE_LINK = len(linkSelection) == 1
        POINT_SELECTED = bool(pointSelection)
        LINK_SELECTED = (
            bool(linkSelection) and
            (0 not in linkSelection) and
            (not ONE_LINK)
        )
        #Edit
        self.action_Edit_Point.setEnabled(ONE_POINT)
        self.action_Edit_Link.setEnabled(ONE_LINK)
        #Delete
        self.action_Delete_Point.setEnabled(POINT_SELECTED)
        self.action_Delete_Link.setEnabled(LINK_SELECTED)
    
    @pyqtSlot()
    def copyPointsTable(self):
        """Copy text from point table."""
        self.__copyTableData(self.Entities_Point)
    
    @pyqtSlot()
    def copyLinksTable(self):
        """Copy text from link table."""
        self.__copyTableData(self.Entities_Link)
    
    def __copyTableData(self, table):
        """Copy item text to clipboard."""
        text = table.currentItem().text()
        if text:
            QApplication.clipboard().setText(text)
    
    def copyCoord(self):
        """Copy the current coordinate of the point."""
        pos = self.Entities_Point.currentPosition(self.Entities_Point.currentRow())
        text = str(pos[0] if (len(pos) == 1) else pos)
        QApplication.clipboard().setText(text)
    
    def closeEvent(self, event):
        """Close event to avoid user close the window accidentally."""
        if self.checkFileChanged():
            event.ignore()
            return
        if self.InputsWidget.inputs_playShaft.isActive():
            self.InputsWidget.inputs_playShaft.stop()
        XStream.back()
        self.setAttribute(Qt.WA_DeleteOnClose)
        print("Exit.")
        event.accept()
    
    def checkFileChanged(self) -> bool:
        """If the user has not saved the change.
        
        Return True if user want to "discard" the operation.
        """
        if not self.FileWidget.changed:
            return False
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?\nAny changes won't be saved.",
            (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel),
            QMessageBox.Save
        )
        if reply == QMessageBox.Save:
            self.on_action_Save_triggered()
            return self.FileWidget.changed
        elif reply == QMessageBox.Discard:
            return False
        return True
    
    @pyqtSlot(int)
    def commandReload(self, index):
        """The time of withdrawal and redo action."""
        if index != self.FileWidget.Stack:
            self.workbookNoSave()
        else:
            self.workbookSaved()
        self.InputsWidget.variableReload()
        self.resolve()
    
    def resolve(self):
        """Resolve: Use Solvespace lib."""
        inputs = list(self.InputsWidget.getInputsVariables())
        try:
            result, DOF = slvsProcess(
                self.Entities_Point.data(),
                self.Entities_Link.data(),
                inputs if not self.FreeMoveMode.isChecked() else ()
            )
        except SlvsException as e:
            if self.showConsoleError.isChecked():
                print(e)
            self.ConflictGuide.setToolTip(str(e))
            self.ConflictGuide.setStatusTip("Error: {}".format(e))
            self.ConflictGuide.setVisible(True)
            self.DOFview.setVisible(False)
        else:
            self.Entities_Point.updateCurrentPosition(result)
            self.DOF = DOF
            self.DOFview.setText("{} ({})".format(self.DOF, len(inputs)))
            self.ConflictGuide.setVisible(False)
            self.DOFview.setVisible(True)
        self.reloadCanvas()
    
    def getGraph(self) -> List[Tuple[int, int]]:
        """Return edges data for NetworkX graph class.
        
        + VLinks will become graph nodes.
        """
        joint_data = self.Entities_Point.data()
        link_data = self.Entities_Link.data()
        G = Graph()
        #links name for RP joint.
        k = len(link_data)
        used_point = set()
        for i, vlink in enumerate(link_data):
            for p in vlink.points:
                if p in used_point:
                    continue
                for m, vlink_ in enumerate(link_data):
                    if not ((i != m) and (p in vlink_.points)):
                        continue
                    if joint_data[p].type != 2:
                        G.add_edge(i, m)
                        continue
                    G.add_edge(i, k)
                    G.add_edge(k, m)
                    k += 1
                used_point.add(p)
        return [edge for n, edge in edges_view(G)]
    
    def getTriangle(self, vpoints: Tuple[VPoint]) -> List[Tuple[str]]:
        """Update triangle expression here.
        
        Special function for VPoints.
        """
        exprs = vpoints_configure(
            vpoints,
            tuple(self.InputsWidget.inputPair())
        )
        self.Entities_Expr.setExpr(exprs)
        return exprs
    
    def rightInput(self) -> bool:
        """Is input same as DOF?"""
        inputs = (self.InputsWidget.inputCount() != 0) and (self.DOF == 0)
        if not inputs:
            self.Entities_Expr.clear()
        return inputs
    
    def pathInterval(self) -> float:
        """Wrapper use to get path interval."""
        return self.InputsWidget.record_interval.value()
    
    def reloadCanvas(self):
        """Update main canvas data, without resolving."""
        self.DynamicCanvasView.updateFigure(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self.InputsWidget.currentPath()
        )
    
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value: int):
        """Reset the text when zoom bar changed."""
        self.ZoomText.setText('{}%'.format(value))
    
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
    def on_action_Display_Dimensions_toggled(self, toggled):
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_Display_Point_Mark.setChecked(True)
    
    @pyqtSlot(bool)
    def on_action_Display_Point_Mark_toggled(self, toggled):
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_Display_Dimensions.setChecked(False)
    
    @pyqtSlot()
    def on_action_Path_style_triggered(self):
        """Set path style as curve (true) or dots (false)."""
        self.DynamicCanvasView.setCurveMode(self.action_Path_style.isChecked())
    
    @pyqtSlot(int)
    def on_SynthesisTab_currentChanged(self, index):
        """Dimensional synthesis information will show on the canvas."""
        self.DynamicCanvasView.setShowTargetPath(
            self.SynthesisTab.tabText(index)=="Dimensional"
        )
    
    def addTargetPoint(self):
        """Use context menu to add a target path coordinate."""
        self.DimensionalSynthesis.addPoint(self.mouse_pos_x, self.mouse_pos_y)
    
    @pyqtSlot(int, tuple)
    def mergeResult(self, row, path):
        """Merge result function of dimensional synthesis."""
        Result = self.DimensionalSynthesis.mechanism_data[row]
        #exp_symbol = ['A', 'B', 'C', 'D', 'E']
        exp_symbol = []
        for exp in Result['Link_Expression'].split(';'):
            for name in from_parenthesis(exp, '[', ']').split(','):
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
                for name in from_parenthesis(exp, '[', ']').split(',')
            )
            if i == 0:
                self.constrainLink(self.Entities_Link.rowCount()-1)
        self.CommandStack.endMacro()
        #Add the path.
        i = 0
        while "Algorithm_path_{}".format(i) in self.InputsWidget.pathData:
            i += 1
        self.InputsWidget.addPath("Algorithm_path_{}".format(i), path)
        self.DynamicCanvasView.zoomToFit()
    
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
