# -*- coding: utf-8 -*-
'''
Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''
from .QtModules import *
from .modules import *
_translate = QCoreApplication.translate
from .Ui_main import Ui_MainWindow
from .Ui_custom import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #Arguments
        self.args = args
        if self.args.show_args: print("Arguments: {}".format(vars(self.args)))
        #File & Default Setting
        self.FileState = QUndoStack()
        self.FileState.indexChanged.connect(self.commandReload)
        showUndoWindow(self)
        self.File = File(self.FileState, args)
        self.setLocate(QFileInfo('.').absolutePath())
        #QPainter Window
        self.DynamicCanvasView = DynamicCanvas()
        self.DynamicCanvasView.mouse_getClick.connect(self.addPointGroup)
        self.mplLayout.insertWidget(0, self.DynamicCanvasView)
        self.DynamicCanvasView.show()
        self.Resolve()
        #Solve & Script & DOF & Mask
        self.Solvefail = False
        self.DOF = 0
        self.FocusTable = None
        self.MaskChange()
        self.Parameter_digital.setValidator(self.Mask)
        init_Right_click_menu(self)
        actionEnabled(self)
        if self.args.r: self.loadWorkbook("Loading by Argument.", fileName=self.args.r)
    
    def setLocate(self, locate):
        self.Default_Environment_variables = locate
        print("~Start at: [{}]".format(self.Default_Environment_variables))
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            for url in mimeData.urls():
                FilePath = url.toLocalFile()
                if QFileInfo(FilePath).suffix()=="csv": event.acceptProposedAction()
    def dropEvent(self, event):
        FilePath = event.mimeData().urls()[-1].toLocalFile()
        self.checkChange(FilePath, list(), "Loaded drag-in file:\n"+FilePath)
        event.acceptProposedAction()
    
    #Mouse position on canvace
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    #TODO: Right-click menu event
    def on_painter_context_menu(self, point):
        self.action_painter_right_click_menu_path_add.setVisible(self.PathSolving.isChecked())
        action = self.popMenu_painter.exec_(self.DynamicCanvasView.mapToGlobal(point))
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.mouse_pos_x
        y = self.mouse_pos_y
        if action==self.action_painter_right_click_menu_add: self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), False, styleTable=table2, color='Green', ringsize=5, ringcolor='Green')
        elif action==self.action_painter_right_click_menu_fix_add: self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), True, styleTable=table2, color='Blue', ringsize=10, ringcolor='Blue')
        elif action==self.action_painter_right_click_menu_path_add: self.PathSolving_add_rightClick(x, y)
        elif action==self.action_painter_right_click_menu_dimension_add:
            if self.actionDisplay_Dimensions.isChecked()==False: self.action_painter_right_click_menu_dimension_add.setText("Hide Dimension")
            elif self.actionDisplay_Dimensions.isChecked()==True: self.action_painter_right_click_menu_dimension_add.setText("Show Dimension")
            self.action_painter_right_click_menu_dimension_add.setChecked(not self.actionDisplay_Dimensions.isChecked())
            self.actionDisplay_Dimensions.setChecked(not self.actionDisplay_Dimensions.isChecked())
        elif action==self.action_painter_right_click_menu_dimension_path_track:
            if self.Path_data_show.checkState()==True: self.action_painter_right_click_menu_dimension_path_track.setText("Hide Path Track")
            elif self.Path_data_show.checkState()==False: self.action_painter_right_click_menu_dimension_path_track.setText("Show Path Track")
            self.Path_data_show.setChecked(not self.Path_data_show.checkState())
            self.on_Path_data_show_clicked()
    def on_point_context_menu(self, point):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        NOT_ORIGIN = table1.rowCount()>1 and table1.currentRow()!=0
        self.action_point_right_click_menu_delete.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_edit.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_lock.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_coverage.setEnabled(NOT_ORIGIN)
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        table_pos = table1.currentRow() if table1.currentRow()>=1 else 1
        table_pos_0 = table1.currentRow()
        if action==self.action_point_right_click_menu_copy: self.Coordinate_Copy(table1)
        elif action==self.action_point_right_click_menu_copyPoint: self.File.Lists.editTable(table1, 'Point', False,
            table1.item(table_pos_0, 1).text(), table1.item(table_pos_0, 2).text(), table1.item(table_pos_0, 3).checkState()==Qt.Checked,
            styleTable=table2, color='Green', ringsize=5, ringcolor='Orange')
        elif action==self.action_point_right_click_menu_coverage: self.File.Lists.coverageCoordinate(table1, table_pos_0)
        elif action==self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action==self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered(table_pos)
        elif action==self.action_point_right_click_menu_lock:
            self.File.Lists.editTable(table1, 'Point', table_pos_0,
                str(self.File.Lists.PointList[table_pos_0]['x']), str(self.File.Lists.PointList[table_pos_0]['y']), not(self.File.Lists.PointList[table_pos_0]['fix']))
            self.File.Lists.styleFix(table2, self.File.Lists.PointList[table_pos_0]['fix'], table_pos_0)
        elif action==self.action_point_right_click_menu_replace: self.on_actionReplace_Point_triggered(table_pos_0)
        elif action==self.action_point_right_click_menu_delete: self.on_actionDelete_Point_triggered(table_pos)
    def on_link_context_menu(self, point):
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Link.currentRow()
        if action==self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action==self.action_link_right_click_menu_edit: self.on_actionEdit_Linkage_triggered(table_pos)
        elif action==self.action_link_right_click_menu_shaft: self.link2Shaft(table_pos)
        elif action==self.action_link_right_click_menu_reversion: self.File.Lists.lineNodeReversion(self.Entiteis_Point, table_pos)
        elif action==self.action_link_right_click_menu_delete: self.on_actionDelete_Linkage_triggered(table_pos)
    def on_chain_context_menu(self, point):
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Stay_Chain.currentRow()
        if action==self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action==self.action_chain_right_click_menu_edit: self.on_actionEdit_Stay_Chain_triggered(table_pos)
        elif action==self.action_chain_right_click_menu_delete: self.on_actionDelete_Stay_Chain_triggered(table_pos)
    def on_shaft_context_menu(self, point):
        self.action_shaft_right_click_menu_move_up.setEnabled(self.Shaft.rowCount()>0 and self.Shaft.currentRow()>0)
        self.action_shaft_right_click_menu_move_down.setEnabled(self.Shaft.rowCount()>0 and self.Shaft.currentRow()<self.Shaft.rowCount()-1)
        action = self.popMenu_shaft.exec_(self.Shaft_Widget.mapToGlobal(point))
        table_pos = self.Shaft.currentRow()
        if action==self.action_shaft_right_click_menu_add: self.on_action_Set_Shaft_triggered()
        elif action==self.action_shaft_right_click_menu_edit: self.on_action_Edit_Shaft_triggered(table_pos)
        elif action==self.action_shaft_right_click_menu_move_up: self.File.Lists.shaftChange(self.Shaft, table_pos, table_pos-1)
        elif action==self.action_shaft_right_click_menu_move_down: self.File.Lists.shaftChange(self.Shaft, table_pos, table_pos+1)
        elif action==self.action_shaft_right_click_menu_delete: self.on_actionDelete_Shaft_triggered(table_pos)
    def on_slider_context_menu(self, point):
        action = self.popMenu_slider.exec_(self.Slider_Widget.mapToGlobal(point))
        table_pos = self.Slider.currentRow()
        if action==self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action==self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered(table_pos)
        elif action==self.action_slider_right_click_menu_delete: self.on_actionDelete_Slider_triggered(table_pos)
    def on_rod_context_menu(self, point):
        action = self.popMenu_rod.exec_(self.Rod_Widget.mapToGlobal(point))
        table_pos = self.Rod.currentRow()
        if action==self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action==self.action_rod_right_click_menu_edit: self.on_action_Edit_Rod_triggered(table_pos)
        elif action==self.action_rod_right_click_menu_delete: self.on_actionDelete_Piston_Spring_triggered(table_pos)
    
    #Close Event
    def closeEvent(self, event):
        if self.File.form.changed:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_actionSave_triggered()
                if self.File.form.changed: event.ignore()
                else: self.Exit(event)
            elif reply==QMessageBox.Discard: self.Exit(event)
            else: event.ignore()
        else: self.Exit(event)
    def Exit(self, event):
        print('-'*7+"\nExit.")
        event.accept()
    
    #TODO: Undo and Redo
    @pyqtSlot(int)
    def commandReload(self, index=0):
        self.File.Lists.updateAll(self.Entiteis_Point, self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Shaft, self.Slider, self.Rod, self.Parameter_list)
        self.actionUndo.setText("Undo {}".format(self.FileState.undoText()))
        self.actionRedo.setText("Redo {}".format(self.FileState.redoText()))
        if self.FileState.undoText(): print(self.FileState.undoText())
        if index!=self.File.form.Stack: self.workbookNoSave()
        else: self.workbookSaved()
        for i in range(1, self.Entiteis_Point_Style.rowCount()):
            self.Entiteis_Point_Style.cellWidget(i, 1).currentIndexChanged.connect(self.Edit_Point_Style)
            self.Entiteis_Point_Style.cellWidget(i, 3).currentIndexChanged.connect(self.Edit_Point_Style)
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Triangle Solver" in tabNameList:
            self.PointTab.widget(tabNameList.index("Triangle Solver")).setPoint(self.File.Lists.PointList)
        self.Resolve()
    
    #Resolve
    def Resolve(self):
        Point, Line, Chain, Shaft, Slider, Rod = self.File.Obstacles_Exclusion()
        result, DOF = slvsProcess(Point, Line, Chain, Shaft, Slider, Rod, hasWarning=self.args.w)
        Failed = DOF is False
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
            self.File.conflictMessage(self.ConflictGuide)
            self.Reload_Canvas()
    #Reload Canvas
    def Reload_Canvas(self):
        self.DynamicCanvasView.update_figure(
            float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList,
            self.Entiteis_Point_Style, self.ZoomText.text(), self.Font_size.value(), self.actionDisplay_Dimensions.isChecked(), self.actionDisplay_Point_Mark.isChecked(),
            self.File.Lists.data, self.File.Lists.runList, self.File.Lists.shaftList)
    
    #Workbook Change
    def workbookNoSave(self):
        self.File.form.changed = True
        self.setWindowTitle(self.windowTitle().replace('*', str())+'*')
        actionEnabled(self)
    def workbookSaved(self):
        self.File.form.changed = False
        self.setWindowTitle(self.windowTitle().replace('*', str()))
        actionEnabled(self)
    
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        dlg = version_show()
        splash = Pyslvs_Splash()
        splash.show()
        self.OpenDlg(dlg)
        splash.finish(dlg)
    @pyqtSlot()
    def on_actionAbout_Qt_triggered(self): QMessageBox.aboutQt(self)
    @pyqtSlot()
    def on_action_Get_Help_triggered(self): self.OpenURL("http://project.mde.tw/blog/slvs-library-functions.html")
    @pyqtSlot()
    def on_actionGit_hub_Site_triggered(self): self.OpenURL("https://github.com/KmolYuan/python-solvespace")
    @pyqtSlot()
    def on_actionGithub_Wiki_triggered(self): self.OpenURL("https://github.com/KmolYuan/Pyslvs-manual/tree/master")
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        Point, Line, Chain, Shaft, Slider, Rod = self.File.Obstacles_Exclusion()
        self.File.Script = slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod)
        self.OpenDlg(Script_Dialog(self.File.Script, self.Default_Environment_variables))
    @pyqtSlot()
    def on_actionSearch_Points_triggered(self): self.OpenDlg(Association_show(self.File.Lists.PointList, self.File.Lists.LineList,
        self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList))
    def OpenURL(self, URL):
        print("Open - {{{}}}".format(URL))
        webbrowser.open(URL)
    def OpenDlg(self, dlg):
        dlg.show()
        dlg.exec()
    
    #TODO: Example
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self): self.checkChange("[New Workbook]", new_workbook(), 'Generating New Workbook...')
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self): self.checkChange(say='Open file...')
    @pyqtSlot()
    def on_actionCrank_rocker_triggered(self): self.checkChange("[Example] Crank Rocker", example_crankRocker())
    @pyqtSlot()
    def on_actionDrag_link_triggered(self): self.checkChange("[Example] Drag-link", example_DragLink())
    @pyqtSlot()
    def on_actionDouble_rocker_triggered(self): self.checkChange("[Example] Double Rocker", example_doubleRocker())
    @pyqtSlot()
    def on_actionParallelogram_linkage_triggered(self): self.checkChange("[Example] Parallelogram Linkage", example_parallelogramLinkage())
    @pyqtSlot()
    def on_actionMutiple_Link_triggered(self): self.checkChange("[Example] Mutiple Link", example_mutipleLink())
    @pyqtSlot()
    def on_actionTwo_Mutiple_Link_triggered(self): self.checkChange("[Example] Two Pairs Mutiple Link", example_twoMutipleLink())
    @pyqtSlot()
    def on_actionReverse_Parsing_Rocker_triggered(self): self.checkChange("[Example] Reverse Parsing Rocker", example_reverseParsingRocker())
    @pyqtSlot()
    def on_actionSlider_and_Rod_triggered(self): self.checkChange("[Example] Slider and Rod", example_sliderRod())
    @pyqtSlot()
    def on_actionRock_Slider_triggered(self): self.checkChange("[Example] Rock Slider", example_rockSlider())
    @pyqtSlot()
    def on_actionLift_Tailgate_triggered(self): self.checkChange("[Example] Lift Tailgate", example_liftTailgate())
    @pyqtSlot()
    def on_actionTheo_Jansen_s_multi_linkage_triggered(self): self.checkChange("[Example] Theo Jansen\'s multiple linkage", example_TJLinkage())
    @pyqtSlot()
    def on_actionRock_Slider_Design_triggered(self): self.checkChange("[Example] Rock slider design", example_RockSliderDesign())
    #Workbook Functions
    def checkChange(self, name=False, data=list(), say='Loading Example...'):
        if self.File.form.changed:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit this file?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Save:
                self.on_actionSave_triggered()
                if not self.File.form.changed: self.loadWorkbook(say, name, data)
            elif reply==QMessageBox.Discard: self.loadWorkbook(say, name, data)
        else: self.loadWorkbook(say, name, data)
    def loadWorkbook(self, say, fileName=False, data=list()):
        print(say)
        self.closePanels()
        self.File.reset(self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Shaft, self.Slider, self.Rod, self.Parameter_list)
        self.DynamicCanvasView.changeCurrentShaft(0)
        self.DynamicCanvasView.path_solving(list())
        self.Resolve()
        self.FileState.clear()
        self.X_coordinate.clear()
        self.Y_coordinate.clear()
        self.setWindowTitle("Pyslvs - [New Workbook]")
        print("Reset workbook.")
        if fileName==False:
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
            if fileName: self.setLocate(QFileInfo(fileName).absolutePath())
        if QFileInfo(fileName).suffix()=='csv' or QFileInfo(fileName).suffix()=='txt' or ('[Example]' in fileName) or ('[New Workbook]' in fileName):
            data = self.File.readData(fileName, data)
            if self.File.check(data):
                self.File.read(fileName, data,
                    self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Shaft, self.Slider, self.Rod, self.Parameter_list)
                self.setWindowTitle("Pyslvs - {}".format(QFileInfo(fileName).fileName()))
                self.Path_Clear.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                self.Path_coordinate.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                self.Path_data_show.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                self.workbookSaved()
                print("Loaded the workbook.")
                if not('[New Workbook]' in fileName): self.show_Property()
                else: self.on_action_Property_triggered()
            else: self.loadWorkbookError()
    @pyqtSlot()
    def on_actionImportFromWorkbook_triggered(self): self.importWorkbook(say='Import from file...')
    def importWorkbook(self, say, fileName=False, data=list()):
        print(say)
        if fileName==False:
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
            if fileName: self.setLocate(QFileInfo(fileName).absolutePath())
        if QFileInfo(fileName).suffix()=='csv' or QFileInfo(fileName).suffix()=='txt' or ('[Template]' in fileName):
            data = self.File.readData(fileName, data)
            if self.File.check(data):
                self.File.readMerge(data,
                    self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Shaft, self.Slider, self.Rod, self.Parameter_list)
            else: self.loadWorkbookError()
    def loadWorkbookError(self):
        dlgbox = QMessageBox(QMessageBox.Warning, "Loading failed", "File:\n{}\n\nYour data sheet is an incorrect format.".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_(): print("Error: Incorrect format.")
    
    #TODO: Save format
    @pyqtSlot()
    def on_actionSave_triggered(self):
        n = self.File.form.fileName.absoluteFilePath()
        if ('[New Workbook]' in n or '[Example]' in n)and(QFileInfo(n).suffix()!='csv' and QFileInfo(n).suffix()!='txt'):
            fileName = self.outputTo("Workbook", 'Spreadsheet(*.csv)')
        else: fileName = self.File.form.fileName.absoluteFilePath()
        if fileName: self.save(fileName)
    @pyqtSlot()
    def on_actionSave_as_triggered(self):
        fileName = self.outputTo("Workbook", 'Spreadsheet(*.csv)')
        if fileName: self.save(fileName)
    def save(self, fileName):
        with open(fileName, 'w', newline=str()) as stream:
            writer = csv.writer(stream)
            self.File.write(
                fileName, writer,
                self.Entiteis_Point, self.Entiteis_Point_Style,
                self.Entiteis_Link, self.Entiteis_Stay_Chain,
                self.Shaft, self.Slider,
                self.Rod, self.Parameter_list)
        print("Successful saved: {}".format(fileName))
        self.workbookSaved()
    
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        dlg = slvsTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_(): self.replyBox('Solvespace Models', dlg.folderPath.absolutePath())
    @pyqtSlot()
    def on_actionSolvespace_2D_sketch_triggered(self):
        fileName = self.outputTo("Solvespace sketch", 'Solvespace module(*.slvs)')
        if fileName:
            content = slvs2D(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f: f.write(content)
            self.replyBox('Solvespace Sketch', fileName)
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        Point, Line, Chain, Shaft, Slider, Rod = self.File.Obstacles_Exclusion()
        self.File.Script = slvsProcessScript(Point, Line, Chain, Shaft, Slider, Rod)
        fileName = self.outputTo("Python Script", 'Python Script(*.py)')
        if fileName:
            with open(fileName, 'w', newline=str()) as f: f.write(self.File.Script)
            self.replyBox('Python Script', fileName)
    @pyqtSlot()
    def on_actionDXF_2D_models_triggered(self):
        dlg = dxfTypeSettings(self.Default_Environment_variables, self.File.form.fileName.baseName(),
            self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_(): self.replyBox('DXF 2D Models', dlg.filePath)
    @pyqtSlot()
    def on_actionDXF_2D_sketch_triggered(self):
        fileName = self.outputTo("DXF", 'AutoCAD DXF (*.dxf)')
        if fileName:
            dxfSketch(fileName, self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
            self.replyBox('DXF 2D Sketch', fileName)
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        fileName = self.outputTo("picture", "Portable Network Graphics (*.png);;Joint Photographic Experts Group (*.jpg);;Joint Photographic Experts Group (*.jpeg);;Bitmap Image file (*.bmp);;\
            Business Process Model (*.bpm);;Tagged Image File Format (*.tiff);;Tagged Image File Format (*.tif);;Windows Icon (*.ico);;Wireless Application Protocol Bitmap (*.wbmp);;\
            X BitMap (*.xbm);;X Pixmap (*.xpm)")
        if fileName:
            pixmap = self.DynamicCanvasView.grab()
            pixmap.save(fileName, format = QFileInfo(fileName).suffix())
            self.replyBox('Picture', fileName)
    def outputTo(self, formatName, formatChoose):
        suffix0 = formatChoose.split(';;')[0].split('*')[-1][:-1]
        fileName, form = QFileDialog.getSaveFileName(
            self, 'Save file...', self.Default_Environment_variables+'/'+self.File.form.fileName.baseName()+suffix0, formatChoose)
        if fileName:
            self.setLocate(QFileInfo(fileName).absolutePath())
            suffix = form.split('*')[-1][:-1]
            fileName = self.Default_Environment_variables+'/'+QFileInfo(fileName).baseName()+suffix
            print("Formate: {}".format(form))
        return fileName
    def replyBox(self, title, fileName):
        dlgbox = QMessageBox(QMessageBox.Information, title, "Successfully converted:\n{}".format(fileName), (QMessageBox.Ok), self)
        if dlgbox.exec_(): print("Successful Saved {}.".format(title))
    
    def show_Property(self):
        dlg = fileInfo_show()
        dlg.rename(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description, self.File.form.lastTime)
        dlg.show()
        if dlg.exec_(): pass
    @pyqtSlot()
    def on_action_Property_triggered(self):
        dlg = editFileInfo_show()
        self.File.updateTime()
        dlg.rename(self.File.form.fileName.fileName(), self.File.form.author, self.File.form.description, self.File.form.lastTime)
        dlg.show()
        if dlg.exec_():
            self.File.updateAuthorDescription(dlg.authorName_input.text(), dlg.descriptionText.toPlainText())
            self.workbookNoSave()
    
    @pyqtSlot(int, int)
    def on_Entiteis_Point_cellDoubleClicked(self, row, column):
        if row>0: self.on_actionEdit_Point_triggered(row)
    @pyqtSlot(int, int)
    def on_Entiteis_Link_cellDoubleClicked(self, row, column): self.on_actionEdit_Linkage_triggered(row)
    @pyqtSlot(int, int)
    def on_Entiteis_Stay_Chain_cellDoubleClicked(self, row, column): self.on_actionEdit_Stay_Chain_triggered(row)
    @pyqtSlot(int, int)
    def on_Shaft_cellDoubleClicked(self, row, column): self.on_action_Edit_Shaft_triggered(row)
    @pyqtSlot(int, int)
    def on_Slider_cellDoubleClicked(self, row, column): self.on_action_Edit_Slider_triggered(row)
    @pyqtSlot(int, int)
    def on_Rod_cellDoubleClicked(self, row, column): self.on_action_Edit_Rod_triggered(row)
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        dlg = edit_point_show(self.Mask, table1, self.File.Lists.PointList)
        dlg.show()
        if dlg.exec_():
            x = dlg.X_coordinate.text() if not dlg.X_coordinate.text() in [str(), "n", "-"] else dlg.X_coordinate.placeholderText()
            y = dlg.Y_coordinate.text() if not dlg.Y_coordinate.text() in [str(), "n", "-"] else dlg.Y_coordinate.placeholderText()
            self.File.Lists.editTable(table1, 'Point', False, x, y, bool(dlg.Fix_Point.checkState()),
                styleTable=table2, color='Green', ringsize=10 if dlg.Fix_Point.checkState() else 5, ringcolor='Green')
    def addPointGroup(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        table3 = self.Entiteis_Link
        self.File.Lists.editTable(table1, 'Point', False, str(self.mouse_pos_x), str(self.mouse_pos_y), False,
            styleTable=table2, color='Green', ringsize=5, ringcolor='Green')
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text() if not self.X_coordinate.text() in [str(), "n", "-"] else self.X_coordinate.placeholderText()
        y = self.Y_coordinate.text() if not self.Y_coordinate.text() in [str(), "n", "-"] else self.Y_coordinate.placeholderText()
        self.File.Lists.editTable(table1, 'Point', False, x, y, False,
            styleTable=table2, color='Green', ringsize=5, ringcolor='Green')
        self.X_coordinate.clear()
        self.Y_coordinate.clear()
    @pyqtSlot(int, int, int, int)
    def on_Entiteis_Point_currentCellChanged(self, c0, c1, p0, p1):
        self.X_coordinate.setPlaceholderText(self.Entiteis_Point.item(c0, 1).text())
        self.Y_coordinate.setPlaceholderText(self.Entiteis_Point.item(c0, 2).text())
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self, pos=1):
        table = self.Entiteis_Point
        dlg = edit_point_show(self.Mask, table, self.File.Lists.PointList, pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table, 'Point', dlg.Point.currentIndex()+1,
                dlg.X_coordinate.text() if not dlg.X_coordinate.text()in[str(), "n", "-"] else dlg.X_coordinate.placeholderText(),
                dlg.Y_coordinate.text() if not dlg.Y_coordinate.text()in[str(), "n", "-"] else dlg.Y_coordinate.placeholderText(),
                bool(dlg.Fix_Point.checkState()))
            self.File.Lists.styleFix(self.Entiteis_Point_Style, bool(dlg.Fix_Point.checkState()), pos)
    
    @pyqtSlot(int)
    def Edit_Point_Style(self, index):
        self.Resolve()
        self.workbookNoSave()
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        dlg = edit_link_show(self.Mask, table1, table2, self.File.Lists.PointList, self.File.Lists.LineList)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Line', False, dlg.Start_Point.currentText(), dlg.End_Point.currentText(), dlg.len)
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        dlg = edit_link_show(self.Mask, table1, table2, self.File.Lists.PointList, self.File.Lists.LineList, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Line', dlg.Link.currentIndex(),
            dlg.Start_Point.currentText(), dlg.End_Point.currentText(), dlg.len)
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        dlg = edit_chain_show(self.Mask, table1, table2, self.File.Lists.PointList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Chain', False, dlg.p1, dlg.p2, dlg.p3, dlg.p1_p2Val, dlg.p2_p3Val, dlg.p1_p3Val)
    
    @pyqtSlot()
    def on_actionEdit_Stay_Chain_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        dlg = edit_chain_show(self.Mask, table1, table2, self.File.Lists.PointList, self.File.Lists.ChainList, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Chain', dlg.Chain.currentIndex(),
            dlg.p1, dlg.p2, dlg.p3, dlg.p1_p2Val, dlg.p2_p3Val, dlg.p1_p3Val)
    
    @pyqtSlot()
    def on_action_Set_Shaft_triggered(self, cen=0, ref=0):
        table1 = self.Entiteis_Point
        table2 = self.Shaft
        dlg = edit_shaft_show(table1, table2, self.File.Lists.ShaftList, cen=cen, ref=ref)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Shaft', False,
            dlg.center, dlg.ref, dlg.start, dlg.end, self.File.Lists.m(dlg.center, dlg.ref), bool(dlg.isParallelogram.checkState()))
    
    @pyqtSlot()
    def on_action_Edit_Shaft_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Shaft
        dlg = edit_shaft_show(table1, table2, self.File.Lists.ShaftList, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Shaft', dlg.Shaft.currentIndex(), dlg.center, dlg.ref, dlg.start, dlg.end,
            table2.item(dlg.Shaft.currentIndex(), 5), bool(dlg.isParallelogram.checkState()))
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        dlg = edit_slider_show(self.Entiteis_Point, self.Slider, self.File.Lists.SliderList)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(self.Slider, 'Slider', False, dlg.slider, dlg.start, dlg.end)
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self, pos=0):
        dlg = edit_slider_show(self.Entiteis_Point, self.Slider, self.File.Lists.SliderList, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(self.Slider, 'Slider', dlg.Slider.currentIndex(), dlg.slider, dlg.start, dlg.end)
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        dlg = edit_rod_show(table1, table2, self.File.Lists.RodList)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Rod', False, dlg.cen, dlg.start, dlg.end, dlg.pos)
    
    @pyqtSlot()
    def on_action_Edit_Rod_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        dlg = edit_rod_show(table1, table2, self.File.Lists.RodList, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Rod', dlg.Rod.currentIndex(), dlg.cen, dlg.start, dlg.end, dlg.pos)
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Point.currentRow()
        self.deletePanel(self.Entiteis_Point, 'Point', ":/icons/delete.png", ":/icons/point.png", pos)
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Link.currentRow()
        self.deletePanel(self.Entiteis_Link, 'Line', ":/icons/deleteline.png", ":/icons/line.png", pos)
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self, pos=None):
        if pos==None: pos = self.Entiteis_Stay_Chain.currentRow()
        self.deletePanel(self.Entiteis_Stay_Chain, 'Chain', ":/icons/deletechain.png", ":/icons/equal.png", pos)
    @pyqtSlot()
    def on_actionDelete_Shaft_triggered(self, pos=None):
        if pos==None: pos = self.Shaft.currentRow()
        self.deletePanel(self.Shaft, 'Shaft', ":/icons/deleteshaft.png", ":/icons/circle.png", pos)
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self, pos=None):
        if pos==None: pos = self.Slider.currentRow()
        self.deletePanel(self.Slider, 'Slider', ":/icons/deleteslider.png", ":/icons/pointonx.png", pos)
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self, pos=None):
        if pos==None: pos = self.Rod.currentRow()
        self.deletePanel(self.Rod, 'Rod', QIcon(QPixmap(":/icons/deleterod.png")), QIcon(QPixmap(":/icons/spring.png")), pos)
    def deletePanel(self, table, name, icon1, icon2, pos):
        dlg = deleteDlg(QIcon(QPixmap(icon1)), QIcon(QPixmap(icon2)), table, pos)
        dlg.move(QCursor.pos()-QPoint(dlg.size().width(), dlg.size().height()))
        dlg.show()
        if dlg.exec_():
            if name=='Point': self.File.Lists.deletePointTable(self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link,
                self.Entiteis_Stay_Chain, self.Shaft, self.Slider, self.Rod, dlg.Entity.currentIndex())
            else: self.File.Lists.deleteTable(table, name, dlg.Entity.currentIndex())
            self.closePanels()
    
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
    def on_actionReplace_Point_triggered(self, pos=0):
        dlg = replacePoint_show(QIcon(QPixmap(":/icons/point.png")), self.Entiteis_Point, pos)
        dlg.show()
        if dlg.exec_(): self.File.Lists.ChangePoint(self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Shaft, self.Slider, self.Rod,
            dlg.Prv.currentIndex(), dlg.Next.currentIndex())
    
    @pyqtSlot()
    def on_actionBatch_moving_triggered(self):
        dlg = batchMoving_show(self.File.Lists.PointList, self.File.Lists.ParameterList)
        dlg.show()
        if dlg.exec_(): self.File.Lists.batchMove(self.Entiteis_Point, dlg.XIncrease.value(), dlg.YIncrease.value(),
            [int(dlg.Move_list.item(e).text().replace('Point', "")) for e in range(dlg.Move_list.count())])
    
    def Coordinate_Copy(self, table):
        clipboard = QApplication.clipboard()
        clipboard.setText(table.currentItem().text())
    
    def link2Shaft(self, row):
        cen = self.File.Lists.LineList[row]['start']
        ref = self.File.Lists.LineList[row]['end']
        self.on_action_Set_Shaft_triggered(cen, ref)
    
    @pyqtSlot()
    def on_ResetCanvas_clicked(self): self.DynamicCanvasView.SetIn()
    @pyqtSlot()
    def on_FitW_clicked(self):
        self.Fit2H()
        self.Fit2W()
    def Fit2W(self):
        for i in range(10):
            max_pt = max(self.DynamicCanvasView.points['x'])
            min_pt = min(self.DynamicCanvasView.points['x'])
            self.DynamicCanvasView.points['origin']['x'] = (self.DynamicCanvasView.width()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.DynamicCanvasView.width()/(max_pt+min_pt+100))
            self.Reload_Canvas()
    @pyqtSlot()
    def on_FitH_clicked(self):
        self.Fit2W()
        self.Fit2H()
    def Fit2H(self):
        for i in range(10):
            max_pt = max(self.DynamicCanvasView.points['y'])
            min_pt = min(self.DynamicCanvasView.points['y'])
            self.DynamicCanvasView.points['origin']['y'] = (self.DynamicCanvasView.height()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.DynamicCanvasView.height()/(max_pt-min_pt+100))
            self.Reload_Canvas()
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setText(str(value)+'%')
        self.Reload_Canvas()
    #Wheel Event
    def wheelEvent(self, event):
        if self.mapFromGlobal(QCursor.pos()).x()>=470:
            if event.angleDelta().y()>0: self.ZoomBar.setValue(self.ZoomBar.value()+10)
            if event.angleDelta().y()<0: self.ZoomBar.setValue(self.ZoomBar.value()-10)
    
    @pyqtSlot(int)
    def on_LineWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_Font_size_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_PathWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Dimensions_toggled(self, p0):
        if p0: self.actionDisplay_Point_Mark.setChecked(True)
        self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Point_Mark_toggled(self, p0):
        if not p0: self.actionDisplay_Dimensions.setChecked(False)
        self.Reload_Canvas()
    @pyqtSlot()
    def on_Path_data_show_clicked(self):
        self.DynamicCanvasView.points['Path']['show'] = self.Path_data_show.checkState()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_Path_points_show_clicked(self):
        self.DynamicCanvasView.points['slvsPath']['show'] = self.Path_points_show.checkState()
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_PathTrack_clicked(self):
        table1 = self.Entiteis_Point
        dlg = Path_Track_show(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList,
            self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self.Parameter_list)
        self.actionDisplay_Point_Mark.setChecked(True)
        dlg.show()
        if dlg.exec_(): self.File.Lists.setPath(dlg.Path_data,
            [dlg.Run_list.item(i).text() for i in range(dlg.Run_list.count())], dlg.work.ShaftList)
    @pyqtSlot()
    def on_Path_Clear_clicked(self):
        self.File.Lists.clearPath()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_Path_coordinate_clicked(self):
        dlg = path_point_data_show(self.Default_Environment_variables, self.File.Lists.data, self.File.Lists.runList)
        dlg.show()
        dlg.exec()
    
    @pyqtSlot(bool)
    def on_PathSolving_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Path Solving" in tabNameList: self.closePanel(tabNameList.index("Path Solving"))
        else:
            panel = Path_Solving_show(self.Mask, self.File.Designs.list, self.File.Designs.result, self.width())
            panel.addPathPoint.connect(self.PathSolving_add)
            panel.deletePathPoint.connect(self.PathSolving_delete)
            panel.Generate.clicked.connect(self.PathSolving_send)
            panel.moveupPathPoint.connect(self.PathSolving_moveup)
            panel.movedownPathPoint.connect(self.PathSolving_movedown)
            panel.mergeMechanism.connect(self.PathSolving_merge)
            panel.deleteResult.connect(self.PathSolving_deleteResult)
            panel.mergeResult.connect(self.PathSolving_mergeResult)
            self.PathSolvingStart.connect(panel.start)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/bezier.png")), "Path Solving")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    def PathSolving_add_rightClick(self, x, y):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.PointTab.widget(tabNameList.index("Path Solving")).addPath(x, y)
        self.PathSolving_add(x, y)
    @pyqtSlot(float, float)
    def PathSolving_add(self, x=0, y=0):
        self.File.Designs.add(x, y)
        self.DynamicCanvasView.path_solving(self.File.Designs.list)
        self.workbookNoSave()
    @pyqtSlot(int)
    def PathSolving_delete(self, row):
        self.File.Designs.remove(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.list)
        self.workbookNoSave()
    @pyqtSlot(int)
    def PathSolving_moveup(self, row):
        self.File.Designs.moveUP(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.list)
    @pyqtSlot(int)
    def PathSolving_movedown(self, row):
        self.File.Designs.moveDown(row)
        self.DynamicCanvasView.path_solving(self.File.Designs.list)
    PathSolvingStart = pyqtSignal(list)
    @pyqtSlot()
    def PathSolving_send(self): self.PathSolvingStart.emit(self.File.Designs.list)
    @pyqtSlot(list)
    def PathSolving_merge(self, mechanism_data): self.File.Designs.resultMerge(mechanism_data)
    @pyqtSlot(int)
    def PathSolving_deleteResult(self, row): self.File.Designs.removeResult(row)
    @pyqtSlot(int)
    def PathSolving_mergeResult(self, row): self.File.Generate_Merge(row, self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Shaft)
    
    @pyqtSlot(bool)
    def on_TriangleSolver_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Triangle Solver" in tabNameList: self.closePanel(tabNameList.index("Triangle Solver"))
        else:
            panel = Triangle_Solver_show(self.FileState, self.File.Lists.PointList, self.File.Designs.TSDirections)
            panel.startMerge.connect(self.TriangleSolver_merge)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/TS.png")), "Triangle Solver")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    @pyqtSlot()
    def TriangleSolver_merge(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        self.File.TS_Merge(self.PointTab.widget(tabNameList.index("Triangle Solver")).answers,
            self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Slider)
    
    @pyqtSlot()
    def on_Drive_shaft_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Drive Shaft" in tabNameList: self.closePanel(tabNameList.index("Drive Shaft"))
        else:
            panel = Drive_shaft_show(self.File.Lists.ShaftList, self.DynamicCanvasView.points['currentShaft'])
            panel.Degree.sliderReleased.connect(self.Save_demo_angle)
            panel.Degree.valueChanged.connect(self.Change_demo_angle)
            panel.Shaft.currentIndexChanged.connect(self.changeCurrentShaft)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/same-orientation.png")), "Drive Shaft")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    @pyqtSlot()
    def Save_demo_angle(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Shaft"))
        self.File.Lists.saveDemo(self.Shaft, 'Shaft',
            panel.Degree.value()/100, row=panel.Shaft.currentIndex(), column=5)
    @pyqtSlot(int)
    def Change_demo_angle(self, angle):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Shaft"))
        self.File.Lists.setDemo('Shaft', row=panel.Shaft.currentIndex(), pos=angle/100)
        self.Resolve()
        self.workbookNoSave()
    @pyqtSlot(int)
    def changeCurrentShaft(self, pos): self.DynamicCanvasView.changeCurrentShaft(pos)
    
    @pyqtSlot()
    def on_Drive_rod_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Drive Rod" in tabNameList: self.closePanel(tabNameList.index("Drive Rod"))
        else:
            panel = Drive_rod_show(self.File.Lists.RodList, self.File.Lists.PointList)
            panel.Position.sliderReleased.connect(self.Save_position)
            panel.Position.valueChanged.connect(self.Change_position)
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/normal.png")), "Drive Rod")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    @pyqtSlot()
    def Save_position(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Rod"))
        self.File.Lists.saveDemo(self.Rod, 'Rod',
            panel.Position.value()/100, row=panel.Rod.currentIndex(), column=4)
    @pyqtSlot(int)
    def Change_position(self, pos):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        panel = self.PointTab.widget(tabNameList.index("Drive Rod"))
        self.File.Lists.setDemo('Rod', row=panel.Rod.currentIndex(), pos=pos/100)
        self.Resolve()
        self.workbookNoSave()
    
    @pyqtSlot()
    def on_Measurement_clicked(self):
        tabNameList = [self.PointTab.tabText(i) for i in range(self.PointTab.count())]
        if "Measurement" in tabNameList: self.closePanel(tabNameList.index("Measurement"))
        else:
            table = self.Entiteis_Point
            panel = Measurement_show(table)
            self.DynamicCanvasView.change_event.connect(panel.Detection_do)
            self.actionDisplay_Dimensions.setChecked(True)
            self.actionDisplay_Point_Mark.setChecked(True)
            self.DynamicCanvasView.mouse_track.connect(panel.show_mouse_track)
            panel.point_change.connect(self.distance_solving)
            self.distance_changed.connect(panel.change_distance)
            panel.Mouse.setPlainText("Detecting...")
            self.PointTab.addTab(panel, QIcon(QPixmap(":/icons/ref.png")), "Measurement")
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
    distance_changed = pyqtSignal(float)
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        x = self.File.Lists.PointList[start]['cx']-self.File.Lists.PointList[end]['cx']
        y = self.File.Lists.PointList[start]['cy']-self.File.Lists.PointList[end]['cy']
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
            panel = AuxLine_show(table, self.DynamicCanvasView.AuxLine['pt'], self.DynamicCanvasView.AuxLine['color'], self.DynamicCanvasView.AuxLine['limit_color'])
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
    def on_actionClose_all_panel_triggered(self): self.closePanels()
    def closePanels(self):
        while self.PointTab.count()>3: self.closePanel(self.PointTab.count()-1)
        self.PointTab.setCurrentIndex(0)
        for button in [self.PathSolving, self.TriangleSolver,
            self.Drive_shaft, self.Drive_rod, self.Measurement, self.AuxLine]: button.setChecked(False)
        self.DynamicCanvasView.reset_Auxline()
    def closePanel(self, pos):
        panel = self.PointTab.widget(pos)
        self.PointTab.removeTab(pos)
        panel.close()
        panel.deleteLater()
    
    def FocusChange(self, item):
        if self.FocusTable!=item.tableWidget():
            self.claerTableDelShortcut()
            if item.tableWidget()==self.Entiteis_Point: self.actionDelete_Point.setShortcut('Del')
            elif item.tableWidget()==self.Entiteis_Link: self.actionDelete_Linkage.setShortcut('Del')
            elif item.tableWidget()==self.Entiteis_Stay_Chain: self.actionDelete_Stay_Chain.setShortcut('Del')
            elif item.tableWidget()==self.Shaft: self.actionDelete_Shaft.setShortcut('Del')
            elif item.tableWidget()==self.Slider: self.actionDelete_Slider.setShortcut('Del')
            elif item.tableWidget()==self.Rod: self.actionDelete_Piston_Spring.setShortcut('Del')
            self.FocusTable = item.tableWidget()
    def claerTableDelShortcut(self):
        for action in [self.actionDelete_Point, self.actionDelete_Linkage, self.actionDelete_Stay_Chain,
            self.actionDelete_Shaft, self.actionDelete_Slider, self.actionDelete_Piston_Spring]: action.setShortcut('')
    
    def MaskChange(self):
        Count = str(max(list(self.File.Lists.ParameterList.keys())) if self.File.Lists.ParameterList else -1)
        param = '(({}{}){})'.format(
            '[1-{}]'.format(Count[0]) if int(Count)>9 else '[0-{}]'.format(Count),
            ''.join(['[0-{}]'.format(e) for e in Count[1:]]),
            '|[0-9]{{1,{}}}'.format(len(Count)-1) if len(Count)>1 else str())
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
