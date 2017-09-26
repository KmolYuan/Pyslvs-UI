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
tr = QCoreApplication.translate
from .Ui_main import Ui_MainWindow
from .Ui_custom import initCustomWidgets, action_Enabled, showUndoWindow

#Dialog
from .info.info import version_show
from .io.script import Script_Dialog
#Undo redo
from .io.undoRedo import (
    addTableCommand, deleteTableCommand,
    editPointTableCommand, editLinkTableCommand
)
#Entities
from .entities.edit_point import edit_point_show
from .entities.edit_link import edit_link_show
from .entities.delete import deleteDlg
from .entities.batchMoving import batchMoving_show
#Tools
from .tools.DimensionalSynthesis.Path_Solving import Path_Solving_show
from .tools.DimensionalSynthesis.Triangle_Solver import Triangle_Solver_show
#Solve
from .calculation.planeSolving import slvsProcess
#File & Example
from .io.fileForm import File
from .io import example
from .io.dxfType import dxfTypeSettings
from .io.dxfForm.sketch import dxfSketch
from .io.slvsType import slvsTypeSettings
from .io.slvsForm.sketch import slvs2D
from .info.fileInfo import fileInfo_show, editFileInfo_show
#Logging
from .io.loggingHandler import XStream

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.args = args
        #Console Widget
        self.showConsoleError.setChecked(self.args.w)
        if not self.args.debug_mode:
            self.on_connectConsoleButton_clicked()
        #File
        self.FileState = QUndoStack()
        self.FileState.indexChanged.connect(self.commandReload)
        showUndoWindow(self, self.FileState)
        self.File = File(self.FileState, self.args)
        self.setLocate(QFileInfo(self.args.i if self.args.i else '.').canonicalFilePath())
        #Initialize custom UI
        initCustomWidgets(self)
        self.Resolve()
        #Solve & DOF
        self.Solvefail = False
        self.DOF = 0
        action_Enabled(self)
        if self.args.r:
            self.loadWorkbook("Loading by Argument.", fileName=self.args.r)
        else:
            Args = [
                'ground',
                'R',
                'Red',
                0.,
                0.
            ]
            rowCount = self.Entiteis_Point.rowCount()
            self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
            self.FileState.push(addTableCommand(self.Entiteis_Point))
            self.FileState.push(editPointTableCommand(self.Entiteis_Point, rowCount, self.Entiteis_Link, Args))
            self.FileState.endMacro()
    
    def setLocate(self, locate):
        self.Default_Environment_variables = locate
        print("~Start at: [{}]".format(self.Default_Environment_variables))
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            for url in mimeData.urls():
                FilePath = url.toLocalFile()
                if QFileInfo(FilePath).suffix() in ['pyslvs']:
                    event.acceptProposedAction()
    
    def dropEvent(self, event):
        FilePath = event.mimeData().urls()[-1].toLocalFile()
        self.checkChange(FilePath, [], "Loaded drag-in file: [{}]".format(FilePath))
        event.acceptProposedAction()
    
    #Mouse position on canvace
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    
    #Entiteis_Point context menu
    @pyqtSlot(QPoint)
    def on_point_context_menu(self, point):
        self.enableEditPoint()
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        if action==self.action_point_right_click_menu_copydata:
            self.tableCopy(self.Entiteis_Point)
    
    #Entiteis_Link context menu
    @pyqtSlot(QPoint)
    def on_link_context_menu(self, point):
        self.action_link_right_click_menu_delete.setEnabled(self.Entiteis_Link.currentRow()>0)
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        if action==self.action_link_right_click_menu_copydata:
            self.tableCopy(self.Entiteis_Link)
    
    #DynamicCanvasView context menu
    @pyqtSlot(QPoint)
    def on_painter_context_menu(self, point):
        self.action_painter_right_click_menu_path.setVisible(self.PathSolving.isChecked())
        self.enableEditPoint()
        action = self.popMenu_painter.exec_(self.DynamicCanvasView.mapToGlobal(point))
        if action==self.action_painter_right_click_menu_add:
            self.addPointGroup()
        elif action==self.action_painter_right_click_menu_fix_add:
            self.addPointGroup(True)
        elif action==self.action_painter_right_click_menu_path:
            self.PathSolving_add_rightClick(x, y)
    
    def enableEditPoint(self):
        pos = self.Entiteis_Point.currentRow()
        if pos>-1:
            self.action_point_right_click_menu_lock.setChecked(
                'ground' in self.Entiteis_Point.item(pos, 1).text())
        for action in [
            self.action_point_right_click_menu_edit,
            self.action_point_right_click_menu_lock,
            self.action_point_right_click_menu_copyPoint,
            self.action_link_right_click_menu_copydata,
            self.action_point_right_click_menu_delete
        ]:
            action.setEnabled(pos>-1 and bool(self.Entiteis_Point.selectedRows()))
    
    def tableCopy(self, table):
        text = table.currentItem().text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
    
    #Close Event
    def closeEvent(self, event):
        if self.File.form.changed:
            reply = QMessageBox.question(self, "Message", "Are you sure to quit?\nAny changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_action_Save_triggered()
                if self.File.form.changed:
                    event.ignore()
                else:
                    self.Exit(event)
            elif reply==QMessageBox.Discard:
                self.Exit(event)
            else:
                event.ignore()
        else:
            self.Exit(event)
    def Exit(self, event):
        self.disconnectConsole()
        self.setAttribute(Qt.WA_DeleteOnClose)
        print('Exit.')
        event.accept()
    
    #Undo and Redo
    @pyqtSlot(int)
    def commandReload(self, index=0):
        self.action_Undo.setText("Undo {}".format(self.FileState.undoText()))
        self.action_Redo.setText("Redo {}".format(self.FileState.redoText()))
        if index!=self.File.form.Stack:
            self.workbookNoSave()
        else:
            self.workbookSaved()
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        if "Triangle Solver" in tabNameList:
            self.panelWidget.widget(tabNameList.index("Triangle Solver")).setPoint(self.File.Lists.PointList)
        self.update_inputs_points()
        self.Resolve()
    
    #Resolve
    def Resolve(self):
        result, DOF = slvsProcess(
            self.Entiteis_Point.data(),
            self.Entiteis_Link.data(),
            hasWarning=self.showConsoleError.isChecked())
        Failed = type(DOF)!=int
        self.ConflictGuide.setVisible(Failed)
        self.DOFview.setVisible(not Failed)
        if not Failed:
            self.Solvefail = False
            self.Entiteis_Point.updateCurrentPosition(result)
            self.DOF = DOF
            self.DOFview.setText(str(self.DOF))
            self.Reload_Canvas()
        else:
            self.Solvefail = True
            self.ConflictGuide.setToolTip(DOF)
            self.Reload_Canvas()
    
    #Reload Canvas
    @pyqtSlot(int)
    @pyqtSlot(float)
    def Reload_Canvas(self, *Args):
        self.DynamicCanvasView.update_figure(self.Entiteis_Point.data(), self.Entiteis_Link.data(), self.File.pathData)
    
    #Workbook Change
    def workbookNoSave(self):
        self.File.form.changed = True
        self.setWindowTitle(self.windowTitle().replace('*', str())+'*')
        action_Enabled(self)
    def workbookSaved(self):
        self.File.form.changed = False
        self.setWindowTitle("Pyslvs - {}".format(self.File.form.fileName.fileName()))
        action_Enabled(self)
    
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        self.OpenURL("http://mde.tw")
    
    @pyqtSlot()
    def on_action_Pyslvs_com_triggered(self):
        self.OpenURL("https://pyslvs.com")
    
    @pyqtSlot()
    def on_action_Git_hub_Site_triggered(self):
        self.OpenURL("https://github.com/KmolYuan/Pyslvs-PyQt5")
    
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        self.OpenDlg(version_show(self))
    
    @pyqtSlot()
    def on_action_About_Qt_triggered(self):
        QMessageBox.aboutQt(self)
    
    def OpenURL(self, URL):
        print("Open - {{{}}}".format(URL))
        QDesktopServices.openUrl(QUrl(URL))
    
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        self.OpenDlg(Script_Dialog(self.File.form.fileName.baseName(), Point, Line, Chain, Shaft, Slider, Rod, self.Default_Environment_variables, self))
    @pyqtSlot()
    def on_action_Search_Points_triggered(self):
        self.OpenDlg(Association_show(self.File.Lists.PointList, self.File.Lists.LineList,
            self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self))
    def OpenDlg(self, dlg):
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_action_Console_triggered(self):
        self.OptionTab.setCurrentIndex(2)
        self.History_tab.setCurrentIndex(1)
    
    #TODO: Example need to update!
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        self.checkChange("[New Workbook]", example.new_workbook(), 'Generating New Workbook...')
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        self.checkChange(say='Open file...', isFile=True)
    @pyqtSlot()
    def on_action_Crank_rocker_triggered(self):
        self.checkChange("[Example] Crank Rocker", example.crankRocker())
    @pyqtSlot()
    def on_action_Drag_link_triggered(self):
        self.checkChange("[Example] Drag-link", example.DragLink())
    @pyqtSlot()
    def on_action_Double_rocker_triggered(self):
        self.checkChange("[Example] Double Rocker", example.doubleRocker())
    @pyqtSlot()
    def on_action_Parallelogram_linkage_triggered(self):
        self.checkChange("[Example] Parallelogram Linkage", example.parallelogramLinkage())
    @pyqtSlot()
    def on_action_Multiple_Link_triggered(self):
        self.checkChange("[Example] Multiple Link", example.multipleLink())
    @pyqtSlot()
    def on_action_Two_Multiple_Link_triggered(self):
        self.checkChange("[Example] Two Pairs Multiple Link", example.twoMultipleLink())
    @pyqtSlot()
    def on_action_Four_bar_linkage_triggered(self):
        self.checkChange("[Example] Four bar linkage", example.FourBarFeet())
    @pyqtSlot()
    def on_action_Slider_and_Rod_triggered(self):
        self.checkChange("[Example] Slider and Rod", example.sliderRod())
    @pyqtSlot()
    def on_action_Rock_Slider_triggered(self):
        self.checkChange("[Example] Rock Slider", example.rockSlider())
    @pyqtSlot()
    def on_action_Lift_Tailgate_triggered(self):
        self.checkChange("[Example] Lift Tailgate", example.liftTailgate())
    @pyqtSlot()
    def on_action_Theo_Jansen_s_multi_linkage_triggered(self):
        self.checkChange("[Example] Theo Jansen\'s multiple linkage", example.TJLinkage())
    @pyqtSlot()
    def on_action_Rock_Slider_Design_triggered(self):
        self.checkChange("[Example] Rock slider design", example.RockSliderDesign())
    @pyqtSlot()
    def on_action_Reverse_Parsing_Rocker_triggered(self):
        self.checkChange("[Example] Reverse Parsing Rocker", example.reverseParsingRocker())
    @pyqtSlot()
    def on_action_Three_Algorithm_Result_triggered(self):
        self.checkChange("[Example] Three algorithm result", example.threeAlgorithmResult())
    
    #Workbook Functions
    def checkChange(self, name='', data=[], say='Loading Example...', isFile=False):
        if self.File.form.changed:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit this file?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_action_Save_triggered()
                if not self.File.form.changed:
                    self.loadWorkbook(say, name, data, isFile)
            elif reply==QMessageBox.Discard:
                self.loadWorkbook(say, name, data, isFile)
        else:
            self.loadWorkbook(say, name, data, isFile)
    
    def loadWorkbook(self, say, fileName='', data=[], isFile=False):
        if isFile:
            data.clear()
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, "XML File(*.xml);;CSV File(*.csv)")
            if fileName:
                self.setLocate(QFileInfo(fileName).absolutePath())
        if fileName or isFile==False:
            print(say)
            self.closeAllPanels()
            self.File.reset(self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain,
                self.Simulate_Shaft, self.Simulate_Slider, self.Simulate_Rod, self.Parameter_list)
            self.DynamicCanvasView.changeCurrentShaft()
            self.DynamicCanvasView.path_solving()
            self.Resolve()
            self.setWindowTitle("Pyslvs - [New Workbook]")
            print("Reset workbook.")
            checkdone, data = self.File.check(fileName, data)
            if checkdone:
                errorInfo = self.File.read(fileName, data,
                    self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain,
                    self.Simulate_Shaft, self.Simulate_Slider, self.Simulate_Rod, self.Parameter_list)
                if errorInfo:
                    print("The following content(s) contain errors:\n+ {{{}}}".format(', '.join(errorInfo)))
                else:
                    print("Successful loaded contents of the file.")
                self.workbookSaved()
                self.DynamicCanvasView.SetIn()
                print("Loaded the workbook.")
                if '[New Workbook]' in fileName and isFile==False:
                    self.on_action_Property_triggered()
                else:
                    self.show_Property(errorInfo)
                    if errorInfo:
                        self.on_action_Console_triggered()
            else:
                self.loadWorkbookError(fileName)
    
    @pyqtSlot()
    def on_action_Import_From_Workbook_triggered(self):
        self.importWorkbook(say='Import from file...')
    
    def importWorkbook(self, say, fileName=False, data=[]):
        if fileName==False:
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, "XML File(*.xml);;CSV File(*.csv)")
            if fileName:
                self.setLocate(QFileInfo(fileName).absolutePath())
        if fileName:
            print(say)
            checkdone, data = self.File.check(fileName, data)
            if checkdone:
                suffix = QFileInfo(fileName).suffix().lower()
                tables = [data, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain,
                    self.Simulate_Shaft, self.Simulate_Slider, self.Simulate_Rod, self.Parameter_list]
                if suffix=='xml':
                    errorInfo = self.File.readXMLMerge(*tables)
                elif suffix=='csv':
                    errorInfo = self.File.readCSVMerge(*tables)
                self.show_Property(errorInfo)
                if errorInfo:
                    self.on_action_Console_triggered()
            else:
                self.loadWorkbookError(fileName)
    
    def loadWorkbookError(self, fileName):
        dlgbox = QMessageBox(QMessageBox.Warning, "Loading failed", "File:\n{}\n\nYour data sheet is an incorrect format.".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_():
            print("Error: Incorrect format.")
    
    #TODO: Save format need to update!
    @pyqtSlot()
    def on_action_Save_triggered(self):
        fileName = self.File.form.fileName.absoluteFilePath()
        suffix = QFileInfo(fileName).suffix()
        self.save('' if suffix!='csv' and suffix!='xml' else fileName)
    
    @pyqtSlot()
    def on_action_Save_as_triggered(self):
        self.save()
    
    def save(self, fileName=str()):
        hasReply = bool(fileName)==False
        if hasReply:
            fileName = self.outputTo("Workbook", ["XML File(*.xml)", "CSV File(*.csv)"])
        if fileName:
            self.File.write(fileName)
            if hasReply:
                self.saveReplyBox('Workbook', fileName)
            self.workbookSaved()
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        dlg = slvsTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_():
            self.saveReplyBox('Solvespace Models', dlg.folderPath.absolutePath())
    
    @pyqtSlot()
    def on_action_Solvespace_2D_sketch_triggered(self):
        fileName = self.outputTo("Solvespace sketch", ['Solvespace module(*.slvs)'])
        if fileName:
            content = slvs2D(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f:
                f.write(content)
            self.saveReplyBox('Solvespace Sketch', fileName)
    
    @pyqtSlot()
    def on_action_DXF_2D_models_triggered(self):
        dlg = dxfTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_():
            self.saveReplyBox('DXF 2D Models', dlg.filePath)
    
    @pyqtSlot()
    def on_action_DXF_2D_sketch_triggered(self):
        fileName = self.outputTo("DXF", ['AutoCAD DXF (*.dxf)'])
        if fileName:
            dxfSketch(fileName, self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            self.saveReplyBox('DXF 2D Sketch', fileName)
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        fileName = self.outputTo("picture", ["Portable Network Graphics (*.png)", "Joint Photographic Experts Group (*.jpg)", "Bitmap Image file (*.bmp)",
            "Business Process Model (*.bpm)", "Tagged Image File Format (*.tiff)", "Windows Icon (*.ico)", "Wireless Application Protocol Bitmap (*.wbmp)",
            "X BitMap (*.xbm)", "X Pixmap (*.xpm)"])
        if fileName:
            pixmap = self.DynamicCanvasView.grab()
            pixmap.save(fileName, format = QFileInfo(fileName).suffix())
            self.saveReplyBox('Picture', fileName)
    
    def outputTo(self, formatName, formatChoose):
        suffix0 = formatChoose[0].split('*')[-1][:-1]
        fileName, form = QFileDialog.getSaveFileName(self, 'Save file...',
            self.Default_Environment_variables+'/'+self.File.form.fileName.baseName()+suffix0, ';;'.join(formatChoose))
        if fileName:
            if QFileInfo(fileName).suffix()!=suffix0[1:]:
                fileName = fileName+suffix0
            self.setLocate(QFileInfo(fileName).absolutePath())
            print("Formate: {}".format(form))
        return fileName
    
    def saveReplyBox(self, title, fileName):
        dlgbox = QMessageBox(QMessageBox.Information, title, "Successfully converted:\n{}".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_():
            print("Successful saved {}.".format(title))
    
    def show_Property(self, errorInfo):
        dlg = fileInfo_show(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description,
            self.File.form.lastTime, self.File.Designs.result, errorInfo, self)
        dlg.show()
        if dlg.exec_():
            pass
    
    @pyqtSlot()
    def on_action_Property_triggered(self):
        dlg = editFileInfo_show(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description,
            self.File.form.lastTime, self.File.Designs.result, self)
        dlg.show()
        if dlg.exec_():
            self.File.updateAuthorDescription(dlg.authorName_input.text(), dlg.descriptionText.toPlainText())
            self.workbookNoSave()
    
    @pyqtSlot()
    def on_action_Output_to_PMKS_triggered(self):
        url = "http://designengrlab.github.io/PMKS/pmks.html?mech="
        urlTable = []
        for row in range(self.Entiteis_Point.rowCount()):
            TypeAndAngle = self.Entiteis_Point.item(row, 2).text().split(':')
            pointData = [
                self.Entiteis_Point.item(row, 1).text(),
                TypeAndAngle[0],
                self.Entiteis_Point.item(row, 4).text(),
                self.Entiteis_Point.item(row, 5).text(),
            ]
            if len(TypeAndAngle)==2:
                pointData.append(TypeAndAngle[1])
            pointData.append('tfff')
            urlTable.append(','.join(pointData))
        url += '|'.join(urlTable)+'|'
        text = '\n'.join([
            "Copy and past this link to web browser:\n", url+'\n',
            "If you have installed Microsoft Silverlight in Internet Explorer as default browser, "+
            "just click \"Open\" button to open it in PMKS web version."
        ])
        dlg = QMessageBox(QMessageBox.Information, "PMKS web server", text, (QMessageBox.Open | QMessageBox.Close), self)
        dlg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        dlg.show()
        if dlg.exec()==QMessageBox.Open:
            self.OpenURL(url)
    
    #Entities
    def addPointGroup(self, fixed=False):
        if not self.PathSolving.isChecked():
            Args = [
                'ground' if fixed else '',
                'R',
                'Blue' if fixed else 'Green',
                self.mouse_pos_x,
                self.mouse_pos_y
            ]
            rowCount = self.Entiteis_Point.rowCount()
            self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
            self.FileState.push(addTableCommand(self.Entiteis_Point))
            self.FileState.push(editPointTableCommand(self.Entiteis_Point, rowCount, self.Entiteis_Link, Args))
            self.FileState.endMacro()
        else:
            self.PathSolving_add_rightClick(self.mouse_pos_x, self.mouse_pos_y)
    
    @pyqtSlot(list)
    def addLinkGroup(self, points):
        name = 'link_0'
        names = [self.Entiteis_Link.item(row, 0).text() for row in range(self.Entiteis_Link.rowCount())]
        i = 0
        while name in names:
            i += 1
            name = 'link_{}'.format(i)
        Args = [
            name,
            'Blue',
            ','.join(['Point{}'.format(i) for i in points])
        ]
        self.FileState.beginMacro("Add {{Link: {}}}".format(name))
        self.FileState.push(addTableCommand(self.Entiteis_Link))
        self.FileState.push(editLinkTableCommand(self.Entiteis_Link, self.Entiteis_Link.rowCount()-1, self.Entiteis_Point, Args))
        self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        self.editPoint()
    
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self):
        pos = self.Entiteis_Point.currentRow()
        pos = pos if pos>-1 else 0
        self.editPoint(pos)
    
    def editPoint(self, pos=False):
        dlg = edit_point_show(self.Entiteis_Point.data(), self.Entiteis_Link.data(), pos, self)
        dlg.show()
        if dlg.exec_():
            rowCount = self.Entiteis_Point.rowCount()
            Type = dlg.Type.currentText().split(" ")[0]
            if Type!='R':
                Type += ":{}".format(dlg.Angle.value())
            Args = [
                ','.join([dlg.selected.item(row).text() for row in range(dlg.selected.count())]),
                Type,
                dlg.Color.currentText(),
                dlg.X_coordinate.value(),
                dlg.Y_coordinate.value()
            ]
            if pos is False:
                self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
                self.FileState.push(addTableCommand(self.Entiteis_Point))
                pos = rowCount
            else:
                self.FileState.beginMacro("Edit {{Point{}}}".format(rowCount))
            self.FileState.push(editPointTableCommand(self.Entiteis_Point, pos, self.Entiteis_Link, Args))
            self.FileState.endMacro()
    
    def lockPoint(self):
        pos = self.Entiteis_Point.currentRow()
        Links = self.Entiteis_Point.item(pos, 1).text().split(',')
        if 'ground' in Links:
            Links.remove('ground')
        else:
            Links.append('ground')
        Args = [
            ','.join(filter(lambda a: a!='', Links)),
            self.Entiteis_Point.item(pos, 2).text(),
            self.Entiteis_Point.item(pos, 3).text(),
            self.Entiteis_Point.item(pos, 4).text(),
            self.Entiteis_Point.item(pos, 5).text()
        ]
        self.FileState.beginMacro("Edit {{Point{}}}".format(pos))
        self.FileState.push(editPointTableCommand(self.Entiteis_Point, pos, self.Entiteis_Link, Args))
        self.FileState.endMacro()
    
    def copyPoint(self):
        pos = self.Entiteis_Point.currentRow()
        Args = [
            self.Entiteis_Point.item(pos, 1).text(),
            self.Entiteis_Point.item(pos, 2).text(),
            'Orange',
            self.Entiteis_Point.item(pos, 4).text(),
            self.Entiteis_Point.item(pos, 5).text()
        ]
        rowCount = self.Entiteis_Point.rowCount()
        self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
        self.FileState.push(addTableCommand(self.Entiteis_Point))
        self.FileState.push(editPointTableCommand(self.Entiteis_Point, rowCount, self.Entiteis_Link, Args))
        self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        self.editLineDlg()
    
    @pyqtSlot()
    def on_action_Edit_Linkage_triggered(self):
        pos = self.Entiteis_Link.currentRow()
        pos = pos if pos>0 else 1
        self.editLineDlg(pos)
    
    def editLineDlg(self, pos=False):
        dlg = edit_link_show(self.Entiteis_Point.data(), self.Entiteis_Link.data(), pos, self)
        dlg.show()
        if dlg.exec_():
            name = dlg.name_edit.text()
            Args = [
                name,
                dlg.Color.currentText(),
                ','.join([dlg.selected.item(row).text() for row in range(dlg.selected.count())])
            ]
            if pos is False:
                self.FileState.beginMacro("Add {{Link: {}}}".format(name))
                self.FileState.push(addTableCommand(self.Entiteis_Link))
                pos = self.Entiteis_Link.rowCount()-1
            else:
                self.FileState.beginMacro("Edit {{Link: {}}}".format(name))
            self.FileState.push(editLinkTableCommand(self.Entiteis_Link, pos, self.Entiteis_Point, Args))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self):
        pos = self.Entiteis_Point.currentRow()
        pos = self.deleteDlg(self.action_New_Point.icon(), self.Entiteis_Point, pos if pos>-1 else 0)
        if pos is not None:
            Args = [
                '',
                self.Entiteis_Point.item(pos, 2).text(),
                self.Entiteis_Point.item(pos, 3).text(),
                self.Entiteis_Point.item(pos, 4).text(),
                self.Entiteis_Point.item(pos, 5).text()
            ]
            self.FileState.beginMacro("Delete {{Point{}}}".format(pos))
            self.FileState.push(editPointTableCommand(self.Entiteis_Point, pos, self.Entiteis_Link, Args))
            self.FileState.push(deleteTableCommand(self.Entiteis_Point, pos, isRename=True))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Linkage_triggered(self):
        pos = self.Entiteis_Link.currentRow()
        if pos>0:
            pos = self.deleteDlg(self.action_New_Line.icon(), self.Entiteis_Link, pos)
            if pos is not None:
                Args = [
                    self.Entiteis_Link.item(pos, 0).text(),
                    self.Entiteis_Link.item(pos, 1).text(),
                    ''
                ]
                self.FileState.beginMacro("Delete {{Link: {}}}".format(self.Entiteis_Link.item(pos, 0).text()))
                self.FileState.push(editLinkTableCommand(self.Entiteis_Link, pos, self.Entiteis_Point, Args))
                self.FileState.push(deleteTableCommand(self.Entiteis_Link, pos, isRename=False))
                self.FileState.endMacro()
    
    def deleteDlg(self, icon, table, pos):
        dlg = deleteDlg(icon, table, pos, self)
        dlg.move(QCursor.pos()-QPoint(dlg.size().width()/2, dlg.size().height()/2))
        dlg.show()
        if dlg.exec_():
            self.closeAllPanels()
            return dlg.Entity.currentIndex()
    
    @pyqtSlot()
    def on_action_Batch_moving_triggered(self):
        dlg = batchMoving_show(self.Entiteis_Point.data(), self.Entiteis_Point.selectedRows(), self)
        dlg.show()
        if dlg.exec_():
            points = [int(dlg.selected.item(row).text().replace('Point', '')) for row in range(dlg.selected.count())]
            self.FileState.beginMacro("Batch moving {{Point {}}}".format(points))
            for row in points:
                Args = [
                    self.Entiteis_Point.item(row, 1).text(),
                    self.Entiteis_Point.item(row, 2).text(),
                    self.Entiteis_Point.item(row, 3).text(),
                    float(self.Entiteis_Point.item(row, 4).text())+dlg.XIncrease.value(),
                    float(self.Entiteis_Point.item(row, 5).text())+dlg.YIncrease.value()
                ]
                self.FileState.push(editPointTableCommand(self.Entiteis_Point, row, self.Entiteis_Link, Args))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_Zoom_to_fit_triggered(self):
        self.DynamicCanvasView.SetIn()
    
    @pyqtSlot()
    def on_ResetCanvas_clicked(self):
        self.DynamicCanvasView.SetIn()
    @pyqtSlot()
    def on_CanvasCapture_clicked(self):
        clipboard = QApplication.clipboard()
        pixmap = self.DynamicCanvasView.grab()
        clipboard.setPixmap(pixmap)
        dlgbox = QMessageBox(self)
        dlgbox.setWindowTitle("Captured!")
        dlgbox.setStandardButtons((QMessageBox.Ok))
        dlgbox.setIconPixmap(pixmap.scaledToWidth(650))
        if dlgbox.exec_():
            pass
    
    @pyqtSlot(int)
    def setZoomBar(self, val):
        self.ZoomBar.setValue(val)
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setText('{}%'.format(value))
    
    #Wheel Event
    def wheelEvent(self, event):
        if self.DynamicCanvasView.underMouse():
            self.ZoomBar.setValue(self.ZoomBar.value()+10*(1 if event.angleDelta().y()>0 else -1))
    
    @pyqtSlot(bool)
    def on_action_Display_Dimensions_toggled(self, p0):
        if p0:
            self.action_Display_Point_Mark.setChecked(True)
    @pyqtSlot(bool)
    def on_action_Display_Point_Mark_toggled(self, p0):
        if not p0:
            self.action_Display_Dimensions.setChecked(False)
    
    @pyqtSlot()
    def on_action_Path_data_show_triggered(self):
        self.DynamicCanvasView.Path.show = self.action_Path_data_show.isChecked()
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_action_Path_style_triggered(self):
        self.DynamicCanvasView.Path.mode = self.action_Path_style.isChecked()
        self.Reload_Canvas()
    
    def update_inputs_points(self):
        self.inputs_points.clear()
        for i in range(self.Entiteis_Point.rowCount()):
            self.inputs_points.addItem('Point{}'.format(i))
    
    @pyqtSlot(tuple)
    def inputs_points_setSelection(self, selections):
        self.inputs_points.setCurrentRow(selections[0])
    
    @pyqtSlot()
    def inputs_points_clearSelection(self):
        self.inputs_points.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_inputs_points_currentRowChanged(self, row):
        if not row in self.Entiteis_Point.selectedRows():
            self.Entiteis_Point.setSelections((row,))
        self.inputs_baseLinks.clear()
        if row>-1:
            for linkName in self.Entiteis_Point.item(row, 1).text().split(','):
                self.inputs_baseLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_baseLinks_currentRowChanged(self, row):
        self.inputs_driveLinks.clear()
        if row>-1:
            for linkName in self.Entiteis_Point.item(self.inputs_points.currentRow(), 1).text().split(','):
                if linkName==self.inputs_baseLinks.currentItem().text():
                    continue
                self.inputs_driveLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_driveLinks_currentRowChanged(self, row):
        self.inputs_variable_add.setEnabled(row>-1)
    
    @pyqtSlot()
    def on_inputs_variable_add_clicked(self):
        angle = str(0.)
        text = '->'.join([
            self.inputs_points.currentItem().text(),
            self.inputs_baseLinks.currentItem().text(),
            self.inputs_driveLinks.currentItem().text(),
            angle])
        if self.inputs_variable.count()<self.DOF and not self.inputs_variable.findItems(text, Qt.MatchExactly):
            self.inputs_variable.addItem(text)
    
    @pyqtSlot()
    def on_inputs_variable_remove_clicked(self):
        row = self.inputs_variable.currentRow()
        if row>-1:
            self.inputs_variable.takeItem(row)
    
    @pyqtSlot(int)
    def on_inputs_variable_currentRowChanged(self, row):
        self.inputs_Degree.setEnabled(row>-1)
        if row>-1:
            #TODO: Set the angle of QDial.
            pass
    
    @pyqtSlot(bool)
    def on_PathSolving_clicked(self):
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        self.DynamicCanvasView.showSlvsPath = not "Path Solving" in tabNameList
        if "Path Solving" in tabNameList:
            self.closePanel(tabNameList.index("Path Solving"))
        else:
            panel = Path_Solving_show(
                self.File.Designs.path,
                self.File.Designs.result,
                self.Default_Environment_variables,
                self.workbookNoSave,
                self)
            panel.fixPointRange.connect(self.DynamicCanvasView.update_ranges)
            panel.addPathPoint.connect(self.PathSolving_add)
            panel.deletePathPoint.connect(self.PathSolving_delete)
            panel.moveupPathPoint.connect(self.PathSolving_moveup)
            panel.movedownPathPoint.connect(self.PathSolving_movedown)
            panel.mergeResult.connect(self.PathSolving_mergeResult)
            self.panelWidget.addTab(panel, self.PathSolving.icon(), "Path Solving")
            self.panelWidget.setCurrentIndex(self.panelWidget.count()-1)
        self.Reload_Canvas()
    def PathSolving_add_rightClick(self, x, y):
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        self.panelWidget.widget(tabNameList.index("Path Solving")).addPath(x, y)
        self.PathSolving_add(x, y)
    @pyqtSlot(float, float)
    def PathSolving_add(self, x=0, y=0):
        self.File.Designs.add(x, y)
        self.DynamicCanvasView.path_solving(self.File.Designs.path)
    @pyqtSlot(int)
    def PathSolving_delete(self, row):
        self.File.Designs.remove(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.path)
    @pyqtSlot(int)
    def PathSolving_moveup(self, row):
        self.File.Designs.moveUP(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.path)
    @pyqtSlot(int)
    def PathSolving_movedown(self, row):
        self.File.Designs.moveDown(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.path)
    @pyqtSlot(int)
    def PathSolving_deleteResult(self, row):
        self.File.Designs.removeResult(row)
    @pyqtSlot(int, float, float, list, dict)
    def PathSolving_mergeResult(self, row, startAngle, endAngle, answer, Paths):
        if self.File.Generate_Merge(row, startAngle, endAngle, answer, Paths,
                self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain, self.Simulate_Shaft)==False:
            dlgbox = QMessageBox(QMessageBox.Warning, "Error when merge...", "Please check dimension.", (QMessageBox.Ok), self)
            if dlgbox.exec_():
                print("Generate Result Error.")
                self.on_action_Console_triggered()
    
    @pyqtSlot(bool)
    def on_TriangleSolver_clicked(self):
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        if "Triangle Solver" in tabNameList:
            self.closePanel(tabNameList.index("Triangle Solver"))
        else:
            panel = Triangle_Solver_show(self.FileState, self.File.Lists.PointList, self.File.Designs.TSDirections, self)
            panel.startMerge.connect(self.TriangleSolver_merge)
            self.panelWidget.addTab(panel, self.TriangleSolver.icon(), "Triangle Solver")
            self.panelWidget.setCurrentIndex(self.panelWidget.count()-1)
    @pyqtSlot()
    def TriangleSolver_merge(self):
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        self.File.TS_Merge(self.panelWidget.widget(tabNameList.index("Triangle Solver")).answers,
            self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Chain, self.Simulate_Slider)
    
    def closeAllPanels(self):
        for i in reversed(range(self.panelWidget.count())):
            self.closePanel(i)
        for button in [self.TriangleSolver, self.PathSolving]:
            button.setChecked(False)
        self.DynamicCanvasView.showSlvsPath = False
        self.DynamicCanvasView.Path.drive_mode = False
        self.Reload_Canvas()
    
    def closePanel(self, pos):
        panel = self.panelWidget.widget(pos)
        self.panelWidget.removeTab(pos)
        panel.deleteLater()
    
    @pyqtSlot()
    def pointSelection(self):
        self.DynamicCanvasView.changePointsSelection(self.Entiteis_Point.selectedRows())
    
    @pyqtSlot(int, int, int, int)
    def on_Parameter_list_currentCellChanged(self, c0, c1, p0, p1):
        try:
            self.Parameter_num.setPlainText('n{}'.format(c0))
            self.Parameter_digital.setPlaceholderText(str(self.Parameter_list.item(c0, 1).text()))
            self.Parameter_comment.setPlaceholderText(str(self.Parameter_list.item(c0, 2).text()))
            self.Parameter_comment.setText(str(self.Parameter_list.item(c0, 2).text()))
        except:
            self.Parameter_num.setPlainText('N/A')
            self.Parameter_digital.setPlaceholderText('0.0')
            self.Parameter_comment.setPlaceholderText('No-comment')
        self.Parameter_digital.clear()
        self.Parameter_comment.clear()
        enabled = self.Parameter_list.rowCount()>0 and c0>-1
        for widget in [self.Parameter_num, self.Parameter_digital, self.Parameter_comment, self.Parameter_lable,
            self.Comment_lable, self.Parameter_update]:
                widget.setEnabled(enabled)
    
    def connectConsole(self):
        XStream.stdout().messageWritten.connect(self.appendToConsole)
        XStream.stderr().messageWritten.connect(self.appendToConsole)
    def disconnectConsole(self):
        XStream.back()
    @pyqtSlot()
    def on_connectConsoleButton_clicked(self):
        print("Connect to GUI console.")
        self.connectConsole()
        self.connectConsoleButton.setEnabled(False)
        self.disconnectConsoleButton.setEnabled(True)
        print("Connect to GUI console.")
    @pyqtSlot()
    def on_disconnectConsoleButton_clicked(self):
        print("Disconnect from GUI console.")
        self.disconnectConsole()
        self.connectConsoleButton.setEnabled(True)
        self.disconnectConsoleButton.setEnabled(False)
        print("Disconnect from GUI console.")
    
    @pyqtSlot(str)
    def appendToConsole(self, log):
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
        self.consoleWidgetBrowser.insertPlainText(log)
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
    
    @pyqtSlot(int)
    def on_panelWidget_currentChanged(self, index):
        if index==-1:
            self.panelWidget.hide()
        else:
            if not self.panelWidget.isVisible():
                self.panelWidget.show()
