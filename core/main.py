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
    Dict,
)
from itertools import chain
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
    AddTable,
    DeleteTable,
    FixSequenceNumber,
    EditPointTable,
    EditLinkTable,
    XStream,
    from_parenthesis,
)
from core.widgets import (
    CustomizeFunc,
    StorageFunc,
    IOFunc,
)
from core.entities import (
    EditPointDialog,
    EditLinkDialog,
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
    StorageFunc
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
        """Overloaded function.
        
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
            fileName = url.toLocalFile()
            if QFileInfo(fileName).suffix() in ('pyslvs', 'db'):
                event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Drop file in to our window."""
        fileName = event.mimeData().urls()[-1].toLocalFile()
        self.FileWidget.read(fileName)
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
        ONE_POINT = len(pointSelection)==1
        ONE_LINK = len(linkSelection)==1
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
    
    @pyqtSlot()
    def qAddNormalPoint(self):
        """Add point group using alt key."""
        tabText = self.SynthesisTab.tabText(self.SynthesisTab.currentIndex())
        if tabText == "Dimensional":
            self.addTargetPoint()
        else:
            self.__addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    def addNormalPoint(self):
        """Add a point (not fixed)."""
        self.__addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    def addFixedPoint(self):
        """Add a point (fixed)."""
        self.__addPoint(self.mouse_pos_x, self.mouse_pos_y, True)
    
    def __addPoint(self,
        x: float,
        y: float,
        fixed: bool =False,
        color: str =None
    ) -> int:
        """Add an ordinary point.
        Return the row count of new point.
        """
        rowCount = self.Entities_Point.rowCount()
        if fixed:
            links = 'ground'
            if color is None:
                color = 'Blue'
        else:
            links = ''
            if color is None:
                color = 'Green'
        self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
        self.CommandStack.push(AddTable(self.Entities_Point))
        self.CommandStack.push(EditPointTable(
            rowCount,
            self.Entities_Point,
            self.Entities_Link,
            [links, 'R', color, x, y]
        ))
        self.CommandStack.endMacro()
        return rowCount
    
    def addPointsByGraph(self,
        G: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: int
    ):
        """Add points by networkx graph and position dict."""
        base_count = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Number and Type Synthesis}"
        )
        for i in range(len(pos)):
            self.__addPoint(*pos[i])
        for link in G.nodes:
            self.addLink(self.__getLinkSerialNumber(), 'Blue', [
                base_count + n
                for n, edge in edges_view(G) if (link in edge)
            ])
            if link == ground_link:
                ground = self.Entities_Link.rowCount()-1
        self.CommandStack.endMacro()
        if ground_link is not None:
            self.constrainLink(ground)
    
    @pyqtSlot(list)
    def __addNormalLink(self, points):
        """Add a link."""
        self.addLink(self.__getLinkSerialNumber(), 'Blue', points)
    
    def addLink(self, name, color, points=()):
        """Push a new link command to stack."""
        linkArgs = [name, color, ','.join('Point{}'.format(i) for i in points)]
        self.CommandStack.beginMacro("Add {{Link: {}}}".format(name))
        self.CommandStack.push(AddTable(self.Entities_Link))
        self.CommandStack.push(EditLinkTable(
            self.Entities_Link.rowCount() - 1,
            self.Entities_Link,
            self.Entities_Point,
            linkArgs
        ))
        self.CommandStack.endMacro()
    
    def __getLinkSerialNumber(self) -> str:
        """Return a new serial number name of link."""
        names = [
            self.Entities_Link.item(row, 0).text()
            for row in range(self.Entities_Link.rowCount())
        ]
        i = 1
        while "link_{}".format(i) in names:
            i += 1
        return "link_{}".format(i)
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        """Create a point with arguments."""
        self.__editPoint()
    
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self):
        """Edit a point with arguments."""
        row = self.Entities_Point.currentRow()
        self.__editPoint(row if (row > -1) else 0)
    
    def __editPoint(self, row: int = False):
        """Edit point function."""
        dlg = EditPointDialog(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        rowCount = self.Entities_Point.rowCount()
        Type = dlg.Type.currentText().split()[0]
        if Type!='R':
            Type += ":{}".format(dlg.Angle.value()%360)
        args = [
            ','.join(
                dlg.selected.item(link).text()
                for link in range(dlg.selected.count())
            ),
            Type,
            dlg.Color.currentText(),
            dlg.X_coordinate.value(),
            dlg.Y_coordinate.value()
        ]
        if row is False:
            self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
            self.CommandStack.push(AddTable(self.Entities_Point))
            row = rowCount
        else:
            row = dlg.Point.currentIndex()
            self.CommandStack.beginMacro("Edit {{Point{}}}".format(rowCount))
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        self.CommandStack.endMacro()
    
    def lockPoint(self):
        """Turn a group of points to fixed on ground or not."""
        toFixed = self.action_point_context_lock.isChecked()
        for row in self.Entities_Point.selectedRows():
            newLinks = self.Entities_Point.item(row, 1).text().split(',')
            if toFixed:
                if 'ground' not in newLinks:
                    newLinks.append('ground')
            else:
                if 'ground' in newLinks:
                    newLinks.remove('ground')
            args = self.Entities_Point.rowTexts(row)
            args[0] = ','.join(s for s in newLinks if s)
            self.CommandStack.beginMacro("Edit {{Point{}}}".format(row))
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
            self.CommandStack.endMacro()
    
    def __toMultipleJoint(self, index: int, points: Tuple[int]):
        """Merge points into a multiple joint.
        
        @index: The index of main joint in the sequence.
        """
        row = points[index]
        self.CommandStack.beginMacro(
            "Merge {{{}}} as multiple joint {{{}}}".format(
                ", ".join('Point{}'.format(p) for p in points),
                'Point{}'.format(row)
            )
        )
        points_data = self.Entities_Point.data()
        for i, p in enumerate(points):
            if i == index:
                continue
            newLinks = points_data[row].links
            for l in points_data[p].links:
                #Add new links.
                if l not in newLinks:
                    newLinks.append(l)
            args = self.Entities_Point.rowTexts(row)
            args[0] = ','.join(newLinks)
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
            self.__deletePoint(p)
        self.CommandStack.endMacro()
    
    def clonePoint(self):
        """Clone a point (with orange color)."""
        row = self.Entities_Point.currentRow()
        args = self.Entities_Point.rowTexts(row)
        args[2] = 'Orange'
        rowCount = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Clone {{Point{}}} as {{Point{}}}".format(row, rowCount)
        )
        self.CommandStack.push(AddTable(self.Entities_Point))
        self.CommandStack.push(EditPointTable(
            rowCount,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot(tuple)
    def setFreemoved(self, coordinates):
        """Free move function."""
        self.CommandStack.beginMacro("Moved {{{}}}".format(", ".join(
            "Point{}".format(c[0]) for c in coordinates
        )))
        for row, (x, y) in coordinates:
            args = self.Entities_Point.rowTexts(row)
            args[3] = x
            args[4] = y
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                args
            ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_New_Link_triggered(self):
        """Create a link with arguments.
        
        + Last than one point:
            
            - Create a new link
        
        + Search method:
            
            - Find the intersection between points that was
                including any link.
            - Add the points that is not in the intersection
                to the link.
        
        + If no, just create a new link by selected points.
        """
        rows = self.Entities_Point.selectedRows()
        if not len(rows) > 1:
            self.__editLink()
            return
        links_all = list(chain(*(
            self.Entities_Point.getLinks(row) for row in rows
        )))
        count_0 = False
        for p in set(links_all):
            if links_all.count(p) > 1:
                count_0 = True
                break
        if (not links_all) or (not count_0):
            self.__addNormalLink(rows)
            return
        name = max(set(links_all), key=links_all.count)
        row = self.Entities_Link.findName(name)
        self.CommandStack.beginMacro("Edit {{Link: {}}}".format(name))
        args = self.Entities_Link.rowTexts(row, hasName=True)
        points = set(self.Entities_Link.getPoints(row))
        points.update(rows)
        args[2] = ','.join('Point{}'.format(p) for p in points)
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Edit_Link_triggered(self):
        """Edit a link with arguments."""
        self.__editLink(self.Entities_Link.currentRow())
    
    def __editLink(self, row=False):
        """Edit link function."""
        dlg = EditLinkDialog(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        name = dlg.name_edit.text()
        args = [
            name,
            dlg.Color.currentText(),
            ','.join(
                dlg.selected.item(point).text()
                for point in range(dlg.selected.count())
            )
        ]
        if row is False:
            self.CommandStack.beginMacro("Add {{Link: {}}}".format(name))
            self.CommandStack.push(AddTable(self.Entities_Link))
            row = self.Entities_Link.rowCount()-1
        else:
            row = dlg.Link.currentIndex()
            self.CommandStack.beginMacro("Edit {{Link: {}}}".format(name))
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def releaseGround(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__getLinkSerialNumber()
        args = [name, 'Blue', self.Entities_Link.item(0, 2).text()]
        self.CommandStack.beginMacro(
            "Release ground to {{Link: {}}}".format(name)
        )
        #Free all points.
        self.CommandStack.push(EditLinkTable(
            0,
            self.Entities_Link,
            self.Entities_Point,
            ['ground', 'White', '']
        ))
        #Create new link.
        self.CommandStack.push(AddTable(self.Entities_Link))
        self.CommandStack.push(EditLinkTable(
            self.Entities_Link.rowCount() - 1,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def constrainLink(self, row=None):
        """Turn a link to ground, then delete this link."""
        if row is None:
            row = self.Entities_Link.currentRow()
        name = self.Entities_Link.item(row, 0).text()
        linkArgs = [
            self.Entities_Link.item(row, 0).text(),
            self.Entities_Link.item(row, 1).text(),
            ''
        ]
        newPoints = sorted(
            set(self.Entities_Link.item(0, 2).text().split(',')) |
            set(self.Entities_Link.item(row, 2).text().split(','))
        )
        groundArgs = ['ground', 'White', ','.join(e for e in newPoints if e)]
        self.CommandStack.beginMacro(
            "Constrain {{Link: {}}} to ground".format(name)
        )
        #Turn to ground.
        self.CommandStack.push(EditLinkTable(
            0,
            self.Entities_Link,
            self.Entities_Point,
            groundArgs
        ))
        #Free all points and delete the link.
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            linkArgs
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Link,
            isRename=False
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self):
        """Delete the selected points.
        Be sure that the points will has new position after deleted.
        """
        selections = self.Entities_Point.selectedRows()
        for i, p in enumerate(selections):
            if p > selections[i-1]:
                row = p-i
            else:
                row = p
            self.__deletePoint(row)
    
    def __deletePoint(self, row: int):
        """Push delete point command to stack."""
        args = self.Entities_Point.rowTexts(row)
        args[0] = ''
        self.CommandStack.beginMacro("Delete {{Point{}}}".format(row))
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            args
        ))
        for i in range(self.Entities_Link.rowCount()):
            self.CommandStack.push(FixSequenceNumber(
                self.Entities_Link,
                i,
                row
            ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Point,
            isRename=True
        ))
        self.InputsWidget.variableExcluding(row)
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Link_triggered(self):
        """Delete the selected links.
        Be sure that the links will has new position after deleted.
        """
        selections = self.Entities_Link.selectedRows()
        selections = tuple(
            p - i + int(0 in selections) if p>selections[i-1] else p
            for i, p in enumerate(selections)
        )
        for row in selections:
            self.__deleteLink(row)
    
    def __deleteLink(self, row: int):
        """Push delete link command to stack.
        
        Remove link will not remove the points.
        """
        if not row > 0:
            return
        args = self.Entities_Link.rowTexts(row, hasName=True)
        args[2] = ''
        self.CommandStack.beginMacro("Delete {{Link: {}}}".format(
            self.Entities_Link.item(row, 0).text()
        ))
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            args
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.Entities_Link,
            isRename=False
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_Output_to_Picture_clipboard_triggered(self):
        """Capture the canvas image to clipboard."""
        QApplication.clipboard().setPixmap(self.DynamicCanvasView.grab())
        QMessageBox.information(self,
            "Captured!",
            "Canvas widget picture is copy to clipboard."
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
            tmp_dict[tag] = self.__addPoint(
                Result[tag][0],
                Result[tag][1],
                color=("Dark-Orange" if (tag in Result['Target']) else None)
            )
        for i, exp in enumerate(Result['Link_Expression'].split(';')):
            self.__addNormalLink(
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
