# -*- coding: utf-8 -*-

"""This module contain all the functions we needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

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
    QDesktopServices,
    QUrl,
    QInputDialog,
    QFileDialog,
    QListWidgetItem,
    QTextCursor,
    QProgressDialog,
)
from core.info import PyslvsAbout, check_update
from core.graphics import (
    slvsProcess,
    SlvsException,
    edges_view,
)
from core.io import (
    Script_Dialog,
    AddTable, DeleteTable, FixSequenceNumber,
    EditPointTable, EditLinkTable,
    AddStorage, DeleteStorage,
    AddStorageName, ClearStorageName,
    Qt_images,
    slvs2D,
    dxfSketch,
    XStream,
    PMKS_parser,
    PMKSArgsTransformer,
    get_from_parenthesis,
)
from core.widgets import initCustomWidgets
from core.entities import EditPoint_show, EditLink_show
from core.libs import vpoints_configure, VPoint
from typing import (
    Tuple,
    List,
    Dict,
)
from networkx import Graph
from .Ui_main import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    
    """The main window of Pyslvs.
    
    Inherited from QMainWindow.
    Exit with QApplication.
    """
    
    def __init__(self, args, parent=None):
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
        self.__setLocate(
            QFileInfo(self.args.i).canonicalFilePath() if self.args.i else
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        )
        #Initialize custom UI.
        initCustomWidgets(self)
        self.resolve()
        #Expression & DOF value.
        self.vpoints_old = ()
        self.exprs_old = ()
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
    
    def __setLocate(self, locate: str):
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
            fixed = all(
                'ground' in self.Entities_Point.item(row, 1).text()
                for row in self.Entities_Point.selectedRows()
            )
            self.action_point_context_lock.setChecked(fixed)
        #If no any points selected.
        for action in (
            self.action_point_context_add,
            self.action_canvas_context_add,
            self.action_canvas_context_fix_add
        ):
            action.setVisible(selectionCount<=0)
        self.action_point_context_lock.setVisible(row>-1)
        self.action_point_context_delete.setVisible(row>-1)
        #If a point selected.
        for action in (
            self.action_point_context_edit,
            self.action_point_context_copyPoint,
            self.action_point_context_copydata
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
    
    def closeEvent(self, event):
        """Close event to avoid user close the window accidentally."""
        if self.__checkFileChanged():
            event.ignore()
            return
        if self.InputsWidget.inputs_playShaft.isActive():
            self.InputsWidget.inputs_playShaft.stop()
        XStream.back()
        self.setAttribute(Qt.WA_DeleteOnClose)
        print("Exit.")
        event.accept()
    
    def __checkFileChanged(self) -> bool:
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
        #Links name for RP joint.
        k = len(link_data)
        used_point = set()
        for i, vlink in enumerate(link_data):
            for p in vlink.points:
                if p in used_point:
                    continue
                match = [
                    m for m, vlink_ in enumerate(link_data)
                    if (i != m) and (p in vlink_.points)
                ]
                for m in match:
                    if joint_data[p].type==2:
                        G.add_edge(i, k)
                        G.add_edge(k, m)
                        k += 1
                    else:
                        G.add_edge(i, m)
                used_point.add(p)
        return [edge for n, edge in edges_view(G)]
    
    def getTriangle(self, vpoints: Tuple[VPoint]) -> List[Tuple[str]]:
        """Update triangle expression here.
        
        Special function for VPoints.
        """
        if self.vpoints_old == vpoints:
            return self.exprs_old
        self.vpoints_old = vpoints
        self.exprs_old = vpoints_configure(
            vpoints,
            tuple(self.InputsWidget.inputPair())
        )
        self.Entities_Expr.setExpr(self.exprs_old)
        return self.exprs_old
    
    def rightInput(self) -> bool:
        """Is input same as DOF?"""
        return (self.InputsWidget.inputCount() != 0) and (self.DOF == 0)
    
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
    
    def v_to_slvs(self) -> Tuple[Tuple[int, int]]:
        """Solvespace edges."""
        for vlink in self.Entities_Link.data():
            if vlink.name=='ground':
                continue
            for i, p in enumerate(vlink.points):
                if i==0:
                    continue
                yield (vlink.points[0], p)
                if i>1:
                    yield (vlink.points[i-1], p)
    
    def workbookNoSave(self):
        """Workbook not saved signal."""
        self.FileWidget.changed = True
        not_yet_saved = " (not yet saved)"
        self.setWindowTitle(
            self.windowTitle().replace(not_yet_saved, '') +
            not_yet_saved
        )
    
    def workbookSaved(self):
        """Workbook saved signal."""
        self.FileWidget.changed = False
        self.on_windowTitle_fullpath_clicked()
    
    @pyqtSlot()
    def on_windowTitle_fullpath_clicked(self):
        """Set the option 'window title will show the fullpath'."""
        fileName = self.FileWidget.fileName
        self.setWindowTitle("Pyslvs - {}".format(
            fileName.absoluteFilePath()
            if self.windowTitle_fullpath.isChecked()
            else fileName.fileName()
        ) + (" (not yet saved)" if self.FileWidget.changed else ''))
    
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        """Open website: http://mde.tw"""
        self.__openURL("http://mde.tw")
    
    @pyqtSlot()
    def on_action_Pyslvs_com_triggered(self):
        """Open website: http://www.pyslvs.com/blog/index.html"""
        self.__openURL("http://www.pyslvs.com/blog/index.html")
    
    @pyqtSlot()
    def on_action_github_repository_triggered(self):
        """Open website: Github repository."""
        self.__openURL("https://github.com/KmolYuan/Pyslvs-PyQt5")
    
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        """Open Pyslvs about."""
        about = PyslvsAbout(self)
        about.show()
    
    @pyqtSlot()
    def on_action_About_Qt_triggered(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)
    
    def __openURL(self, URL):
        """Use to open link."""
        QDesktopServices.openUrl(QUrl(URL))
    
    @pyqtSlot()
    def on_action_Console_triggered(self):
        """Open GUI console."""
        self.OptionTab.setCurrentIndex(2)
        self.History_tab.setCurrentIndex(1)
    
    @pyqtSlot()
    def on_action_Example_triggered(self):
        """Load examples from 'FileWidget'.
        Return true if successed.
        """
        if self.FileWidget.loadExample():
            self.DynamicCanvasView.zoomToFit()
    
    @pyqtSlot()
    def on_action_Import_Example_triggered(self):
        """Import a example and merge it to canvas."""
        self.FileWidget.loadExample(isImport=True)
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        """Create (Clean) a new workbook."""
        if self.__checkFileChanged():
            return
        self.clear()
        self.FileWidget.reset()
        self.FileWidget.closeDatabase()
        print("Created a new workbook.")
    
    def clear(self):
        """Clear to create commit stage."""
        self.mechanism_storage_name_tag.clear()
        self.mechanism_storage.clear()
        self.CollectionTabPage.clear()
        self.NumberAndTypeSynthesis.clear()
        self.InputsWidget.clear()
        self.DimensionalSynthesis.clear()
        self.Entities_Point.clear()
        self.Entities_Link.clear()
        self.resolve()
    
    @pyqtSlot()
    def on_action_Import_PMKS_server_triggered(self):
        """Load PMKS URL and turn it to expression."""
        URL, ok = QInputDialog.getText(self,
            "PMKS URL input",
            "Please input link string:"
        )
        if not ok:
            return
        if not URL:
            QMessageBox.warning(self,
                "Loading failed",
                "Your link is in an incorrect format."
            )
            return
        try:
            textList = list(filter(lambda s: s not in ('', " ", '\n'),
                tuple(filter(
                    lambda s: 'mech=' in s,
                    URL.split('?')[-1].split('&')
                ))[0].replace('mech=', '').split('|')
            ))
            expression = []
            while textList:
                item = textList.pop(0).split(',')[:-1]
                for i, e in enumerate(reversed(item)):
                    if e in ['R', 'P', 'RP']:
                        t = -(i+1)
                        break
                links = item[:t]
                item = item[t:]
                expression.append("J[{}, P[{}], L[{}]]".format(
                    "{}:{}".format(item[0], item[-1]) if item[0]!='R' else 'R',
                    ", ".join((item[1], item[2])),
                    ", ".join(links)
                ))
            expression = "M[{}]".format(", ".join(expression))
        except Exception as e:
            QMessageBox.warning(self,
                "Loading failed",
                "Your link is in an incorrect format."
            )
        else:
            self.parseExpression(expression)
    
    def parseExpression(self, expr):
        """Parse expression."""
        try:
            pointsArgs = PMKSArgsTransformer().transform(PMKS_parser.parse(expr))
        except Exception as e:
            print(e)
            QMessageBox.warning(self,
                "Loading failed",
                "Your expression is in an incorrect format."
            )
        else:
            for pointArgs in pointsArgs:
                linkNames = tuple(
                    vlink.name for vlink in self.Entities_Link.data()
                )
                links = pointArgs[0].split(',')
                for linkName in links:
                    #If link name not exist.
                    if linkName not in linkNames:
                        self.__addLink(linkName, 'Blue')
                rowCount = self.Entities_Point.rowCount()
                self.CommandStack.beginMacro("Add {{Point{}}}".format(rowCount))
                self.CommandStack.push(AddTable(self.Entities_Point))
                self.CommandStack.push(EditPointTable(
                    rowCount,
                    self.Entities_Point,
                    self.Entities_Link, pointArgs
                ))
                self.CommandStack.endMacro()
    
    def AddEmptyLinkGroup(self, linkcolor: Dict[str, str]):
        """Use to add empty link when loading database."""
        for name, color in linkcolor.items():
            if name != 'ground':
                self.__addLink(name, color)
    
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        """Load workbook."""
        if self.__checkFileChanged():
            return
        fileName = self.inputFrom(
            "Workbook database",
            ["Pyslvs workbook (*.pyslvs)"]
        )
        if not fileName:
            return
        self.FileWidget.read(fileName)
        self.DynamicCanvasView.zoomToFit()
    
    @pyqtSlot()
    def on_action_Import_Workbook_triggered(self):
        """Import from workbook."""
        if self.__checkFileChanged():
            return
        fileName = self.inputFrom(
            "Workbook database (Import)",
            ["Pyslvs workbook (*.pyslvs)"]
        )
        if not fileName:
            return
        self.FileWidget.importMechanism(fileName)
    
    @pyqtSlot()
    def on_action_Save_triggered(self, isBranch=False):
        """Save action."""
        fileName = self.FileWidget.fileName.absoluteFilePath()
        if self.FileWidget.fileName.suffix()=='pyslvs':
            self.FileWidget.save(fileName, isBranch)
        else:
            self.on_action_Save_as_triggered(isBranch)
    
    @pyqtSlot()
    def on_action_Save_as_triggered(self, isBranch=False):
        """Save as action."""
        fileName = self.outputTo("workbook", ["Pyslvs workbook (*.pyslvs)"])
        if fileName:
            self.FileWidget.save(fileName, isBranch)
            self.saveReplyBox("Workbook", fileName)
    
    @pyqtSlot()
    def on_action_Save_branch_triggered(self):
        """Save as new branch action."""
        self.on_action_Save_triggered(True)
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        """Solvespace 2d save function."""
        fileName = self.outputTo(
            "Solvespace sketch",
            ["Solvespace module(*.slvs)"]
        )
        if not fileName:
            return
        slvs2D(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self.v_to_slvs,
            fileName
        )
        self.saveReplyBox("Solvespace sketch", fileName)
    
    @pyqtSlot()
    def on_action_Output_to_DXF_triggered(self):
        """DXF 2d save function."""
        fileName = self.outputTo(
            "Drawing Exchange Format",
            ["Drawing Exchange Format(*.dxf)"]
        )
        if not fileName:
            return
        dxfSketch(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self.v_to_slvs,
            fileName
        )
        self.saveReplyBox("Drawing Exchange Format", fileName)
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        """Picture save function."""
        fileName = self.outputTo("picture", Qt_images)
        if not fileName:
            return
        pixmap = self.DynamicCanvasView.grab()
        pixmap.save(fileName, format=QFileInfo(fileName).suffix())
        self.saveReplyBox("Picture", fileName)
    
    def outputTo(self, formatName: str, formatChoose: List[str]):
        """Simple to support mutiple format."""
        suffix0 = get_from_parenthesis(formatChoose[0], '(', ')').split('*')[-1]
        fileName, suffix = QFileDialog.getSaveFileName(
            self,
            "Save to {}...".format(formatName),
            self.env+'/'+self.FileWidget.fileName.baseName()+suffix0,
            ';;'.join(formatChoose)
        )
        if fileName:
            suffix = get_from_parenthesis(suffix, '(', ')').split('*')[-1]
            print("Format: {}".format(suffix))
            if QFileInfo(fileName).suffix()!=suffix[1:]:
                fileName += suffix
            self.__setLocate(QFileInfo(fileName).absolutePath())
        return fileName
    
    def saveReplyBox(self, title: str, fileName: str):
        """Show message when successfully saved."""
        size = QFileInfo(fileName).size()
        print("Size: {}".format(
            "{} MB".format(round(size/1024/1024, 2))
            if size/1024//1024 else "{} KB".format(round(size/1024, 2))
        ))
        QMessageBox.information(self,
            title,
            "Successfully converted:\n{}".format(fileName)
        )
        print("Successful saved: [\"{}\"]".format(fileName))
    
    def inputFrom(self,
        formatName: str,
        formatChoose: List[str],
        multiple=False
    ):
        """Get file name(s)."""
        args = (
            "Open {} file{}...".format(formatName, 's' if multiple else ''),
            self.env,
            ';;'.join(formatChoose)
        )
        if multiple:
            fileName_s, suffix = QFileDialog.getOpenFileNames(self, *args)
        else:
            fileName_s, suffix = QFileDialog.getOpenFileName(self, *args)
        if fileName_s:
            suffix = get_from_parenthesis(suffix, '(', ')').split('*')[-1]
            print("Format: {}".format(suffix))
            if type(fileName_s)==str:
                self.__setLocate(QFileInfo(fileName_s).absolutePath())
            else:
                self.__setLocate(QFileInfo(fileName_s[0]).absolutePath())
        return fileName_s
    
    @pyqtSlot()
    def on_action_Output_to_PMKS_triggered(self):
        """Output to PMKS as URL."""
        url = "http://designengrlab.github.io/PMKS/pmks.html?mech="
        urlTable = []
        for row in range(self.Entities_Point.rowCount()):
            TypeAndAngle = self.Entities_Point.item(row, 2).text().split(':')
            pointData = [
                self.Entities_Point.item(row, 1).text(),
                TypeAndAngle[0],
                self.Entities_Point.item(row, 4).text(),
                self.Entities_Point.item(row, 5).text(),
            ]
            if len(TypeAndAngle)==2:
                pointData.append(TypeAndAngle[1])
            pointData.append('tfff')
            urlTable.append(','.join(pointData))
        url += '|'.join(urlTable)+'|'
        text = '\n'.join([
            "Copy and past this link to web browser:\n",
            url + '\n',
            "If you have installed Microsoft Silverlight in " +
            "Internet Explorer as default browser, " +
            "just click \"Open\" button to open it in PMKS website."
        ])
        reply = QMessageBox.information(self,
            "PMKS web server",
            text,
            (QMessageBox.Save | QMessageBox.Open | QMessageBox.Close),
            QMessageBox.Save
        )
        if reply == QMessageBox.Open:
            self.__openURL(url)
        elif reply == QMessageBox.Save:
            QApplication.clipboard().setText(url)
    
    @pyqtSlot()
    def on_action_Output_to_Expression_triggered(self):
        """Output as expression."""
        data = self.Entities_Point.data()
        expr = "M[{}]".format(", ".join(vpoint.expr for vpoint in data))
        text = (
            "You can copy the expression and import to another workbook:" +
            "\n\n{}\n\nClick the save button to copy it.".format(expr)
        )
        reply = QMessageBox.question(self,
            "Pyslvs Expression",
            text,
            (QMessageBox.Save | QMessageBox.Close),
            QMessageBox.Save
        )
        if reply == QMessageBox.Save:
            QApplication.clipboard().setText(expr)
    
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        """Output to Python script for Jupyter notebook."""
        sd = Script_Dialog(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self
        )
        sd.show()
    
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
    
    def addPointsByGraph(self, G, pos, ground_link: [None, int]):
        """Add points by networkx graph and position dict."""
        base_count = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Number and Type Synthesis}"
        )
        for i in range(len(pos)):
            self.__addPoint(*pos[i])
        for link in G.nodes:
            self.__addLink(self.__getLinkSerialNumber(), 'Blue', [
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
        self.__addLink(self.__getLinkSerialNumber(), 'Blue', points)
    
    def __addLink(self, name, color, points=()):
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
        self.__editPoint(row if row>-1 else 0)
    
    def __editPoint(self, row=False):
        """Edit point function."""
        dlg = EditPoint_show(
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
        Args = [
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
            Args
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
            Args = list(self.Entities_Point.rowTexts(row, True))
            Args[0] = ','.join(filter(lambda a: a!='', newLinks))
            self.CommandStack.beginMacro("Edit {{Point{}}}".format(row))
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                Args
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
        Links = lambda i: list(filter(
            lambda a: a!='',
            self.Entities_Point.item(i, 1).text().split(',')
        ))
        newLinks = Links(row)
        for i, p in enumerate(points):
            if i == index:
                continue
            for l in Links(p):
                if l not in newLinks:
                    newLinks.append(l)
            self.__deletePoint(p)
        Args = list(self.Entities_Point.rowTexts(row, True))
        Args[0] = ','.join(newLinks)
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            Args
        ))
        self.CommandStack.endMacro()
    
    def clonePoint(self):
        """Clone a point (with orange color)."""
        row = self.Entities_Point.currentRow()
        Args = list(self.Entities_Point.rowTexts(row, True))
        Args[2] = 'Orange'
        rowCount = self.Entities_Point.rowCount()
        self.CommandStack.beginMacro(
            "Clone {{Point{}}} as {{Point{}}}".format(row, rowCount)
        )
        self.CommandStack.push(AddTable(self.Entities_Point))
        self.CommandStack.push(EditPointTable(
            rowCount,
            self.Entities_Point,
            self.Entities_Link,
            Args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot(tuple)
    def setFreemoved(self, coordinates):
        """Free move function."""
        self.CommandStack.beginMacro("Moved {{{}}}".format(", ".join(
            "Point{}".format(c[0]) for c in coordinates
        )))
        for row, (x, y) in coordinates:
            Args = list(self.Entities_Point.rowTexts(row, True))
            Args[3] = x
            Args[4] = y
            self.CommandStack.push(EditPointTable(
                row,
                self.Entities_Point,
                self.Entities_Link,
                Args
            ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_action_New_Link_triggered(self):
        """Create a link with arguments."""
        selectedRows = self.Entities_Point.selectedRows()
        if not len(selectedRows)>1:
            self.__editLink()
            return
        #Search to found that there is any point is not idle.
        link_data = self.Entities_Link.data()
        for row, vlink in enumerate(link_data):
            sr_set = set(selectedRows)
            ps_set = set(vlink.points)
            #If link are exist, edit the link.
            if sr_set == ps_set:
                self.__editLink(row)
                return
            #If link has some new point, add the new points to link.
            elif ps_set and (sr_set > ps_set):
                self.CommandStack.beginMacro(
                    "Edit {{Link: {}}}".format(vlink.name)
                )
                for row_, vlink_ in enumerate(link_data):
                    Args = [vlink_.name, vlink_.colorSTR, ','.join(
                        'Point{}'.format(p)
                        for p in vlink_.points if p not in selectedRows
                    )]
                    self.CommandStack.push(EditLinkTable(
                        row_,
                        self.Entities_Link,
                        self.Entities_Point,
                        Args
                    ))
                Args = [vlink.name, vlink.colorSTR, ','.join(
                    'Point{}'.format(p) for p in selectedRows
                )]
                self.CommandStack.push(EditLinkTable(
                    row,
                    self.Entities_Link,
                    self.Entities_Point,
                    Args
                ))
                self.CommandStack.endMacro()
                return
        self.__addNormalLink(selectedRows)
    
    @pyqtSlot()
    def on_action_Edit_Link_triggered(self):
        """Edit a link with arguments."""
        self.__editLink(self.Entities_Link.currentRow())
    
    def __editLink(self, row=False):
        """Edit link function."""
        dlg = EditLink_show(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        name = dlg.name_edit.text()
        Args = [
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
            Args
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def releaseGround(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__getLinkSerialNumber()
        Args = [name, 'Blue', self.Entities_Link.item(0, 2).text()]
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
            Args
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
        Args = list(self.Entities_Point.rowTexts(row, True))
        Args[0] = ''
        self.CommandStack.beginMacro("Delete {{Point{}}}".format(row))
        self.CommandStack.push(EditPointTable(
            row,
            self.Entities_Point,
            self.Entities_Link,
            Args
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
        Args = list(self.Entities_Link.rowTexts(row, True))
        Args[2] = ''
        self.CommandStack.beginMacro("Delete {{Link: {}}}".format(
            self.Entities_Link.item(row, 0).text()
        ))
        self.CommandStack.push(EditLinkTable(
            row,
            self.Entities_Link,
            self.Entities_Point,
            Args
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
            for name in get_from_parenthesis(exp, '[', ']').split(','):
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
                for name in get_from_parenthesis(exp, '[', ']').split(',')
            )
            if i==0:
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
    
    def __clearStorage(self):
        """After saved storage,
        clean all the item of two table widgets.
        """
        self.Entities_Point.clear()
        self.Entities_Link.clear()
        self.InputsWidget.variableExcluding()
    
    @pyqtSlot()
    def on_mechanism_storage_add_clicked(self):
        name = self.mechanism_storage_name_tag.text()
        if not name:
            name = self.mechanism_storage_name_tag.placeholderText()
        self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
        self.__addStorage(name, "M[{}]".format(", ".join(
            vpoint.expr for vpoint in self.Entities_Point.data()
        )))
        self.CommandStack.push(ClearStorageName(
            self.mechanism_storage_name_tag
        ))
        self.CommandStack.endMacro()
    
    @pyqtSlot()
    def on_mechanism_storage_copy_clicked(self):
        """Copy the expression from a storage data."""
        item = self.mechanism_storage.currentItem()
        if item:
            QApplication.clipboard().setText(item.expr)
    
    @pyqtSlot()
    def on_mechanism_storage_paste_clicked(self):
        """Add the storage data from string."""
        expr, ok = QInputDialog.getText(self,
            "Storage",
            "Please input expression:"
        )
        if not ok:
            return
        try:
            #Put the expression into parser to see if it is legal.
            PMKS_parser.parse(expr)
        except:
            QMessageBox.warning(self,
                "Loading failed",
                "Your expression is in an incorrect format."
            )
            return
        name, ok = QInputDialog.getText(self,
            "Storage",
            "Please input name tag:"
        )
        if not ok:
            return
        if not name:
            nameList = [
                self.mechanism_storage.item(i).text()
                for i in range(self.mechanism_storage.count())
            ]
            i = 0
            while "Prototype_{}".format(i) in nameList:
                i += 1
            name = "Prototype_{}".format(i)
        self.__addStorage(name, expr, clear=False)
    
    def __addStorage(self, name, expr, clear=True):
        """Add storage data function."""
        self.CommandStack.beginMacro("Add {{Mechanism: {}}}".format(name))
        if clear:
            self.__clearStorage()
        self.CommandStack.push(AddStorage(
            name,
            self.mechanism_storage,
            expr
        ))
        self.CommandStack.endMacro()
        i = 0
        exprs = []
        for i in range(self.mechanism_storage.count()):
            exprs.append(self.mechanism_storage.item(i).text())
        while "Prototype_{}".format(i) in exprs:
            i += 1
        self.mechanism_storage_name_tag.setPlaceholderText(
            "Prototype_{}".format(i)
        )
    
    @pyqtSlot()
    def on_mechanism_storage_delete_clicked(self):
        """Delete the storage data."""
        row = self.mechanism_storage.currentRow()
        if not row>-1:
            return
        self.CommandStack.beginMacro("Delete {{Mechanism: {}}}".format(
            self.mechanism_storage.item(row).text()
        ))
        self.CommandStack.push(DeleteStorage(row, self.mechanism_storage))
        self.CommandStack.endMacro()
    
    @pyqtSlot(QListWidgetItem)
    def on_mechanism_storage_itemDoubleClicked(self, item):
        """Restore the storage data as below."""
        self.on_mechanism_storage_restore_clicked(item)
    
    @pyqtSlot()
    def on_mechanism_storage_restore_clicked(self, item=None):
        """Restore the storage data."""
        if item is None:
            item = self.mechanism_storage.currentItem()
        if not item:
            return
        reply = QMessageBox.question(self,
            "Storage",
            "Restore mechanism will overwrite the canvas." +
            "\nDo you want to continue?"
        )
        if reply != QMessageBox.Yes:
            return
        name = item.text()
        self.CommandStack.beginMacro(
            "Restore from {{Mechanism: {}}}".format(name)
        )
        self.__clearStorage()
        self.parseExpression(item.expr)
        self.CommandStack.push(DeleteStorage(
            self.mechanism_storage.row(item),
            self.mechanism_storage
        ))
        self.CommandStack.push(AddStorageName(
            name,
            self.mechanism_storage_name_tag
        ))
        self.CommandStack.endMacro()
    
    def loadStorage(self, exprs: Tuple[Tuple[str, str]]):
        """Load storage data from database."""
        for name, expr in exprs:
            self.__addStorage(name, expr, clear=False)
    
    @pyqtSlot()
    def on_action_Check_update_triggered(self):
        """Check for update."""
        progdlg = QProgressDialog("Checking update ...", "Cancel", 0, 3, self)
        progdlg.setAttribute(Qt.WA_DeleteOnClose, True)
        progdlg.setWindowTitle("Check for update")
        progdlg.resize(400, progdlg.height())
        progdlg.setModal(True)
        progdlg.show()
        url = check_update(progdlg)
        if not url:
            QMessageBox.information(self,
                "Pyslvs is up to date",
                "You are using the latest version of Pyslvs."
            )
            return
        reply = QMessageBox.question(
            self,
            "Pyslvs has update",
            "Do you want to get it from Github?",
            (QMessageBox.Ok | QMessageBox.Cancel),
            QMessageBox.Ok
        )
        if reply == QMessageBox.Ok:
            self.__openURL(url)
