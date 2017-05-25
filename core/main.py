# -*- coding: utf-8 -*-
##Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.
##Copyright (C) 2016 Yuan Chang
##E-mail: daan0014119@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from .QtModules import *
from .main_modules import *
_translate = QCoreApplication.translate
from .Ui_main import Ui_MainWindow
from .Ui_custom import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.args = args
        #Console Widget
        if not self.args.debug_mode: self.on_connectButton_clicked()
        #File & Default Setting
        FileState = QUndoStack()
        FileState.indexChanged.connect(self.commandReload)
        showUndoWindow(self, FileState)
        self.File = File(FileState, self.args)
        self.setLocate(QFileInfo(self.args.i if self.args.i else '.').canonicalFilePath())
        #QPainter Window
        self.DynamicCanvasView = DynamicCanvas()
        self.DynamicCanvasView.mouse_getClick.connect(self.addPointGroup)
        self.DynamicCanvasView.zoom_change.connect(self.setZoomBar)
        self.mplLayout.insertWidget(0, self.DynamicCanvasView)
        self.DynamicCanvasView.show()
        self.Resolve()
        #Solve & DOF & Mask
        self.Solvefail = False
        self.DOF = 0
        self.FocusTable = None
        self.MaskChange()
        self.Parameter_digital.setValidator(self.Mask)
        init_Right_click_menu(self)
        action_Enabled(self)
        if self.args.r: self.loadWorkbook("Loading by Argument.", fileName=self.args.r)
    
    def setLocate(self, locate):
        self.Default_Environment_variables = locate
        print("~Start at: [{}]".format(self.Default_Environment_variables))
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            for url in mimeData.urls():
                FilePath = url.toLocalFile()
                if QFileInfo(FilePath).suffix() in ['xml', 'csv']: event.acceptProposedAction()
    def dropEvent(self, event):
        FilePath = event.mimeData().urls()[-1].toLocalFile()
        self.checkChange(FilePath, list(), "Loaded drag-in file: [{}]".format(FilePath))
        event.acceptProposedAction()
    
    #Mouse position on canvace
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    #TODO: Right-click menu event
    def on_painter_context_menu(self, point):
        self.action_painter_right_click_menu_path.setVisible(self.PathSolving.isChecked())
        action = self.popMenu_painter.exec_(self.DynamicCanvasView.mapToGlobal(point))
        table1 = self.Entiteis_Point
        x = self.mouse_pos_x
        y = self.mouse_pos_y
        if action==self.action_painter_right_click_menu_add: self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), False, 'Green')
        elif action==self.action_painter_right_click_menu_fix_add: self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), True, 'Blue')
        elif action==self.action_painter_right_click_menu_path: self.PathSolving_add_rightClick(x, y)
    def on_point_context_menu(self, point):
        table1 = self.Entiteis_Point
        NOT_ORIGIN = table1.rowCount()>1 and table1.currentRow()!=0
        self.action_point_right_click_menu_delete.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_edit.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_lock.setEnabled(NOT_ORIGIN)
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        table_pos = table1.currentRow() if table1.currentRow()>=1 else 1
        table_pos_0 = table1.currentRow()
        if action==self.action_point_right_click_menu_copy: self.Coordinate_Copy(table1)
        elif action==self.action_point_right_click_menu_copyPoint: self.File.Lists.editTable(table1, 'Point', False,
            table1.item(table_pos_0, 1).text(), table1.item(table_pos_0, 2).text(), table1.item(table_pos_0, 3).checkState()==Qt.Checked, 'Orange')
        elif action==self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action==self.action_point_right_click_menu_edit: self.on_action_Edit_Point_triggered(table_pos)
        elif action==self.action_point_right_click_menu_lock:
            self.File.Lists.editTable(table1, 'Point', table_pos_0,
                str(self.File.Lists.PointList[table_pos_0]['x']), str(self.File.Lists.PointList[table_pos_0]['y']), not(self.File.Lists.PointList[table_pos_0]['fix']), 'Green')
        elif action==self.action_point_right_click_menu_replace: self.on_action_Replace_Point_triggered(table_pos_0)
        elif action==self.action_point_right_click_menu_delete: self.on_action_Delete_Point_triggered(table_pos)
    def on_link_context_menu(self, point):
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Link.currentRow()
        if self.Entiteis_Link.currentRow()!=-1:
            currentLine = self.File.Lists.LineList[table_pos]
            self.action_link_right_click_menu_shaft.setEnabled(self.File.Lists.PointList[currentLine.start].fix!=self.File.Lists.PointList[currentLine.end].fix)
        else: self.action_link_right_click_menu_shaft.setEnabled(False)
        if action==self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action==self.action_link_right_click_menu_edit: self.on_action_Edit_Linkage_triggered(table_pos)
        elif action==self.action_link_right_click_menu_shaft: self.File.Lists.link2Shaft(self.Shaft, table_pos)
        elif action==self.action_link_right_click_menu_delete: self.on_action_Delete_Linkage_triggered(table_pos)
    def on_chain_context_menu(self, point):
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Stay_Chain.currentRow()
        if action==self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action==self.action_chain_right_click_menu_edit: self.on_action_Edit_Stay_Chain_triggered(table_pos)
        elif action==self.action_chain_right_click_menu_delete: self.on_action_Delete_Stay_Chain_triggered(table_pos)
    def on_shaft_context_menu(self, point):
        action = self.popMenu_shaft.exec_(self.Shaft_Widget.mapToGlobal(point))
        table_pos = self.Shaft.currentRow()
        if action==self.action_shaft_right_click_menu_add: self.on_action_Set_Shaft_triggered()
        elif action==self.action_shaft_right_click_menu_edit: self.on_action_Edit_Shaft_triggered(table_pos)
        elif action==self.action_shaft_right_click_menu_delete: self.on_action_Delete_Shaft_triggered(table_pos)
    def on_slider_context_menu(self, point):
        action = self.popMenu_slider.exec_(self.Slider_Widget.mapToGlobal(point))
        table_pos = self.Slider.currentRow()
        if action==self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action==self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered(table_pos)
        elif action==self.action_slider_right_click_menu_delete: self.on_action_Delete_Slider_triggered(table_pos)
    def on_rod_context_menu(self, point):
        action = self.popMenu_rod.exec_(self.Rod_Widget.mapToGlobal(point))
        table_pos = self.Rod.currentRow()
        if action==self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action==self.action_rod_right_click_menu_edit: self.on_action_Edit_Rod_triggered(table_pos)
        elif action==self.action_rod_right_click_menu_delete: self.on_action_Delete_Piston_Spring_triggered(table_pos)
    
    #Close Event
    def closeEvent(self, event):
        if self.File.form.changed:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_action_Save_triggered()
                if self.File.form.changed: event.ignore()
                else: self.Exit(event)
            elif reply==QMessageBox.Discard: self.Exit(event)
            else: event.ignore()
        else: self.Exit(event)
    def Exit(self, event):
        self.disconnectConsole()
        print('Exit.')
        event.accept()
    
    #TODO: Undo and Redo
    @pyqtSlot(int)
    def commandReload(self, index=0):
        self.File.Lists.updateAll(self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Shaft, self.Slider, self.Rod, self.Parameter_list)
        self.action_Undo.setText("Undo {}".format(self.File.FileState.undoText()))
        self.action_Redo.setText("Redo {}".format(self.File.FileState.redoText()))
        if index!=self.File.form.Stack: self.workbookNoSave()
        else: self.workbookSaved()
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Triangle Solver" in tabNameList: self.PointTab.widget(tabNameList.index("Triangle Solver")).setPoint(self.File.Lists.PointList)
        self.Resolve()
    
    #Resolve
    def Resolve(self):
        Point, Line, Chain, Shaft, Slider, Rod = self.File.Obstacles_Exclusion()
        result, DOF = slvsProcess(Point, Line, Chain, Shaft, Slider, Rod, hasWarning=self.args.w)
        Failed = type(DOF)!=int
        self.ConflictGuide.setVisible(Failed)
        self.DOFview.setVisible(not Failed)
        if not Failed:
            self.Solvefail = False
            self.File.Lists.currentPos(self.Entiteis_Point, result)
            self.DOF = DOF
            self.DOFview.setText("{} ({})".format(self.DOF-6+self.Shaft.rowCount(), self.DOF-6))
            self.DOFLable.setText("<html><head/><body><p><span style=\" color:#000000;\">DOF:</span></p></body></html>")
            self.Reload_Canvas()
        else:
            self.Solvefail = True
            self.DOFLable.setText("<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">DOF:</span></p></body></html>")
            self.ConflictGuide.setToolTip(DOF)
            self.Reload_Canvas()
    #Reload Canvas
    def Reload_Canvas(self):
        self.DynamicCanvasView.update_figure(
            float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList,
            self.ZoomBar.value(), self.Font_size.value(), self.action_Display_Dimensions.isChecked(), self.action_Display_Point_Mark.isChecked(), self.File.Lists.pathData)
    
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
    def on_action_Get_Help_triggered(self): self.OpenURL("http://mde.tw")
    @pyqtSlot()
    def on_action_Pyslvs_com_triggered(self): self.OpenURL("https://pyslvs.com")
    @pyqtSlot()
    def on_action_Git_hub_Site_triggered(self): self.OpenURL("https://github.com/KmolYuan/python-solvespace")
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        dlg = version_show(self)
        splash = Pyslvs_Splash()
        splash.show()
        self.OpenDlg(dlg)
        splash.finish(dlg)
    @pyqtSlot()
    def on_action_About_Qt_triggered(self): QMessageBox.aboutQt(self)
    def OpenURL(self, URL):
        print("Open - {{{}}}".format(URL))
        webbrowser.open(URL)
    
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        Point, Line, Chain, Shaft, Slider, Rod = self.File.Obstacles_Exclusion()
        self.OpenDlg(Script_Dialog(self.File.form.fileName.baseName(), Point, Line, Chain, Shaft, Slider, Rod, self.Default_Environment_variables, self))
    @pyqtSlot()
    def on_action_Search_Points_triggered(self): self.OpenDlg(Association_show(self.File.Lists.PointList, self.File.Lists.LineList,
        self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self))
    def OpenDlg(self, dlg):
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_action_Console_triggered(self):
        self.OptionTab.setCurrentIndex(2)
        self.History_tab.setCurrentIndex(1)
    
    #TODO: Example
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self): self.checkChange("[New Workbook]", example.new_workbook(), 'Generating New Workbook...')
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self): self.checkChange(say='Open file...', isFile=True)
    @pyqtSlot()
    def on_action_Crank_rocker_triggered(self): self.checkChange("[Example] Crank Rocker", example.crankRocker())
    @pyqtSlot()
    def on_action_Drag_link_triggered(self): self.checkChange("[Example] Drag-link", example.DragLink())
    @pyqtSlot()
    def on_action_Double_rocker_triggered(self): self.checkChange("[Example] Double Rocker", example.doubleRocker())
    @pyqtSlot()
    def on_action_Parallelogram_linkage_triggered(self): self.checkChange("[Example] Parallelogram Linkage", example.parallelogramLinkage())
    @pyqtSlot()
    def on_action_Multiple_Link_triggered(self): self.checkChange("[Example] Multiple Link", example.multipleLink())
    @pyqtSlot()
    def on_action_Two_Multiple_Link_triggered(self): self.checkChange("[Example] Two Pairs Multiple Link", example.twoMultipleLink())
    @pyqtSlot()
    def on_action_Four_bar_linkage_triggered(self): self.checkChange("[Example] Four bar linkage", example.FourBarFeet())
    @pyqtSlot()
    def on_action_Slider_and_Rod_triggered(self): self.checkChange("[Example] Slider and Rod", example.sliderRod())
    @pyqtSlot()
    def on_action_Rock_Slider_triggered(self): self.checkChange("[Example] Rock Slider", example.rockSlider())
    @pyqtSlot()
    def on_action_Lift_Tailgate_triggered(self): self.checkChange("[Example] Lift Tailgate", example.liftTailgate())
    @pyqtSlot()
    def on_action_Theo_Jansen_s_multi_linkage_triggered(self): self.checkChange("[Example] Theo Jansen\'s multiple linkage", example.TJLinkage())
    @pyqtSlot()
    def on_action_Rock_Slider_Design_triggered(self): self.checkChange("[Example] Rock slider design", example.RockSliderDesign())
    @pyqtSlot()
    def on_action_Reverse_Parsing_Rocker_triggered(self): self.checkChange("[Example] Reverse Parsing Rocker", example.reverseParsingRocker())
    @pyqtSlot()
    def on_action_Three_Algorithm_Result_triggered(self): self.checkChange("[Example] Three algorithm result", example.threeAlgorithmResult())
    #Workbook Functions
    def checkChange(self, name='', data=list(), say='Loading Example...', isFile=False):
        if self.File.form.changed:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit this file?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_action_Save_triggered()
                if not self.File.form.changed: self.loadWorkbook(say, name, data, isFile)
            elif reply==QMessageBox.Discard: self.loadWorkbook(say, name, data, isFile)
        else: self.loadWorkbook(say, name, data, isFile)
    def loadWorkbook(self, say, fileName='', data=list(), isFile=False):
        if isFile:
            data.clear()
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, "XML File(*.xml);;CSV File(*.csv)")
            if fileName: self.setLocate(QFileInfo(fileName).absolutePath())
        if fileName or isFile==False:
            print(say)
            self.closeAllPanels(True)
            self.File.reset(self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Shaft, self.Slider, self.Rod, self.Parameter_list)
            self.DynamicCanvasView.changeCurrentShaft()
            self.DynamicCanvasView.path_solving()
            self.Resolve()
            self.X_coordinate.clear()
            self.Y_coordinate.clear()
            self.setWindowTitle("Pyslvs - [New Workbook]")
            print("Reset workbook.")
            checkdone, data = self.File.check(fileName, data)
            if checkdone:
                errorInfo = self.File.read(fileName, data,
                    self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Shaft, self.Slider, self.Rod, self.Parameter_list)
                if errorInfo: print("The following content(s) contain errors:\n+ {{{}}}".format(', '.join(errorInfo)))
                else: print("Successful loaded contents of the file.")
                self.workbookSaved()
                self.DynamicCanvasView.SetIn()
                print("Loaded the workbook.")
                if '[New Workbook]' in fileName and isFile==False: self.on_action_Property_triggered()
                else:
                    self.show_Property(errorInfo)
                    if errorInfo: self.on_action_Console_triggered()
            else: self.loadWorkbookError(fileName)
    
    @pyqtSlot()
    def on_action_Import_From_Workbook_triggered(self): self.importWorkbook(say='Import from file...')
    def importWorkbook(self, say, fileName=False, data=list()):
        if fileName==False:
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, "XML File(*.xml);;CSV File(*.csv)")
            if fileName: self.setLocate(QFileInfo(fileName).absolutePath())
        if fileName:
            print(say)
            checkdone, data = self.File.check(fileName, data)
            if checkdone:
                suffix = QFileInfo(fileName).suffix().lower()
                tables = [data, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Shaft, self.Slider, self.Rod, self.Parameter_list]
                if suffix=='xml': errorInfo = self.File.readXMLMerge(*tables)
                elif suffix=='csv': errorInfo = self.File.readCSVMerge(*tables)
                self.show_Property(errorInfo)
                if errorInfo: self.on_action_Console_triggered()
            else: self.loadWorkbookError(fileName)
    def loadWorkbookError(self, fileName):
        dlgbox = QMessageBox(QMessageBox.Warning, "Loading failed", "File:\n{}\n\nYour data sheet is an incorrect format.".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_(): print("Error: Incorrect format.")
    
    #TODO: Save format
    @pyqtSlot()
    def on_action_Save_triggered(self):
        fileName = self.File.form.fileName.absoluteFilePath()
        suffix = QFileInfo(fileName).suffix()
        self.save('' if suffix!='csv' and suffix!='xml' else fileName)
    @pyqtSlot()
    def on_action_Save_as_triggered(self): self.save()
    def save(self, fileName=str()):
        if bool(fileName)==False: fileName = self.outputTo("Workbook", ["XML File(*.xml)", "CSV File(*.csv)"])
        if fileName:
            self.File.write(fileName)
            self.replyBox('Workbook', fileName)
            self.workbookSaved()
    
    @pyqtSlot()
    def on_action_Save_path_only_triggered(self):
        fileName = self.outputTo("Path-Only Workbook", ["XML File(*.xml)", "CSV File(*.csv)"])
        if fileName:
            self.File.writePathOnly(fileName)
            self.replyBox('Solvespace Sketch', fileName)
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        dlg = slvsTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_(): self.replyBox('Solvespace Models', dlg.folderPath.absolutePath())
    @pyqtSlot()
    def on_action_Solvespace_2D_sketch_triggered(self):
        fileName = self.outputTo("Solvespace sketch", ['Solvespace module(*.slvs)'])
        if fileName:
            content = slvs2D(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f: f.write(content)
            self.replyBox('Solvespace Sketch', fileName)
    @pyqtSlot()
    def on_action_DXF_2D_models_triggered(self):
        dlg = dxfTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_(): self.replyBox('DXF 2D Models', dlg.filePath)
    @pyqtSlot()
    def on_action_DXF_2D_sketch_triggered(self):
        fileName = self.outputTo("DXF", ['AutoCAD DXF (*.dxf)'])
        if fileName:
            dxfSketch(fileName, self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            self.replyBox('DXF 2D Sketch', fileName)
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        fileName = self.outputTo("picture", ["Portable Network Graphics (*.png)", "Joint Photographic Experts Group (*.jpg)", "Bitmap Image file (*.bmp)",
            "Business Process Model (*.bpm)", "Tagged Image File Format (*.tiff)", "Windows Icon (*.ico)", "Wireless Application Protocol Bitmap (*.wbmp)",
            "X BitMap (*.xbm)", "X Pixmap (*.xpm)"])
        if fileName:
            pixmap = self.DynamicCanvasView.grab()
            pixmap.save(fileName, format = QFileInfo(fileName).suffix())
            self.replyBox('Picture', fileName)
    def outputTo(self, formatName, formatChoose):
        suffix0 = formatChoose[0].split('*')[-1][:-1]
        fileName, form = QFileDialog.getSaveFileName(self, 'Save file...',
            self.Default_Environment_variables+'/'+self.File.form.fileName.baseName()+suffix0, ';;'.join(formatChoose))
        if fileName:
            if QFileInfo(fileName).suffix()!=suffix0[1:]: fileName = fileName+suffix0
            self.setLocate(QFileInfo(fileName).absolutePath())
            print("Formate: {}".format(form))
        return fileName
    def replyBox(self, title, fileName):
        dlgbox = QMessageBox(QMessageBox.Information, title, "Successfully converted:\n{}".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_(): print("Successful saved {}.".format(title))
    
    def show_Property(self, errorInfo):
        dlg = fileInfo_show(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description,
            self.File.form.lastTime, self.File.Designs.result, errorInfo, self)
        dlg.show()
        if dlg.exec_(): pass
    @pyqtSlot()
    def on_action_Property_triggered(self):
        dlg = editFileInfo_show(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description,
            self.File.form.lastTime, self.File.Designs.result, self)
        dlg.show()
        if dlg.exec_():
            self.File.updateAuthorDescription(dlg.authorName_input.text(), dlg.descriptionText.toPlainText())
            self.workbookNoSave()
    
    @pyqtSlot(int, int)
    def on_Entiteis_Point_cellDoubleClicked(self, row, column):
        if row>0: self.on_action_Edit_Point_triggered(row)
    @pyqtSlot(int, int)
    def on_Entiteis_Link_cellDoubleClicked(self, row, column): self.on_action_Edit_Linkage_triggered(row)
    @pyqtSlot(int, int)
    def on_Entiteis_Stay_Chain_cellDoubleClicked(self, row, column): self.on_action_Edit_Stay_Chain_triggered(row)
    @pyqtSlot(int, int)
    def on_Shaft_cellDoubleClicked(self, row, column): self.on_action_Edit_Shaft_triggered(row)
    @pyqtSlot(int, int)
    def on_Slider_cellDoubleClicked(self, row, column): self.on_action_Edit_Slider_triggered(row)
    @pyqtSlot(int, int)
    def on_Rod_cellDoubleClicked(self, row, column): self.on_action_Edit_Rod_triggered(row)
    
    #Entities
    def addPointGroup(self):
        if not self.PathSolving.isChecked():
            table = self.Entiteis_Point
            self.File.Lists.editTable(table, 'Point', False, str(self.mouse_pos_x), str(self.mouse_pos_y), False, 'Green')
            self.File.Lists.clearPath()
        else: self.PathSolving_add_rightClick(self.mouse_pos_x, self.mouse_pos_y)
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table = self.Entiteis_Point
        x = self.X_coordinate.text() if not self.X_coordinate.text() in [str(), "n", "-"] else self.X_coordinate.placeholderText()
        y = self.Y_coordinate.text() if not self.Y_coordinate.text() in [str(), "n", "-"] else self.Y_coordinate.placeholderText()
        self.File.Lists.editTable(table, 'Point', False, x, y, False, 'Green')
        self.X_coordinate.clear()
        self.Y_coordinate.clear()
        self.File.Lists.clearPath()
    @pyqtSlot(int, int, int, int)
    def on_Entiteis_Point_currentCellChanged(self, c0, c1, p0, p1):
        self.X_coordinate.setPlaceholderText(self.Entiteis_Point.item(c0, 1).text())
        self.Y_coordinate.setPlaceholderText(self.Entiteis_Point.item(c0, 2).text())
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self): self.editPoint()
    @pyqtSlot()
    def on_action_Edit_Point_triggered(self, pos=1): self.editPoint(pos)
    def editPoint(self, pos=False):
        dlg = edit_point_show(self.Mask, self.File.Lists.PointList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            self.File.Lists.editTable(self.Entiteis_Point, 'Point', False if pos is False else dlg.Point.currentIndex()+1,
                dlg.X_coordinate.text() if not dlg.X_coordinate.text() in [str(), 'n', '-'] else dlg.X_coordinate.placeholderText(),
                dlg.Y_coordinate.text() if not dlg.Y_coordinate.text() in [str(), 'n', '-'] else dlg.Y_coordinate.placeholderText(),
                bool(dlg.Fix_Point.checkState()), dlg.Color.currentText())
            self.closeAllPanels()
    @pyqtSlot()
    def on_action_Update_all_points_triggered(self): self.File.Lists.coverageCoordinate(self.Entiteis_Point)
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self): self.editLine()
    @pyqtSlot()
    def on_action_Edit_Linkage_triggered(self, pos=0): self.editLine(pos)
    def editLine(self, pos=False):
        dlg = edit_link_show(self.Mask, self.File.Lists.PointList, self.File.Lists.LineList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            if dlg.isReplace.isChecked(): self.checkEntitiesConflict(pos, [dlg.Start_Point.currentIndex(), dlg.End_Point.currentIndex()])
            self.File.Lists.editTable(self.Entiteis_Link, 'Line', False if pos is False else dlg.Link.currentIndex(),
                dlg.Start_Point.currentIndex(), dlg.End_Point.currentIndex(), dlg.len)
            self.closeAllPanels()
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self): self.editChain()
    @pyqtSlot()
    def on_action_Edit_Stay_Chain_triggered(self, pos=0): self.editChain(pos)
    def editChain(self, pos=False):
        dlg = edit_chain_show(self.Mask, self.File.Lists.PointList, self.File.Lists.ChainList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            if dlg.isReplace.isChecked(): self.checkEntitiesConflict(pos, [dlg.p1, dlg.p2, dlg.p3])
            self.File.Lists.editTable(self.Entiteis_Stay_Chain, 'Chain', False if pos is False else dlg.Chain.currentIndex(),
                dlg.p1, dlg.p2, dlg.p3, dlg.p1_p2Val, dlg.p2_p3Val, dlg.p1_p3Val)
            self.closeAllPanels()
    
    def checkEntitiesConflict(self, pos, points):
        for i, e in enumerate(self.File.Lists.LineList):
            if len(set(points) & set([e.start, e.end]))>1 and (i!=pos or len(points)!=2): self.File.Lists.deleteTable(
                self.Entiteis_Link, 'Line', i)
        for i, e in enumerate(self.File.Lists.ChainList):
            if len(set(points) & set([e.p1, e.p2, e.p3]))>1 and (i!=pos or len(points)!=3): self.File.Lists.deleteTable(
                self.Entiteis_Stay_Chain, 'Chain', i)
    
    #Simulate
    @pyqtSlot()
    def on_action_Set_Shaft_triggered(self): self.editShaft()
    @pyqtSlot()
    def on_action_Edit_Shaft_triggered(self, pos=0): self.editShaft(pos)
    def editShaft(self, pos=False):
        dlg = edit_shaft_show(self.File.Lists.PointList, self.File.Lists.ShaftList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            self.File.Lists.editTable(self.Shaft, 'Shaft', False if pos is False else dlg.Shaft.currentIndex(),
                dlg.center, dlg.ref, dlg.start, dlg.end, self.File.Lists.m(dlg.center, dlg.ref))
            self.closeAllPanels()
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self): self.editSlider()
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self, pos=0): self.editSlider(pos)
    def editSlider(self, pos=False):
        dlg = edit_slider_show(self.File.Lists.PointList, self.File.Lists.SliderList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            self.File.Lists.editTable(self.Slider, 'Slider', False if pos is False else dlg.Slider.currentIndex(),
                dlg.slider, dlg.start, dlg.end)
            self.closeAllPanels()
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self): self.editRod()
    @pyqtSlot()
    def on_action_Edit_Rod_triggered(self, pos=0): self.editRod(pos)
    def editRod(self, pos=False):
        dlg = edit_rod_show(self.File.Lists.PointList, self.File.Lists.RodList, pos, self)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            self.File.Lists.editTable(self.Rod, 'Rod', False if pos is False else dlg.Rod.currentIndex(),
                dlg.cen, dlg.start, dlg.end, dlg.pos)
            self.closeAllPanels()
    
    #Delete
    @pyqtSlot()
    def on_action_Delete_Point_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Point.currentRow()
        self.deletePanel(self.Entiteis_Point, 'Point', ":/icons/delete.png", ":/icons/point.png", pos)
    @pyqtSlot()
    def on_action_Delete_Linkage_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Link.currentRow()
        self.deletePanel(self.Entiteis_Link, 'Line', ":/icons/deleteline.png", ":/icons/line.png", pos)
    @pyqtSlot()
    def on_action_Delete_Stay_Chain_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Stay_Chain.currentRow()
        self.deletePanel(self.Entiteis_Stay_Chain, 'Chain', ":/icons/deletechain.png", ":/icons/equal.png", pos)
    @pyqtSlot()
    def on_action_Delete_Shaft_triggered(self, pos=None):
        if pos==None: pos = self.Shaft.currentRow()
        self.deletePanel(self.Shaft, 'Shaft', ":/icons/deleteshaft.png", ":/icons/circle.png", pos)
    @pyqtSlot()
    def on_action_Delete_Slider_triggered(self, pos=None):
        if pos==None: pos = self.Slider.currentRow()
        self.deletePanel(self.Slider, 'Slider', ":/icons/deleteslider.png", ":/icons/pointonx.png", pos)
    @pyqtSlot()
    def on_action_Delete_Piston_Spring_triggered(self, pos=None):
        if pos==None: pos = self.Rod.currentRow()
        self.deletePanel(self.Rod, 'Rod', QIcon(QPixmap(":/icons/deleterod.png")), QIcon(QPixmap(":/icons/spring.png")), pos)
    def deletePanel(self, table, name, icon1, icon2, pos):
        dlg = deleteDlg(QIcon(QPixmap(icon1)), QIcon(QPixmap(icon2)), table, pos, self)
        dlg.move(QCursor.pos()-QPoint(dlg.size().width(), dlg.size().height()))
        dlg.show()
        if dlg.exec_():
            self.File.Lists.clearPath()
            if name=='Point': self.File.Lists.deletePointTable(self.Entiteis_Point, self.Entiteis_Link,
                self.Entiteis_Stay_Chain, self.Shaft, self.Slider, self.Rod, dlg.Entity.currentIndex())
            else: self.File.Lists.deleteTable(table, name, dlg.Entity.currentIndex())
            self.closeAllPanels()
    
    @pyqtSlot()
    def on_Parameter_add_clicked(self):
        self.File.Lists.editTable(self.Parameter_list, 'n', False, '0.0', 'No-comment')
        self.MaskChange()
    @pyqtSlot()
    def on_Parameter_update_clicked(self):
        dtext = self.Parameter_digital.text()
        ctext = self.Parameter_comment.text()
        self.File.Lists.editTable(self.Parameter_list, 'n', self.Parameter_list.currentRow(),
            dtext if dtext!='' else self.Parameter_digital.placeholderText(),
            ctext if ctext!='' else self.Parameter_comment.placeholderText())
    @pyqtSlot()
    def on_Parameter_delete_clicked(self):
        pos = self.Parameter_list.currentRow()
        if pos>-1:
            self.File.Lists.deleteParameterTable(self.Parameter_list,
                self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain, pos)
            self.MaskChange()
    
    @pyqtSlot()
    def on_action_Replace_Point_triggered(self, pos=0):
        dlg = replacePoint_show(QIcon(QPixmap(":/icons/point.png")), self.Entiteis_Point, pos, self)
        dlg.move(QCursor.pos()-QPoint(dlg.size().width(), dlg.size().height()))
        dlg.show()
        if dlg.exec_(): self.File.Lists.ChangePoint(self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Shaft, self.Slider, self.Rod,
            dlg.Prv.currentIndex(), dlg.Next.currentIndex())
    
    @pyqtSlot()
    def on_action_Batch_moving_triggered(self):
        dlg = batchMoving_show(self.File.Lists.PointList, self.File.Lists.ParameterList, self)
        dlg.show()
        if dlg.exec_(): self.File.Lists.batchMove(self.Entiteis_Point, dlg.XIncrease.value(), dlg.YIncrease.value(),
            [int(dlg.Move_list.item(e).text().replace('Point', "")) for e in range(dlg.Move_list.count())])
    
    def Coordinate_Copy(self, table):
        clipboard = QApplication.clipboard()
        clipboard.setText(table.currentItem().text())
    
    @pyqtSlot()
    def on_action_Zoom_to_fit_triggered(self): self.DynamicCanvasView.SetIn()
    @pyqtSlot(int)
    def setZoomBar(self, val): self.ZoomBar.setValue(val)
    @pyqtSlot()
    def on_ResetCanvas_clicked(self): self.DynamicCanvasView.SetIn()
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setText('{}%'.format(value))
        self.Reload_Canvas()
    #Wheel Event
    def wheelEvent(self, event):
        if self.DynamicCanvasView.underMouse(): self.ZoomBar.setValue(self.ZoomBar.value()+10*(1 if event.angleDelta().y()>0 else -1))
    
    @pyqtSlot(int)
    def on_LineWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_Font_size_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_PathWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Display_Dimensions_toggled(self, p0):
        if p0: self.action_Display_Point_Mark.setChecked(True)
        self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Display_Point_Mark_toggled(self, p0):
        if not p0: self.action_Display_Dimensions.setChecked(False)
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_action_Path_Track_triggered(self):
        self.closeAllPanels()
        self.on_action_Update_all_points_triggered()
        dlg = Path_Track_show(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList,
            self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self.args.w, self)
        self.action_Display_Point_Mark.setChecked(True)
        dlg.show()
        if dlg.exec_():
            if dlg.ShaftSuggest:
                reply = QMessageBox.question(self, "Angle check results", "The suggested results are as follows:\n\n"+'\n'.join(
                    ['Shaft{}\nStart: {}[deg]\nEnd: {}[deg]\n'.format(i, shaft[0], shaft[1]) for i, shaft in enumerate(dlg.ShaftSuggest)])+
                    "\nSelect \"Apply\" to set the recommended angle.",
                    (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
                if reply==QMessageBox.Apply:
                    for i, shaft in enumerate(dlg.ShaftSuggest):
                        o = self.File.Lists.ShaftList[i]
                        self.File.Lists.editTable(self.Shaft, 'Shaft', i, o.cen, o.ref, shaft[0], shaft[1], o.demo)
            self.File.Lists.setPath(dlg.Path_data)
    @pyqtSlot()
    def on_action_Path_Clear_triggered(self):
        self.File.Lists.clearPath()
        self.closeAllPanels()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_action_Path_coordinate_triggered(self):
        dlg = path_point_data_show(self.Default_Environment_variables, self.File.Lists.pathData, self.File.Lists.PointList)
        dlg.show()
        dlg.exec()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_action_Path_style_triggered(self):
        self.DynamicCanvasView.options.Path.mode = self.action_Path_style.isChecked()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_action_Path_data_show_triggered(self):
        self.DynamicCanvasView.options.Path.show = self.action_Path_data_show.isChecked()
        self.Reload_Canvas()
    
    @pyqtSlot(bool)
    def on_PathSolving_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.DynamicCanvasView.options.slvsPath['show'] = not "Path Solving" in tabNameList
        if "Path Solving" in tabNameList: self.closePanel(tabNameList.index("Path Solving"))
        else:
            panel = Path_Solving_show(self.File.FileState, self.File.Designs.path, self.File.Designs.result, self.width(), self)
            panel.addPathPoint.connect(self.PathSolving_add)
            panel.deletePathPoint.connect(self.PathSolving_delete)
            panel.moveupPathPoint.connect(self.PathSolving_moveup)
            panel.movedownPathPoint.connect(self.PathSolving_movedown)
            panel.mergeResult.connect(self.PathSolving_mergeResult)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/bezier.png")), "Path Solving")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
        self.Reload_Canvas()
    def PathSolving_add_rightClick(self, x, y):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.PointTab.widget(tabNameList.index("Path Solving")).addPath(x, y)
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
    def PathSolving_deleteResult(self, row): self.File.Designs.removeResult(row)
    @pyqtSlot(int)
    def PathSolving_mergeResult(self, row):
        if self.File.Generate_Merge(row, self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Shaft)==False:
            dlgbox = QMessageBox(QMessageBox.Warning, "Error when merge...", "Please check dimension.", (QMessageBox.Ok), self)
            if dlgbox.exec_():
                print("Generate Result Error.")
                self.on_action_Console_triggered()
    
    @pyqtSlot(bool)
    def on_TriangleSolver_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Triangle Solver" in tabNameList: self.closePanel(tabNameList.index("Triangle Solver"))
        else:
            panel = Triangle_Solver_show(self.File.FileState, self.File.Lists.PointList, self.File.Designs.TSDirections, self)
            panel.startMerge.connect(self.TriangleSolver_merge)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/TS.png")), "Triangle Solver")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    @pyqtSlot()
    def TriangleSolver_merge(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.File.TS_Merge(self.PointTab.widget(tabNameList.index("Triangle Solver")).answers,
            self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Slider)
    
    @pyqtSlot()
    def on_Drive_shaft_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.DynamicCanvasView.options.Path.Drivemode = not "Drive Shaft" in tabNameList
        if "Drive Shaft" in tabNameList: self.closePanel(tabNameList.index("Drive Shaft"))
        else:
            isPathDemoMode = bool(self.File.Lists.pathData)
            panel = Drive_shaft_show(self.File.Lists.ShaftList, self.DynamicCanvasView.options.currentShaft, isPathDemoMode, self)
            panel.Degree.valueChanged.connect(self.Change_path_demo_angle if isPathDemoMode else self.Change_demo_angle)
            if not isPathDemoMode: panel.degreeChange.connect(self.Save_demo_angle)
            self.DynamicCanvasView.changePathCurrentShaft()
            panel.Shaft.currentIndexChanged.connect(self.changeCurrentShaft)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/same-orientation.png")), "Drive Shaft")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
        self.Reload_Canvas()
    @pyqtSlot(int)
    def Change_demo_angle(self, angle):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Shaft"))
        self.File.Lists.setDemo('Shaft', row=panel.Shaft.currentIndex(), pos=angle/100)
        self.Resolve()
    @pyqtSlot(int)
    def Change_path_demo_angle(self, angle):
        self.DynamicCanvasView.options.Path.demo = angle/100
        self.Reload_Canvas()
    @pyqtSlot(float, int)
    def Save_demo_angle(self, angle, currentShaft): self.File.Lists.saveDemo(self.Shaft, 'Shaft', angle, row=currentShaft, column=5)
    @pyqtSlot(int)
    def changeCurrentShaft(self, pos): self.DynamicCanvasView.changeCurrentShaft(pos)
    
    @pyqtSlot()
    def on_Drive_rod_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Drive Rod" in tabNameList: self.closePanel(tabNameList.index("Drive Rod"))
        else:
            panel = Drive_rod_show(self.File.Lists.RodList, self.File.Lists.PointList, self)
            panel.positionChange.connect(self.Save_position)
            panel.Position.valueChanged.connect(self.Change_position)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/normal.png")), "Drive Rod")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    @pyqtSlot(int)
    def Change_position(self, pos):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Rod"))
        self.File.Lists.setDemo('Rod', row=panel.Rod.currentIndex(), pos=pos/100)
        self.Resolve()
        self.workbookNoSave()
    @pyqtSlot(float, int)
    def Save_position(self, pos, currentRod): self.File.Lists.saveDemo(self.Rod, 'Rod', pos, row=currentRod, column=4)
    
    @pyqtSlot()
    def on_Measurement_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Measurement" in tabNameList: self.closePanel(tabNameList.index("Measurement"))
        else:
            table = self.Entiteis_Point
            panel = Measurement_show(table, self)
            self.DynamicCanvasView.change_event.connect(panel.Detection_do)
            self.action_Display_Dimensions.setChecked(True)
            self.action_Display_Point_Mark.setChecked(True)
            self.DynamicCanvasView.mouse_track.connect(panel.show_mouse_track)
            panel.point_change.connect(self.distance_solving)
            self.distance_changed.connect(panel.change_distance)
            panel.Mouse.setPlainText("Detecting...")
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/ref.png")), "Measurement")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    distance_changed = pyqtSignal(float)
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        x = self.File.Lists.PointList[start].cx-self.File.Lists.PointList[end].cx
        y = self.File.Lists.PointList[start].cy-self.File.Lists.PointList[end].cy
        self.distance_changed.emit(round((x**2+y**2)**(1/2), 5))
    
    @pyqtSlot()
    def on_AuxLine_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Auxiliary Line" in tabNameList:
            self.closePanel(tabNameList.index("Auxiliary Line"))
            self.DynamicCanvasView.reset_Auxline()
        else:
            self.DynamicCanvasView.AuxLine['show'] = True
            self.DynamicCanvasView.AuxLine['horizontal'] = True
            self.DynamicCanvasView.AuxLine['vertical'] = True
            table = self.Entiteis_Point
            panel = AuxLine_show(table, self.DynamicCanvasView.AuxLine['pt'], self.DynamicCanvasView.AuxLine['color'], self.DynamicCanvasView.AuxLine['limit_color'], self)
            panel.Point_change.connect(self.draw_Auxline)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/auxline.png")), "Auxiliary Line")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
        self.Reload_Canvas()
    @pyqtSlot(int, int, int, bool, bool, bool, bool, bool)
    def draw_Auxline(self, pt, color, color_l, axe_H, axe_V, max_l, min_l, pt_change):
        self.DynamicCanvasView.AuxLine['pt'] = pt
        self.DynamicCanvasView.AuxLine['color'] = color
        self.DynamicCanvasView.AuxLine['limit_color'] = color_l
        if pt_change: self.DynamicCanvasView.Reset_Aux_limit()
        self.DynamicCanvasView.AuxLine['horizontal'] = axe_H
        self.DynamicCanvasView.AuxLine['vertical'] = axe_V
        self.DynamicCanvasView.AuxLine['isMax'] = max_l
        self.DynamicCanvasView.AuxLine['isMin'] = min_l
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_action_Close_all_panel_triggered(self): self.closeAllPanels(True)
    def closeAllPanels(self, closePathSolving=False):
        for i in reversed(range(self.PointTab.count())):
            if not((self.PointTab.tabText(i)=="Path Solving" and not closePathSolving) or i==0 or i==1): self.closePanel(i)
        self.PointTab.setCurrentIndex(0)
        for button in [self.TriangleSolver, self.Drive_shaft, self.Drive_rod, self.Measurement, self.AuxLine]: button.setChecked(False)
        if closePathSolving: self.PathSolving.setChecked(False)
        self.DynamicCanvasView.options.slvsPath['show'] = False
        self.DynamicCanvasView.options.Path.Drivemode = False
        self.DynamicCanvasView.reset_Auxline()
        self.Reload_Canvas()
    def closePanel(self, pos):
        panel = self.PointTab.widget(pos)
        self.PointTab.removeTab(pos)
        panel.close()
        panel.deleteLater()
    
    def tableFocusChange(self, item):
        if self.FocusTable!=item.tableWidget():
            self.claerTableDelShortcut()
            if item.tableWidget()==self.Entiteis_Point: self.action_Delete_Point.setShortcut('Del')
            elif item.tableWidget()==self.Entiteis_Link: self.action_Delete_Linkage.setShortcut('Del')
            elif item.tableWidget()==self.Entiteis_Stay_Chain: self.action_Delete_Stay_Chain.setShortcut('Del')
            elif item.tableWidget()==self.Shaft: self.action_Delete_Shaft.setShortcut('Del')
            elif item.tableWidget()==self.Slider: self.action_Delete_Slider.setShortcut('Del')
            elif item.tableWidget()==self.Rod: self.action_Delete_Piston_Spring.setShortcut('Del')
            self.FocusTable = item.tableWidget()
    def claerTableDelShortcut(self):
        for action in [self.action_Delete_Point, self.action_Delete_Linkage, self.action_Delete_Stay_Chain,
            self.action_Delete_Shaft, self.action_Delete_Slider, self.action_Delete_Piston_Spring]: action.setShortcut('')
    
    def MaskChange(self):
        Count = str(max(list(self.File.Lists.ParameterList.keys())) if self.File.Lists.ParameterList else -1)
        param = '(({}{}){})'.format('[1-{}]'.format(Count[0]) if int(Count)>9 else '[0-{}]'.format(Count),
            ''.join(['[0-{}]'.format(e) for e in Count[1:]]), '|[0-9]{{1,{}}}'.format(len(Count)-1) if len(Count)>1 else str())
        mask = '({}^[-]?(([1-9][0-9]{{0,14}})|[0])?[.][0-9]{{1,15}}$)'.format('^[n]{}$|'.format(param) if int(Count)>-1 else str())
        self.Mask = QRegExpValidator(QRegExp(mask))
        for textBox in [self.X_coordinate, self.Y_coordinate]: textBox.setValidator(self.Mask)
    
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
            self.Comment_lable, self.Parameter_update]: widget.setEnabled(enabled)
    
    @pyqtSlot()
    def on_action_ViewLogFile_triggered(self):
        logfile = 'PyslvsLogFile.log'
        if os.path.isfile(logfile):
            with open (logfile, 'r') as f: data = f.read()
            dlgbox = QMessageBox(QMessageBox.Information, logfile, "In last 1000 characters:\n\n"+data[-1000:], (QMessageBox.Ok), self)
            if dlgbox.exec_(): pass
        else:
            dlgbox = QMessageBox(QMessageBox.Warning, "No Log file", "There is no Pyslvs log file!", (QMessageBox.Ok), self)
            if dlgbox.exec_(): pass
    
    def connectConsole(self):
        XStream.stdout().messageWritten.connect(self.appendToConsole)
        XStream.stderr().messageWritten.connect(self.appendToConsole)
    def disconnectConsole(self): XStream.back()
    @pyqtSlot()
    def on_connectButton_clicked(self):
        print("Connect to GUI console.")
        self.connectConsole()
        self.connectButton.setEnabled(False)
        self.disconnectButton.setEnabled(True)
        print("Connect to GUI console.")
    @pyqtSlot()
    def on_disconnectButton_clicked(self):
        print("Disconnect from GUI console.")
        self.disconnectConsole()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        print("Disconnect from GUI console.")
    
    @pyqtSlot(str)
    def appendToConsole(self, log):
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
        self.consoleWidgetBrowser.insertPlainText(log)
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
