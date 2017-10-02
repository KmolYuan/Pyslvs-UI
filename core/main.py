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
from .widgets.custom import initCustomWidgets, action_Enabled, showUndoWindow

#Dialog
from .info.info import version_show
from .io.script import Script_Dialog
#Undo redo
from .io.undoRedo import (
    addTableCommand, deleteTableCommand,
    editPointTableCommand, editLinkTableCommand,
    fixSequenceNumberCommand
)
#Entities
from .entities.edit_point import edit_point_show
from .entities.edit_link import edit_link_show
from .entities.delete import deleteDlg
from .entities.batchMoving import batchMoving_show
#Tools
from .synthesis.DimensionalSynthesis.Path_Solving import Path_Solving_show
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
        #Console widget.
        self.showConsoleError.setChecked(self.args.w)
        if not self.args.debug_mode:
            self.on_connectConsoleButton_clicked()
        #Undo stack and undo list widget.
        showUndoWindow(self)
        #Set file informations.
        self.File = File(self.FileState, self.args)
        self.setLocate(QFileInfo(self.args.i if self.args.i else '.').canonicalFilePath())
        #Initialize custom UI.
        initCustomWidgets(self)
        self.Resolve()
        #Solve & DOF value.
        self.DOF = 0
        #Enble or disable actions.
        action_Enabled(self)
        if self.args.r:
            #Load workbook.
            self.loadWorkbook("Loading exist workbook.", fileName=self.args.r)
        else:
            #Blank workbook.
            self.addPoint(0., 0., True, 'Red')
    
    #Set environment variables
    def setLocate(self, locate):
        self.Default_Environment_variables = locate
        print("~Start at: [{}]".format(self.Default_Environment_variables))
    
    #Drag file in to our window.
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            for url in mimeData.urls():
                FilePath = url.toLocalFile()
                if QFileInfo(FilePath).suffix() in ['pyslvs']:
                    event.acceptProposedAction()
    
    #Drop file in to our window.
    def dropEvent(self, event):
        FilePath = event.mimeData().urls()[-1].toLocalFile()
        self.checkChange(FilePath, [], "Loaded drag-in file: [{}]".format(FilePath))
        event.acceptProposedAction()
    
    #Mouse position on canvace
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    
    #Entities_Point context menu
    @pyqtSlot(QPoint)
    def on_point_context_menu(self, point):
        self.enableEditPoint()
        action = self.popMenu_point.exec_(self.Entities_Point_Widget.mapToGlobal(point))
        if action==self.action_point_right_click_menu_copydata:
            self.tableCopy(self.Entities_Point)
    
    #Entities_Link context menu
    @pyqtSlot(QPoint)
    def on_link_context_menu(self, point):
        self.action_link_right_click_menu_delete.setEnabled(self.Entities_Link.currentRow()>0)
        action = self.popMenu_link.exec_(self.Entities_Link_Widget.mapToGlobal(point))
        if action==self.action_link_right_click_menu_copydata:
            self.tableCopy(self.Entities_Link)
    
    #DynamicCanvasView context menu
    @pyqtSlot(QPoint)
    def on_painter_context_menu(self, point):
        self.action_painter_right_click_menu_path.setVisible(self.DimensionalSynthesis.isChecked())
        self.enableEditPoint()
        self.popMenu_painter.exec_(self.DynamicCanvasView.mapToGlobal(point))
    
    #What ever we have least one point or not, need to enable / disable QAction.
    def enableEditPoint(self):
        pos = self.Entities_Point.currentRow()
        if pos>-1:
            self.action_point_right_click_menu_lock.setChecked(
                'ground' in self.Entities_Point.item(pos, 1).text())
        for action in [
            self.action_point_right_click_menu_edit,
            self.action_point_right_click_menu_lock,
            self.action_point_right_click_menu_copyPoint,
            self.action_link_right_click_menu_copydata,
            self.action_point_right_click_menu_delete
        ]:
            action.setEnabled(pos>-1 and bool(self.Entities_Point.selectedRows()))
    
    #Copy item text to clipboard.
    def tableCopy(self, table):
        text = table.currentItem().text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
    
    #Close Event: If the user has not saved the change.
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
    
    #The time of withdrawal and redo action.
    @pyqtSlot(int)
    def commandReload(self, index=0):
        self.action_Undo.setText("Undo - {}".format(self.FileState.undoText()))
        self.action_Redo.setText("Redo - {}".format(self.FileState.redoText()))
        if index!=self.File.form.Stack:
            self.workbookNoSave()
        else:
            self.workbookSaved()
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        if "Triangle Solver" in tabNameList:
            self.panelWidget.widget(tabNameList.index("Triangle Solver")).setPoint(self.File.Lists.PointList)
        self.update_inputs_points()
        self.inputs_variable_autoremove()
        self.Resolve()
    
    #Resolve: Use Solvespace kernel.
    def Resolve(self):
        result, DOF = slvsProcess(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self.variableConstraints(),
            hasWarning=self.showConsoleError.isChecked()
        )
        Failed = type(DOF)!=int
        self.ConflictGuide.setVisible(Failed)
        self.DOFview.setVisible(not Failed)
        if not Failed:
            self.Entities_Point.updateCurrentPosition(result)
            self.DOF = DOF
            self.DOFview.setText(str(self.DOF))
            self.Reload_Canvas()
        else:
            self.ConflictGuide.setToolTip(DOF)
            self.Reload_Canvas()
    
    #Reload Canvas, without resolving.
    @pyqtSlot(int)
    @pyqtSlot(float)
    def Reload_Canvas(self, *Args):
        self.DynamicCanvasView.update_figure(
            self.Entities_Point.data(),
            self.Entities_Link.data(),
            self.File.pathData)
    
    #Workbook Change signal.
    def workbookNoSave(self):
        self.File.form.changed = True
        self.setWindowTitle(self.windowTitle().replace('*', '')+'*')
        action_Enabled(self)
    def workbookSaved(self):
        self.File.form.changed = False
        self.setWindowTitle("Pyslvs - {}".format(self.File.form.fileName.fileName()))
        action_Enabled(self)
    
    #Open website: http://mde.tw
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        self.OpenURL("http://mde.tw")
    
    #Open website: https://pyslvs.com
    @pyqtSlot()
    def on_action_Pyslvs_com_triggered(self):
        self.OpenURL("https://pyslvs.com")
    
    #Open website: Github repository.
    @pyqtSlot()
    def on_action_github_repository_triggered(self):
        self.OpenURL("https://github.com/KmolYuan/Pyslvs-PyQt5")
    
    #Open Pyslvs about.
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        self.OpenDlg(version_show(self))
    
    #Open Qt about.
    @pyqtSlot()
    def on_action_About_Qt_triggered(self):
        QMessageBox.aboutQt(self)
    
    #Use to open link.
    def OpenURL(self, URL):
        print("Open - {{{}}}".format(URL))
        QDesktopServices.openUrl(QUrl(URL))
    
    #TODO: Output to Python script for Jupyterhub.
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        self.OpenDlg(Script_Dialog(self.File.form.fileName.baseName(), Point, Line, Chain, Shaft, Slider, Rod, self.Default_Environment_variables, self))
    
    #Use to open dialog widgets.
    def OpenDlg(self, dlg):
        dlg.show()
        dlg.exec()
    
    #Open GUI console.
    @pyqtSlot()
    def on_action_Console_triggered(self):
        self.OptionTab.setCurrentIndex(2)
        self.History_tab.setCurrentIndex(1)
    
    #TODO: Examples need to update!
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
    
    #Load PMKS URL
    @pyqtSlot()
    def on_action_From_PMKS_server_triggered(self):
        URL, ok = QInputDialog.getText(self, "PMKS URL input", "Please input link string:")
        if ok:
            dlg = QMessageBox(QMessageBox.Warning, "Loading failed", "Your link is in an incorrect format.", (QMessageBox.Ok), self)
            if URL:
                try:
                    self.URLParser(tuple(filter(lambda s: 'mech=' in s, URL.split('?')[-1].split('&')))[0].replace('mech=', ''))
                except:
                    dlg.show()
                    dlg.exec_()
            else:
                dlg.show()
                dlg.exec_()
    
    #Parse URL from PMKS symbolic.
    def URLParser(self, URL):
        textList = tuple(filter(lambda s: s!='', URL.split('|')))
        for text in textList:
            item = text.split(',')[:-1]
            isfloat = lambda s: s.replace('.','',1).isdigit()
            hasAngle = isfloat(item[-1]) and isfloat(item[-2]) and isfloat(item[-3])
            links = item[:-4] if hasAngle else item[:-3]
            item = item[-4:] if hasAngle else item[-3:]
            linkNames = [vlink.name for vlink in self.Entities_Link.data()]
            for linkName in links:
                #If link name not exist.
                if linkName not in linkNames:
                    linkArgs = [linkName, 'Blue', '']
                    self.FileState.beginMacro("Add {{Link: {}}}".format(linkName))
                    self.FileState.push(addTableCommand(self.Entities_Link))
                    self.FileState.push(editLinkTableCommand(self.Entities_Link, self.Entities_Link.rowCount()-1, self.Entities_Point, linkArgs))
                    self.FileState.endMacro()
            pointArgs = [
                ','.join(links),
                '{}:{}'.format(item[-4], item[-1]) if item[0]!='R' else 'R',
                'Blue' if 'ground' in links else 'Green',
                item[1],
                item[2]
            ]
            rowCount = self.Entities_Point.rowCount()
            self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
            self.FileState.push(addTableCommand(self.Entities_Point))
            self.FileState.push(editPointTableCommand(self.Entities_Point, rowCount, self.Entities_Link, pointArgs))
            self.FileState.endMacro()
    
    #Load workbook
    def loadWorkbook(self, say, fileName='', data=[], isFile=False):
        if isFile:
            data.clear()
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, "XML File(*.xml);;CSV File(*.csv)")
            if fileName:
                self.setLocate(QFileInfo(fileName).absolutePath())
        if fileName or isFile==False:
            print(say)
            self.closeAllPanels()
            self.File.reset(self.Entities_Point, self.Entities_Link, self.Entities_Chain,
                self.Simulate_Shaft, self.Simulate_Slider, self.Simulate_Rod, self.Parameter_list)
            self.DynamicCanvasView.changeCurrentShaft()
            self.DynamicCanvasView.path_solving()
            self.Resolve()
            self.setWindowTitle("Pyslvs - [New Workbook]")
            print("Reset workbook.")
            checkdone, data = self.File.check(fileName, data)
            if checkdone:
                errorInfo = self.File.read(fileName, data,
                    self.Entities_Point, self.Entities_Link, self.Entities_Chain,
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
    
    #Import from workbook option
    @pyqtSlot()
    def on_action_Import_From_Workbook_triggered(self):
        self.importWorkbook(say='Import from file...')
    
    #Import to workbook
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
                tables = [data, self.Entities_Point, self.Entities_Link, self.Entities_Chain,
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
    
    #Error message when load workbook failed.
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
    
    #Save as function
    @pyqtSlot()
    def on_action_Save_as_triggered(self):
        self.save()
    
    #Save function
    def save(self, fileName=""):
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
        dlg.exec_()
    
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
            "Copy and past this link to web browser:\n", url+'\n',
            "If you have installed Microsoft Silverlight in Internet Explorer as default browser, "+
            "just click \"Open\" button to open it in PMKS web version."
        ])
        dlg = QMessageBox(QMessageBox.Information, "PMKS web server", text, (QMessageBox.Open | QMessageBox.Close), self)
        dlg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        dlg.show()
        if dlg.exec()==QMessageBox.Open:
            self.OpenURL(url)
    
    '''Entities'''
    #Add point group using alt key.
    def qAddPointGroup(self, fixed=False):
        if not self.DimensionalSynthesis.isChecked():
            self.addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
        else:
            self.PathSolving_add_rightClick()
    
    #Add a point group (not fixed).
    def addPointGroup(self):
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, False)
    
    #Add a point group (fixed).
    def addPointGroup_fixed(self):
        self.addPoint(self.mouse_pos_x, self.mouse_pos_y, True)
    
    #Add an ordinary point.
    def addPoint(self, x, y, fixed=False, color=''):
        Args = ['ground' if fixed else '', 'R', color if color else ('Blue' if fixed else 'Green'), x, y]
        rowCount = self.Entities_Point.rowCount()
        self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
        self.FileState.push(addTableCommand(self.Entities_Point))
        self.FileState.push(editPointTableCommand(self.Entities_Point, rowCount, self.Entities_Link, Args))
        self.FileState.endMacro()
        return rowCount
    
    @pyqtSlot(list)
    def addLinkGroup(self, points):
        name = 'link_0'
        names = [self.Entities_Link.item(row, 0).text() for row in range(self.Entities_Link.rowCount())]
        i = 0
        while name in names:
            i += 1
            name = 'link_{}'.format(i)
        Args = [name, 'Blue', ','.join(['Point{}'.format(i) for i in points])]
        self.FileState.beginMacro("Add {{Link: {}}}".format(name))
        self.FileState.push(addTableCommand(self.Entities_Link))
        self.FileState.push(editLinkTableCommand(self.Entities_Link, self.Entities_Link.rowCount()-1, self.Entities_Point, Args))
        self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        self.editPoint()
    
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self):
        pos = self.Entities_Point.currentRow()
        pos = pos if pos>-1 else 0
        self.editPoint(pos)
    
    def editPoint(self, pos=False):
        dlg = edit_point_show(self.Entities_Point.data(), self.Entities_Link.data(), pos, self)
        dlg.show()
        if dlg.exec_():
            rowCount = self.Entities_Point.rowCount()
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
                self.FileState.push(addTableCommand(self.Entities_Point))
                pos = rowCount
            else:
                self.FileState.beginMacro("Edit {{Point{}}}".format(rowCount))
            self.FileState.push(editPointTableCommand(self.Entities_Point, pos, self.Entities_Link, Args))
            self.FileState.endMacro()
    
    def lockPoint(self):
        pos = self.Entities_Point.currentRow()
        Links = self.Entities_Point.item(pos, 1).text().split(',')
        if 'ground' in Links:
            Links.remove('ground')
        else:
            Links.append('ground')
        Args = [
            ','.join(filter(lambda a: a!='', Links)),
            self.Entities_Point.item(pos, 2).text(),
            self.Entities_Point.item(pos, 3).text(),
            self.Entities_Point.item(pos, 4).text(),
            self.Entities_Point.item(pos, 5).text()
        ]
        self.FileState.beginMacro("Edit {{Point{}}}".format(pos))
        self.FileState.push(editPointTableCommand(self.Entities_Point, pos, self.Entities_Link, Args))
        self.FileState.endMacro()
    
    def copyPoint(self):
        pos = self.Entities_Point.currentRow()
        Args = [
            self.Entities_Point.item(pos, 1).text(),
            self.Entities_Point.item(pos, 2).text(),
            'Orange',
            self.Entities_Point.item(pos, 4).text(),
            self.Entities_Point.item(pos, 5).text()
        ]
        rowCount = self.Entities_Point.rowCount()
        self.FileState.beginMacro("Add {{Point{}}}".format(rowCount))
        self.FileState.push(addTableCommand(self.Entities_Point))
        self.FileState.push(editPointTableCommand(self.Entities_Point, rowCount, self.Entities_Link, Args))
        self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_New_Link_triggered(self):
        selectedRows = self.Entities_Point.selectedRows()
        if len(selectedRows)>1:
            self.addLinkGroup(selectedRows)
        else:
            self.editLineDlg()
    
    @pyqtSlot()
    def on_action_Edit_Link_triggered(self):
        pos = self.Entities_Link.currentRow()
        pos = pos if pos>0 else 1
        self.editLineDlg(pos)
    
    def editLineDlg(self, pos=False):
        dlg = edit_link_show(self.Entities_Point.data(), self.Entities_Link.data(), pos, self)
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
                self.FileState.push(addTableCommand(self.Entities_Link))
                pos = self.Entities_Link.rowCount()-1
            else:
                self.FileState.beginMacro("Edit {{Link: {}}}".format(name))
            self.FileState.push(editLinkTableCommand(self.Entities_Link, pos, self.Entities_Point, Args))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self):
        pos = self.Entities_Point.currentRow()
        pos = self.deleteDlg(self.action_New_Point.icon(), self.Entities_Point, pos if pos>-1 else 0)
        if pos is not None:
            pointArgs = [
                '',
                self.Entities_Point.item(pos, 2).text(),
                self.Entities_Point.item(pos, 3).text(),
                self.Entities_Point.item(pos, 4).text(),
                self.Entities_Point.item(pos, 5).text()
            ]
            self.FileState.beginMacro("Delete {{Point{}}}".format(pos))
            self.FileState.push(editPointTableCommand(self.Entities_Point, pos, self.Entities_Link, pointArgs))
            for i in range(self.Entities_Link.rowCount()):
                self.FileState.push(fixSequenceNumberCommand(self.Entities_Link, i, pos))
            self.FileState.push(deleteTableCommand(self.Entities_Point, pos, isRename=True))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_action_Delete_Link_triggered(self):
        pos = self.Entities_Link.currentRow()
        if pos>0:
            pos = self.deleteDlg(self.action_New_Link.icon(), self.Entities_Link, pos)
            if pos is not None:
                Args = [
                    self.Entities_Link.item(pos, 0).text(),
                    self.Entities_Link.item(pos, 1).text(),
                    ''
                ]
                self.FileState.beginMacro("Delete {{Link: {}}}".format(self.Entities_Link.item(pos, 0).text()))
                self.FileState.push(editLinkTableCommand(self.Entities_Link, pos, self.Entities_Point, Args))
                self.FileState.push(deleteTableCommand(self.Entities_Link, pos, isRename=False))
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
        dlg = batchMoving_show(self.Entities_Point.data(), self.Entities_Point.selectedRows(), self)
        dlg.show()
        if dlg.exec_():
            points = [int(dlg.selected.item(row).text().replace('Point', '')) for row in range(dlg.selected.count())]
            self.FileState.beginMacro("Batch moving {{Point {}}}".format(points))
            for row in points:
                Args = [
                    self.Entities_Point.item(row, 1).text(),
                    self.Entities_Point.item(row, 2).text(),
                    self.Entities_Point.item(row, 3).text(),
                    float(self.Entities_Point.item(row, 4).text())+dlg.XIncrease.value(),
                    float(self.Entities_Point.item(row, 5).text())+dlg.YIncrease.value()
                ]
                self.FileState.push(editPointTableCommand(self.Entities_Point, row, self.Entities_Link, Args))
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
        dlgbox.exec_()
    
    @pyqtSlot(int)
    def setZoomBar(self, val):
        self.ZoomBar.setValue(val)
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setText('{}%'.format(value))
    
    #Wheel Event
    def wheelEvent(self, event):
        if self.DynamicCanvasView.underMouse():
            a = event.angleDelta().y()
            self.ZoomBar.setValue(self.ZoomBar.value() + self.ScaleFactor.value()*a/abs(a))
    
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
        for i in range(self.Entities_Point.rowCount()):
            self.inputs_points.addItem("[{}] Point{}".format(self.Entities_Point.item(i, 2).text(), i))
    
    @pyqtSlot(tuple)
    def inputs_points_setSelection(self, selections):
        self.inputs_points.setCurrentRow(selections[0])
    
    @pyqtSlot()
    def inputs_points_clearSelection(self):
        self.inputs_points.setCurrentRow(-1)
    
    @pyqtSlot(int)
    def on_inputs_points_currentRowChanged(self, row):
        if not row in self.Entities_Point.selectedRows():
            self.Entities_Point.setSelections((row,))
        self.inputs_baseLinks.clear()
        if row>-1:
            for linkName in self.Entities_Point.item(row, 1).text().split(','):
                self.inputs_baseLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_baseLinks_currentRowChanged(self, row):
        self.inputs_driveLinks.clear()
        if row>-1:
            for linkName in self.Entities_Point.item(self.inputs_points.currentRow(), 1).text().split(','):
                if linkName==self.inputs_baseLinks.currentItem().text():
                    continue
                self.inputs_driveLinks.addItem(linkName)
    
    @pyqtSlot(int)
    def on_inputs_driveLinks_currentRowChanged(self, row):
        if row>-1:
            typeText = self.inputs_points.currentItem().text().split(" ")[0]
            self.inputs_variable_add.setEnabled(typeText=='[R]')
        else:
            self.inputs_variable_add.setEnabled(False)
    
    @pyqtSlot()
    def on_inputs_variable_add_clicked(self):
        row = self.inputs_points.currentRow()
        Point = self.Entities_Point.data()
        Link = self.Entities_Link.data()
        LinkIndex = [vlink.name for vlink in Link]
        relate = Link[LinkIndex.index(self.inputs_driveLinks.currentItem().text())].points
        base = Point[row]
        drive = Point[relate[relate.index(row)-1]]
        text = '->'.join([
            self.Entities_Point.item(self.inputs_baseLinks.currentRow(), 0).text(),
            self.inputs_baseLinks.currentItem().text(),
            self.inputs_driveLinks.currentItem().text(),
            str(base.slopeAngle(drive))
        ])
        if self.inputs_variable.count()<self.DOF and not(self.inputs_variable.findItems(text, Qt.MatchExactly)):
            self.inputs_variable.addItem(text)
    
    @pyqtSlot()
    def on_inputs_variable_remove_clicked(self):
        row = self.inputs_variable.currentRow()
        if row>-1:
            self.inputs_variable.takeItem(row)
    
    def inputs_variable_autoremove(self):
        for i in range(self.inputs_variable.count()):
            itemText = self.inputs_variable.item(i).text().split('->')
            row = int(itemText[0].replace('Point', ''))
            links = self.Entities_Point.item(row, 1).text()
            if (itemText[1] in links) and (itemText[2] in links):
                self.inputs_variable.takeItem(i)
    
    @pyqtSlot(int)
    def on_inputs_variable_currentRowChanged(self, row):
        enabled = row>-1
        self.inputs_Degree.setEnabled(enabled)
        self.inputs_Degree.setValue(float(self.inputs_variable.currentItem().text().split('->')[-1])*100. if enabled else 0.)
    
    #Update the value when rotating QDial.
    def variableValueUpdate(self, value):
        item = self.inputs_variable.currentItem()
        if item:
            itemText = item.text().split('->')
            itemText[-1] = str(value/100.)
            item.setText('->'.join(itemText))
            self.Resolve()
    
    #Generate constraint symbols.
    def variableConstraints(self):
        constraints = []
        for i in range(self.inputs_variable.count()):
            item = self.inputs_variable.item(i)
            itemText = item.text().split('->')
            itemText[0] = int(itemText[0].replace('Point', ''))
            itemText[-1] = float(itemText[-1])
            constraints.append(tuple(itemText))
        return tuple(constraints)
    
    @pyqtSlot()
    def on_DimensionalSynthesis_clicked(self):
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        self.DynamicCanvasView.showSlvsPath = not self.DimensionalSynthesisGroupBox.title() in tabNameList
        if self.DimensionalSynthesisGroupBox.title() in tabNameList:
            self.closePanel(tabNameList.index(self.DimensionalSynthesisGroupBox.title()))
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
            self.panelWidget.addTab(panel, self.DimensionalSynthesis.icon(), self.DimensionalSynthesisGroupBox.title())
            self.panelWidget.setCurrentIndex(self.panelWidget.count()-1)
        self.Reload_Canvas()
    def PathSolving_add_rightClick(self):
        x = self.mouse_pos_x
        y = self.mouse_pos_y
        tabNameList = [self.panelWidget.tabText(i) for i in range(self.panelWidget.count())]
        self.panelWidget.widget(tabNameList.index(self.DimensionalSynthesisGroupBox.title())).addPath(x, y)
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
    @pyqtSlot(tuple, dict)
    def PathSolving_mergeResult(self, answer, Paths):
        pointNum = []
        for i, (x, y) in enumerate(answer):
            pointNum.append(self.addPoint(x, y, i<2))
        for p in pointNum:
            #TODO: Dimensional synthesis link merge function.
            '''
            self.addLinkGroup([])
            '''
    
    def closeAllPanels(self):
        for i in range(self.panelWidget.count()):
            self.closePanel(0)
        for button in [self.NumberAndTypeSynthesis, self.DimensionalSynthesis]:
            button.setChecked(False)
        self.DynamicCanvasView.showSlvsPath = False
        self.Reload_Canvas()
    
    def closePanel(self, pos):
        panel = self.panelWidget.widget(pos)
        self.panelWidget.removeTab(pos)
        panel.deleteLater()
    
    @pyqtSlot()
    def pointSelection(self):
        self.DynamicCanvasView.changePointsSelection(self.Entities_Point.selectedRows())
    
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
        if index>-1 and not self.panelWidget.isVisible():
            self.panelWidget.show()
        else:
            self.panelWidget.hide()
