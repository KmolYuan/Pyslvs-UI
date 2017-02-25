# -*- coding: utf-8 -*-
'''
PySolvespace - PyQt 5 GUI with Solvespace Library
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
from .modules import *
_translate = QCoreApplication.translate
from .Ui_main import Ui_MainWindow
from .Ui_custom import init_Right_click_menu, actionEnabled

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #File & Default Setting
        self.FileState = QUndoStack()
        self.showUndoWindow(self.FileState)
        self.File = File(self.FileState)
        self.load_settings()
        #QPainter Window
        self.qpainterWindow = DynamicCanvas()
        self.mplLayout.insertWidget(0, self.qpainterWindow)
        self.qpainterWindow.show()
        self.Resolve()
        #Solve & Script & DOF & Mask & Parameter
        self.Solvefail = False
        self.DOF = 0
        self.Mask_Change()
        init_Right_click_menu(self)
        actionEnabled(self)
        self.Parameter_digital.setValidator(QRegExpValidator(QRegExp('^[-]?([1-9][0-9]{1,6})?[0-9][.][0-9]{1,8}$')))
        if len(sys.argv)>2: self.argvLoadFile()
    
    #LoadFile
    def argvLoadFile(self):
        if ".csv" in sys.argv[1].lower():
            try: self.loadWorkbook(sys.argv[1])
            except: print("Error when loading file.")
        elif "example" in sys.argv[1].lower():
            try:
                ExampleNum = int(sys.argv[1].lower().replace("example", str()))
                if ExampleNum==0: self.on_actionCrank_rocker_triggered()
                elif ExampleNum==1: self.on_actionDrag_link_triggered()
                elif ExampleNum==2: self.on_actionDouble_rocker_triggered()
                elif ExampleNum==3: self.on_actionParallelogram_linkage_triggered()
                elif ExampleNum==4: self.on_actionMutiple_Link_triggered()
                elif ExampleNum==5: self.on_actionTwo_Mutiple_Link_triggered()
                elif ExampleNum==6: self.on_actionReverse_Parsing_Rocker_triggered()
            except: print("Error when loading example.")
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
    
    def load_settings(self):
        option_info = Pyslvs_Settings_ini()
        self.Default_Environment_variables = QFileInfo(option_info.Environment_variables).absolutePath()
        self.Default_canvas_view = option_info.Zoom_factor
    
    #TODO: Right-click menu event
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    def on_painter_context_menu(self, point):
        self.action_painter_right_click_menu_path_add.setVisible(hasattr(self, 'PathSolvingDlg'))
        action = self.popMenu_painter.exec_(self.qpainterWindow.mapToGlobal(point))
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.mouse_pos_x
        y = self.mouse_pos_y
        if action==self.action_painter_right_click_menu_add:
            self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), False, **{'styleTable':table2, 'color':'Green', 'ringsize':'5', 'ringcolor':'Green'})
            self.Resolve()
        elif action==self.action_painter_right_click_menu_fix_add:
            self.File.Lists.editTable(table1, 'Point', False, str(x), str(y), True, **{'styleTable':table2, 'color':'Blue', 'ringsize':'10', 'ringcolor':'Green'})
            self.Resolve()
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
        NOT_ORIGIN = self.Entiteis_Point.rowCount()>1 and self.Entiteis_Point.currentRow()!=0
        self.action_point_right_click_menu_delete.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_edit.setEnabled(NOT_ORIGIN)
        self.action_point_right_click_menu_coverage.setVisible(self.Entiteis_Point.currentColumn()==4 and self.Entiteis_Point.currentRow()!=0)
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Point.currentRow() if self.Entiteis_Point.currentRow()>=1 else 1
        table_pos_0 = self.Entiteis_Point.currentRow()
        if action==self.action_point_right_click_menu_copy: self.Coordinate_Copy(self.Entiteis_Point)
        elif action==self.action_point_right_click_menu_copyPoint: self.File.Lists.editTable(self.Entiteis_Point, 'Point', False,
            self.Entiteis_Point.item(table_pos_0, 1).text(), self.Entiteis_Point.item(table_pos_0, 2).text(), self.Entiteis_Point.item(table_pos_0, 3).checkState()==Qt.Checked,
            **{'styleTable':self.Entiteis_Point_Style, 'color':'Green', 'ringsize':'5', 'ringcolor':'Orange'})
        elif action==self.action_point_right_click_menu_coverage: self.File.Lists.coverageCoordinate(self.Entiteis_Point, table_pos_0)
        elif action==self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action==self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered(table_pos)
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
    def on_parameter_context_menu(self, point):
        table_pos = self.Parameter_list.currentRow()
        self.action_parameter_right_click_menu_copy.setVisible(self.Parameter_list.currentColumn()==1)
        self.action_parameter_right_click_menu_move_up.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(table_pos>=1))
        self.action_parameter_right_click_menu_move_down.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(table_pos<=self.Parameter_list.rowCount()-2))
        self.action_parameter_right_click_menu_delete.setEnabled(self.Parameter_list.rowCount()>=1)
        action = self.popMenu_parameter.exec_(self.Parameter_Widget.mapToGlobal(point))
        if action==self.action_parameter_right_click_menu_copy: self.Coordinate_Copy(self.Parameter_list)
        elif action==self.action_parameter_right_click_menu_add: self.on_parameter_add()
        elif action==self.action_parameter_right_click_menu_move_up: self.on_parameter_del()
        elif action==self.action_parameter_right_click_menu_move_down:
            try:
                table.insertRow(row+2)
                for i in range(2):
                    name_set = QTableWidgetItem(table.item(row+2, i).text())
                    name_set.setFlags(Qt.ItemIsEnabled)
                    table.setItem(row+2, i, name_set)
                commit_set = QTableWidgetItem(table.item(row+2, 2).text())
                commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                table.removeRow(row)
                self.workbookNoSave()
            except: pass
        elif action==self.action_parameter_right_click_menu_delete:
            self.Parameter_list.removeRow(table_pos)
            self.workbookNoSave()
            self.Mask_Change()
    
    #Table copy
    def Coordinate_Copy(self, table):
        clipboard = QApplication.clipboard()
        clipboard.setText(table.currentItem().text())
    def link2Shaft(self, row):
        cen = self.File.Lists.LineList[row]['start']
        ref = self.File.Lists.LineList[row]['end']
        self.on_action_Set_Shaft_triggered(cen, ref)
    
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
    
    #Close Event
    def closeEvent(self, event):
        if self.File.form['changed']:
            reply = QMessageBox.question(self, 'Saving Message', "Are you sure to quit?\nAny Changes won't be saved.", (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply==QMessageBox.Discard or reply==QMessageBox.Ok:
                print("Exit.")
                event.accept()
            elif reply==QMessageBox.Save:
                self.on_actionSave_triggered()
                if not self.File.form['changed']:
                    print("Exit.")
                    event.accept()
                else: event.ignore()
            else: event.ignore()
        else:
            print("Exit.")
            event.accept()
    
    #TODO: Undo and Redo
    def showUndoWindow(self, stack):
        stack.indexChanged.connect(self.commandReload)
        undoView = QUndoView(stack)
        undoView.setEmptyLabel("~ Start Pyslvs")
        self.HistoryLayout.addWidget(undoView)
    @pyqtSlot()
    def on_actionUndo_triggered(self):
        doText = self.FileState.undoText()
        self.FileState.undo()
        print("Undo - {}".format(doText))
    @pyqtSlot()
    def on_actionRedo_triggered(self):
        doText = self.FileState.redoText()
        self.FileState.redo()
        print("Redo - {}".format(doText))
    @pyqtSlot(int)
    def commandReload(self, index=0):
        self.File.Lists.updateAll(self.Entiteis_Point,
            self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Shaft, self.Slider, self.Rod, self.Parameter_list)
        self.Resolve()
        if self.FileState.index()!=self.File.Stack: self.workbookNoSave()
        else: self.workbookSaved()
    
    #Resolve
    def Resolve(self):
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = self.File.Obstacles_Exclusion()
        #Solve
        result = False
        result, DOF, script = slvsProcess(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, self.Parameter_list)
        self.File.Script = script
        if result:
            self.Solvefail = False
            self.File.Lists.currentPos(self.Entiteis_Point, result)
            self.DOF = DOF
            self.DOFview.setText("{} ({})".format(self.DOF-6+self.Shaft.rowCount(), self.DOF-6))
            self.DOFLable.setText("<html><head/><body><p><span style=\" color:#000000;\">DOF:</span></p></body></html>")
            self.Reload_Canvas()
        else:
            self.DOFview.setText("Failed.")
            self.DOFLable.setText("<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">DOF:</span></p></body></html>")
            self.Solvefail = True
            if "-w" in sys.argv: print("Rebuild the cavanc failed.")
    #Reload Canvas
    def Reload_Canvas(self):
        self.qpainterWindow.update_figure(
            float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList,
            self.File.Lists.ParameterList, self.Entiteis_Point_Style, self.ZoomText.text(), self.Font_size.value(),
            self.actionDisplay_Dimensions.isChecked(), self.actionDisplay_Point_Mark.isChecked(), self.action_Black_Blackground.isChecked(),
            self.File.Lists.data, self.File.Lists.runList, self.File.Lists.shaftList)
    
    #Workbook Change
    def workbookNoSave(self):
        self.File.form['changed'] = True
        self.setWindowTitle(self.windowTitle().replace('*', str())+'*')
        actionEnabled(self)
    def workbookSaved(self):
        self.File.form['changed'] = False
        self.setWindowTitle(self.windowTitle().replace('*', str()))
        actionEnabled(self)
    
    @pyqtSlot()
    def on_action_Get_Help_triggered(self): self.OpenURL("http://project.mde.tw/blog/slvs-library-functions.html")
    @pyqtSlot()
    def on_actionGit_hub_Site_triggered(self): self.OpenURL("https://github.com/KmolYuan/python-solvespace")
    @pyqtSlot()
    def on_actionGithub_Wiki_triggered(self): self.OpenURL("https://github.com/KmolYuan/Pyslvs-manual/tree/master")
    @pyqtSlot()
    def on_actionHow_to_use_triggered(self): self.OpenDlg(Help_info_show())
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self): self.OpenDlg(version_show())
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self): self.OpenDlg(Info_show())
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self): self.OpenDlg(Script_Dialog(self.File.Script, self.Default_Environment_variables))
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
    #Workbook Functions
    def checkChange(self, name=False, data=list(), say='Loading Example...'):
        if self.File.form['changed']:
            reply = QMessageBox.question(self, 'Clear Message', "Do you want to Clear ALL Drawings?\nThe changes can't be recovery!",
                (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            if reply==QMessageBox.Apply: self.loadWorkbook(say, name, data)
        else: self.loadWorkbook(say, name, data)
    def loadWorkbook(self, say, fileName=False, data=list()):
        print(say)
        self.closePanels()
        self.File.reset(self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain,
            self.Shaft, self.Slider, self.Rod, self.Parameter_list)
        self.Resolve()
        self.FileState.clear()
        self.setWindowTitle(_translate("MainWindow", "Pyslvs - [New Workbook]"))
        print("Reset workbook.")
        if fileName==False:
            fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', self.Default_Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
            if fileName: self.Default_Environment_variables = QFileInfo(fileName).absolutePath()
        if QFileInfo(fileName).suffix()=="csv" or QFileInfo(fileName).suffix()=="txt" or ("[Example]" in fileName) or ("[New Workbook]" in fileName):
            if data==list():
                print("Get: "+fileName)
                with open(fileName, newline=str()) as stream:
                    reader = csv.reader(stream, delimiter=' ', quotechar='|')
                    for row in reader: data += ' '.join(row).split('\t,')
            if self.File.check(data):
                self.File.read(fileName, data,
                    self.Entiteis_Point, self.Entiteis_Point_Style,
                    self.Entiteis_Link, self.Entiteis_Stay_Chain,
                    self.Shaft, self.Slider, self.Rod, self.Parameter_list)
                for i in range(1, self.Entiteis_Point_Style.rowCount()):
                    self.Entiteis_Point_Style.cellWidget(i, 1).currentIndexChanged.connect(self.Point_Style_set)
                    self.Entiteis_Point_Style.cellWidget(i, 3).currentIndexChanged.connect(self.Point_Style_set)
                self.File.form['changed'] = False
                self.setWindowTitle(_translate("MainWindow", "Pyslvs - {}".format(QFileInfo(fileName).fileName())))
                if (bool(self.File.Lists.data) and bool(self.File.Lists.runList)): self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Path Data Exist</span></p></body></html>"))
                else: self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">No Path Data</span></p></body></html>"))
                self.Path_Clear.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                self.Path_coordinate.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                self.Path_data_show.setEnabled(bool(self.File.Lists.data) and bool(self.File.Lists.runList))
                print("Loaded the workbook.")
                actionEnabled(self)
                if not("[New Workbook]" in fileName):
                    dlg = fileInfo_show()
                    dlg.rename(self.File.form['fileName'].fileName(), self.File.form['author'], self.File.form['description'], self.File.form['lastTime'])
                    dlg.show()
                    if dlg.exec_(): pass
            else: print("Failed to load!")
    
    @pyqtSlot()
    def on_actionSave_triggered(self):
        n = self.File.form['fileName'].absoluteFilePath()
        if "[New Workbook]" in n or "[Example]" in n: fileName = self.outputTo("Workbook", 'Spreadsheet(*.csv)')
        else: fileName = self.File.form['fileName'].absoluteFilePath()
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
        print("Successful Save: {}".format(fileName))
        self.File.form['changed'] = False
        self.setWindowTitle(_translate("MainWindow", "Pyslvs - {}".format(QFileInfo(fileName).fileName())))
    @pyqtSlot()
    def on_action_Output_to_Solvespace_triggered(self):
        dlg = slvsTypeSettings(self.Default_Environment_variables, self.File.form['fileName'].baseName(),
            self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList)
        dlg.show()
        if dlg.exec_():
            reply = QMessageBox.question(self, 'Message', "The conversion was successful.", (QMessageBox.Ok), QMessageBox.Ok)
            if reply: print("Successful Saved Solvespace model.")
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        fileName = self.outputTo("Python Script", 'Python Script(*.py)')
        if fileName:
            with open(fileName, 'w', newline=str()) as f: f.write(self.File.Script)
            print("Successful Save: "+fileName)
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        fileName = self.outputTo("picture", "Portable Network Graphics (*.png);;Joint Photographic Experts Group (*.jpg);;Joint Photographic Experts Group (*.jpeg);;Bitmap Image file (*.bmp);;\
            Business Process Model (*.bpm);;Tagged Image File Format (*.tiff);;Tagged Image File Format (*.tif);;Windows Icon (*.ico);;Wireless Application Protocol Bitmap (*.wbmp);;\
            X BitMap (*.xbm);;X Pixmap (*.xpm)")
        if fileName:
            pixmap = self.qpainterWindow.grab()
            pixmap.save(fileName, format = QFileInfo(fileName).suffix())
            print("Successful Save: "+fileName)
    @pyqtSlot()
    def on_actionOutput_to_DXF_triggered(self):
        fileName = self.outputTo("DXF", 'AutoCAD DXF (*.dxf)')
        if fileName:
            dxfCode(fileName, self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList, self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self.Parameter_list)
            print("Successful Save: "+fileName)
    @pyqtSlot()
    def on_action_Output_to_S_QLite_Data_Base_triggered(self):
        fileName = self.outputTo("Data Base", 'Data Base(*.db)')
        if fileName:
            print("Successful Save: "+fileName)
            #TODO: SQLite
    def outputTo(self, formatName, formatChoose):
        print("Saving to {}...".format(formatName))
        fileName, form = QFileDialog.getSaveFileName(self, 'Save file...', self.Default_Environment_variables, formatChoose)
        if fileName:
            self.Default_Environment_variables = QFileInfo(fileName).absolutePath()
            suffix = form.split('*')[-1][:-1]
            fileName = self.Default_Environment_variables+'/'+QFileInfo(fileName).baseName()+suffix
            print("Formate: {}".format(form))
        return fileName
    
    @pyqtSlot()
    def on_action_Property_triggered(self):
        dlg = editFileInfo_show()
        self.File.updateTime()
        dlg.rename(self.File.form['fileName'].fileName(), self.File.form['author'], self.File.form['description'], self.File.form['lastTime'])
        dlg.show()
        if dlg.exec_():
            self.File.updateAuthorDescription(dlg.authorName_input.text(), dlg.descriptionText.toPlainText())
            self.workbookNoSave()
    
    def on_parameter_add(self):
        self.File.Lists.editParameterTable(self.Parameter_list)
        self.workbookNoSave()
        self.Mask_Change()
    def on_parameter_del(self):
        self.File.Lists.deleteParameterTable(self.Parameter_list)
        self.Resolve()
        self.workbookNoSave()
        self.Mask_Change()
    @pyqtSlot()
    def on_Parameter_add_clicked(self): self.on_parameter_add()
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        dlg = edit_point_show(self.Mask, table1)
        dlg.show()
        if dlg.exec_():
            x = dlg.X_coordinate.text() if not dlg.X_coordinate.text() in [str(), "n", "-"] else dlg.X_coordinate.placeholderText()
            y = dlg.Y_coordinate.text() if not dlg.Y_coordinate.text() in [str(), "n", "-"] else dlg.Y_coordinate.placeholderText()
            self.File.Lists.editTable(table1, 'Point', False, x, y, bool(dlg.Fix_Point.checkState()),
            **{'styleTable':table2, 'color':'Green', 'ringsize':'10' if dlg.Fix_Point.checkState() else '5', 'ringcolor':'Green'})
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text() if not self.X_coordinate.text() in [str(), "n", "-"] else self.X_coordinate.placeholderText()
        y = self.Y_coordinate.text() if not self.Y_coordinate.text() in [str(), "n", "-"] else self.Y_coordinate.placeholderText()
        self.File.Lists.editTable(table1, 'Point', False, x, y, False, **{'styleTable':table2, 'color':'Green', 'ringsize':'5', 'ringcolor':'Green'})
        self.X_coordinate.clear()
        self.Y_coordinate.clear()
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self, pos=1):
        table = self.Entiteis_Point
        dlg = edit_point_show(self.Mask, table, pos)
        dlg.Another_point.connect(self.Change_Edit_Point)
        self.point_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Point(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table, 'Point', pos,
                dlg.X_coordinate.text() if not dlg.X_coordinate.text()in[str(), "n", "-"] else dlg.X_coordinate.placeholderText(),
                dlg.Y_coordinate.text() if not dlg.Y_coordinate.text()in[str(), "n", "-"] else dlg.Y_coordinate.placeholderText(),
                bool(dlg.Fix_Point.checkState()))
            self.File.Lists.styleFix(self.Entiteis_Point_Style, bool(dlg.Fix_Point.checkState()), pos)
            self.closePanels()
    point_feedback = pyqtSignal(float, float, bool)
    @pyqtSlot(int)
    def Change_Edit_Point(self, pos):
        thisTable = self.File.Lists.PointList[pos]
        self.point_feedback.emit(thisTable['x'], thisTable['y'], thisTable['fix'])
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        dlg = edit_link_show(self.Mask, table1, table2)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Line', False, dlg.Start_Point.currentText(), dlg.End_Point.currentText(), dlg.len)
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        dlg = edit_link_show(self.Mask, table1, table2, pos)
        dlg.Another_line.connect(self.Change_Edit_Line)
        self.link_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Line(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table2, 'Line', pos, dlg.Start_Point.currentText(), dlg.End_Point.currentText(), dlg.len)
            self.closePanels()
    link_feedback = pyqtSignal(int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Line(self, pos):
        thisTable = self.File.Lists.LineList[pos]
        self.link_feedback.emit(thisTable['start'], thisTable['end'], thisTable['len'])
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        dlg = edit_chain_show(self.Mask, table1, table2)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Chain', False, dlg.p1, dlg.p2, dlg.p3, dlg.p1_p2Val, dlg.p2_p3Val, dlg.p1_p3Val)
    
    @pyqtSlot()
    def on_actionEdit_Stay_Chain_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        dlg = edit_chain_show(self.Mask, table1, table2, pos)
        dlg.Another_chain.connect(self.Change_Edit_Chain)
        self.chain_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Chain(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table2, 'Chain', pos, dlg.p1, dlg.p2, dlg.p3, dlg.p1_p2Val, dlg.p2_p3Val, dlg.p1_p3Val)
            self.closePanels()
    chain_feedback = pyqtSignal(int, int, int, float, float, float)
    @pyqtSlot(int)
    def Change_Edit_Chain(self, pos):
        thisTable = self.File.Lists.ChainList[pos]
        self.chain_feedback.emit(thisTable['p1'], thisTable['p2'], thisTable['p3'], thisTable['p1p2'], thisTable['p2p3'], thisTable['p1p3'])
    
    @pyqtSlot()
    def on_action_Set_Shaft_triggered(self, cen=0, ref=0):
        table1 = self.Entiteis_Point
        table2 = self.Shaft
        dlg = edit_shaft_show(table1, table2, cen=cen, ref=ref)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Shaft', False,
            dlg.center, dlg.ref, dlg.start, dlg.end, dlg.start, bool(dlg.isParallelogram.checkState()))
    
    @pyqtSlot()
    def on_action_Edit_Shaft_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Shaft
        dlg = edit_shaft_show(table1, table2, pos)
        dlg.Another_shaft.connect(self.Change_Edit_Shaft)
        self.shaft_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Shaft(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table2, 'Shaft', pos, dlg.center, dlg.ref, dlg.start, dlg.end,
                table2.item(dlg.Shaft.currentIndex(), 5), bool(dlg.isParallelogram.checkState()))
            self.closePanels()
    shaft_feedback = pyqtSignal(int, int, float, float)
    @pyqtSlot(int)
    def Change_Edit_Shaft(self, pos):
        table = self.Shaft
        center = int(table.item(pos, 1).text().replace("Point", str()))
        references = int(table.item(pos, 2).text().replace("Point", str()))
        start = float(table.item(pos, 3).text())
        end = float(table.item(pos, 4).text())
        self.shaft_feedback.emit(center, references, start, end)
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        dlg = edit_slider_show(self.Entiteis_Point, self.Slider)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(self.Slider, 'Slider', False, dlg.slider, dlg.start, dlg.end)
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self, pos=0):
        dlg = edit_slider_show(self.Entiteis_Point, self.Slider, pos)
        dlg.Another_slider.connect(self.Change_Edit_Slider)
        self.slider_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Slider(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(self.Slider, 'Slider', pos, dlg.slider, dlg.start)
            self.closePanels()
    slider_feedback = pyqtSignal(int, int, int)
    @pyqtSlot(int)
    def Change_Edit_Slider(self, pos):
        thisTable = self.File.Lists.SliderList[pos]
        self.slider_feedback.emit(thisTable['cen'], thisTable['start'], thisTable['end'])
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        dlg = edit_rod_show(table1, table2)
        dlg.show()
        if dlg.exec_(): self.File.Lists.editTable(table2, 'Rod', False, dlg.cen, dlg.start, dlg.end, dlg.pos)
    
    @pyqtSlot()
    def on_action_Edit_Rod_triggered(self, pos=0):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        dlg = edit_rod_show(table1, table2, pos)
        dlg.Another_rod.connect(self.Change_Edit_Rod)
        self.rod_feedback.connect(dlg.change_feedback)
        self.Change_Edit_Rod(pos)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.editTable(table2, 'Rod', pos, dlg.cen, dlg.start, dlg.end, dlg.pos)
            self.closePanels()
    rod_feedback = pyqtSignal(int, int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Rod(self, pos):
        thisTable = self.File.Lists.RodList[pos]
        self.rod_feedback.emit(thisTable['cen'], thisTable['start'], thisTable['end'], thisTable['pos'])
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self, pos = 1): self.deletePanel(self.Entiteis_Point, 'Point', ":/icons/delete.png", ":/icons/point.png", pos)
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self, pos = 0): self.deletePanel(self.Entiteis_Link, 'Line', ":/icons/deleteline.png", ":/icons/line.png", pos)
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self, pos = 0): self.deletePanel(self.Entiteis_Stay_Chain, 'Chain', ":/icons/deletechain.png", ":/icons/equal.png", pos)
    @pyqtSlot()
    def on_actionDelete_Shaft_triggered(self, pos=0): self.deletePanel(self.Shaft, 'Shaft', ":/icons/deleteshaft.png", ":/icons/circle.png", pos)
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self, pos=0): self.deletePanel(self.Slider, 'Slider', ":/icons/deleteslider.png", ":/icons/pointonx.png", pos)
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self, pos=0): self.deletePanel(self.Rod, 'Rod',
        QIcon(QPixmap(":/icons/deleterod.png")), QIcon(QPixmap(":/icons/spring.png")), pos)
    def deletePanel(self, table, name, icon1, icon2, pos):
        dlg = deleteDlg(QIcon(QPixmap(icon1)), QIcon(QPixmap(icon2)), table, pos)
        dlg.show()
        if dlg.exec_():
            if name=='Point': self.File.Lists.deletePointTable(self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link,
                self.Entiteis_Stay_Chain, self.Shaft, self.Slider, self.Rod, self.Parameter_list, dlg.Entity.currentIndex())
            else: self.File.Lists.deleteTable(table, name, dlg.Entity.currentIndex())
            self.closePanels()
    
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
    
    @pyqtSlot()
    def on_ResetCanvas_clicked(self): self.qpainterWindow.SetIn()
    @pyqtSlot()
    def on_FitW_clicked(self):
        self.Fit2H()
        self.Fit2W()
    def Fit2W(self):
        for i in range(10):
            max_pt = max(self.qpainterWindow.points['x'])
            min_pt = min(self.qpainterWindow.points['x'])
            self.qpainterWindow.points['origin']['x'] = (self.qpainterWindow.width()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.qpainterWindow.width()/(max_pt+min_pt+100))
            self.Reload_Canvas()
    @pyqtSlot()
    def on_FitH_clicked(self):
        self.Fit2W()
        self.Fit2H()
    def Fit2H(self):
        for i in range(10):
            max_pt = max(self.qpainterWindow.points['y'])
            min_pt = min(self.qpainterWindow.points['y'])
            self.qpainterWindow.points['origin']['y'] = (self.qpainterWindow.height()-(max_pt+min_pt))/2
            self.ZoomBar.setValue(self.ZoomBar.value()*self.qpainterWindow.height()/(max_pt-min_pt+100))
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
    def on_actionDisplay_Dimensions_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Point_Mark_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Black_Blackground_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def Point_Style_set(self, index):
        self.Reload_Canvas()
        self.workbookNoSave()
    @pyqtSlot()
    def on_Path_data_show_clicked(self):
        self.qpainterWindow.points['Path']['show'] = self.Path_data_show.checkState()
        self.Reload_Canvas()
    @pyqtSlot()
    def on_Path_points_show_clicked(self):
        self.qpainterWindow.points['slvsPath']['show'] = self.Path_points_show.checkState()
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_PathTrack_clicked(self):
        table1 = self.Entiteis_Point
        dlg = Path_Track_show(self.File.Lists.PointList, self.File.Lists.LineList, self.File.Lists.ChainList,
            self.File.Lists.ShaftList, self.File.Lists.SliderList, self.File.Lists.RodList, self.Parameter_list)
        self.actionDisplay_Point_Mark.setChecked(True)
        dlg.show()
        if dlg.exec_():
            self.File.Lists.setPath(dlg.Path_data, [dlg.Run_list.item(i).text() for i in range(dlg.Run_list.count())], dlg.work.ShaftList)
            self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Path Data Exist</span></p></body></html>"))
            self.Path_Clear.setEnabled(True)
            self.Path_coordinate.setEnabled(True)
            self.Path_data_show.setEnabled(True)
    @pyqtSlot()
    def on_Path_Clear_clicked(self):
        self.File.Lists.clearPath()
        self.Reload_Canvas()
        self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">No Path Data</span></p></body></html>"))
        self.Path_Clear.setEnabled(False)
        self.Path_coordinate.setEnabled(False)
        self.Path_data_show.setEnabled(False)
    @pyqtSlot()
    def on_Path_coordinate_clicked(self):
        dlg = path_point_data_show(self.Default_Environment_variables, self.File.Lists.data, self.File.Lists.runList)
        dlg.show()
        dlg.exec()
    
    @pyqtSlot(bool)
    def on_PathSolving_toggled(self, p0):
        if not hasattr(self, 'PathSolvingDlg'):
            self.PathSolvingDlg = Path_Solving_show(self.Mask, self.File.PathSolvingReqs.list, self.File.PathSolvingReqs.result, self.width())
            self.PathSolving.toggled.connect(self.PathSolvingDlg.reject)
            self.PathSolvingDlg.addPathPoint.connect(self.PathSolving_add)
            self.PathSolvingDlg.deletePathPoint.connect(self.PathSolving_delete)
            self.PathSolvingDlg.rejected.connect(self.PathSolving_return)
            self.PathSolvingDlg.Generate.clicked.connect(self.PathSolving_send)
            self.PathSolvingDlg.moveupPathPoint.connect(self.PathSolving_moveup)
            self.PathSolvingDlg.movedownPathPoint.connect(self.PathSolving_movedown)
            self.PathSolvingDlg.mergeMechanism.connect(self.PathSolving_merge)
            self.PathSolvingDlg.Listbox.deleteResult.connect(self.PathSolving_deleteResult)
            self.PathSolvingDlg.Listbox.mergeResult.connect(self.PathSolving_mergeResult)
            self.PathSolvingStart.connect(self.PathSolvingDlg.start)
            self.PathSolvingDlg.show()
            self.PointTab.addTab(self.PathSolvingDlg.Listbox, QIcon(QPixmap(":/icons/bezier.png")), "Thinking list")
            self.PathSolvingDlg.Listbox.show()
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
            if self.PathSolvingDlg.exec_(): pass
        else: self.closePanel(self.PathSolvingDlg, 'PathSolvingDlg', self.PathSolving)
    @pyqtSlot()
    def PathSolving_return(self): self.PathSolving.setChecked(False)
    def PathSolving_add_rightClick(self, x, y):
        self.PathSolvingDlg.addPath(x, y)
        self.PathSolving_add(x, y)
    @pyqtSlot(float, float)
    def PathSolving_add(self, x=0, y=0):
        self.File.PathSolvingReqs.add(x, y)
        self.qpainterWindow.path_solving(self.File.PathSolvingReqs.list, self.File.PathSolvingReqs.result)
        self.workbookNoSave()
    @pyqtSlot(int)
    def PathSolving_delete(self, row):
        self.File.PathSolvingReqs.remove(row)
        self.qpainterWindow.path_solving(self.File.PathSolvingReqs.list, self.File.PathSolvingReqs.result)
        self.workbookNoSave()
    @pyqtSlot(int)
    def PathSolving_moveup(self, row):
        self.File.PathSolvingReqs.moveUP(row)
        self.qpainterWindow.path_solving(self.File.PathSolvingReqs.list, self.File.PathSolvingReqs.result)
    @pyqtSlot(int)
    def PathSolving_movedown(self, row):
        self.File.PathSolvingReqs.moveDown(row)
        self.qpainterWindow.path_solving(self.File.PathSolvingReqs.list, self.File.PathSolvingReqs.result)
    PathSolvingStart = pyqtSignal(list)
    @pyqtSlot()
    def PathSolving_send(self): self.PathSolvingStart.emit(self.File.PathSolvingReqs.list)
    @pyqtSlot(list)
    def PathSolving_merge(self, mechanism_data): self.File.PathSolvingReqs.resultMerge(mechanism_data)
    @pyqtSlot(int)
    def PathSolving_deleteResult(self, row): self.File.PathSolvingReqs.removeResult(row)
    @pyqtSlot(int)
    def PathSolving_mergeResult(self, row): self.File.Generate_Merge(row, slvsProcess(generateResult=self.File.PathSolvingReqs.result[row]),
            self.Entiteis_Point, self.Entiteis_Point_Style, self.Entiteis_Link, self.Entiteis_Stay_Chain, self.Shaft)
    
    @pyqtSlot()
    def on_Drive_shaft_clicked(self):
        if not hasattr(self, 'DriveShaftWidget'):
            self.DriveShaftWidget = Drive_shaft_show(self.File.Lists.ShaftList)
            self.PointTab.addTab(self.DriveShaftWidget, QIcon(QPixmap(":/icons/same-orientation.png")), 'Drive Shaft')
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
            self.DriveShaftWidget.Degree.sliderReleased.connect(self.Save_demo_angle)
            self.DriveShaftWidget.Degree.valueChanged.connect(self.Change_demo_angle)
        else: self.closePanel(self.DriveShaftWidget, 'DriveShaftWidget', self.Drive_shaft)
    @pyqtSlot()
    def Save_demo_angle(self): self.File.Lists.saveDemo(self.Shaft, 'Shaft', self.DriveShaftWidget.Degree.value()/100, 0, 5)
    @pyqtSlot(int)
    def Change_demo_angle(self, angle):
        self.File.Lists.setDemo('Shaft', 0, angle/100)
        self.Resolve()
        self.workbookNoSave()
    
    @pyqtSlot()
    def on_Drive_rod_clicked(self):
        if not hasattr(self, 'DriveRodWidget'):
            self.DriveRodWidget = Drive_rod_show(self.File.Lists.RodList, self.File.Lists.PointList)
            self.PointTab.addTab(self.DriveRodWidget, QIcon(QPixmap(":/icons/normal.png")), 'Drive Rod')
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
            self.DriveRodWidget.Position.sliderReleased.connect(self.Save_position)
            self.DriveRodWidget.Position.valueChanged.connect(self.Change_position)
        else: self.closePanel(self.DriveRodWidget, 'DriveRodWidget', self.Drive_rod)
    @pyqtSlot()
    def Save_position(self):self.File.Lists.saveDemo(self.Rod, 'Rod', self.DriveRodWidget.Position.value()/100, self.DriveRodWidget.Rod.currentIndex(), 4)
    @pyqtSlot(int)
    def Change_position(self, pos):
        self.File.Lists.setDemo('Rod', self.DriveRodWidget.Rod.currentIndex(), pos/100)
        self.Resolve()
        self.workbookNoSave()
    
    @pyqtSlot()
    def on_Measurement_clicked(self):
        if not hasattr(self, 'MeasurementWidget'):
            table = self.Entiteis_Point
            self.MeasurementWidget = Measurement_show(table)
            self.PointTab.addTab(self.MeasurementWidget, QIcon(QPixmap(":/icons/ref.png")), 'Measurement')
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
            self.qpainterWindow.change_event.connect(self.MeasurementWidget.Detection_do)
            self.actionDisplay_Dimensions.setChecked(True)
            self.actionDisplay_Point_Mark.setChecked(True)
            self.qpainterWindow.mouse_track.connect(self.MeasurementWidget.show_mouse_track)
            self.MeasurementWidget.point_change.connect(self.distance_solving)
            self.distance_changed.connect(self.MeasurementWidget.change_distance)
            self.MeasurementWidget.Mouse.setPlainText("Detecting")
        else: self.closePanel(self.MeasurementWidget, 'MeasurementWidget', self.Measurement)
    distance_changed = pyqtSignal(float)
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        start = self.Entiteis_Point.item(start, 4).text().replace('(', str()).replace(')', str())
        end = self.Entiteis_Point.item(end, 4).text().replace('(', str()).replace(')', str())
        x = float(start.split(", ")[0])-float(end.split(", ")[0])
        y = float(start.split(", ")[1])-float(end.split(", ")[1])
        self.distance_changed.emit(round(math.sqrt(x**2+y**2), 9))
    
    @pyqtSlot()
    def on_AuxLine_clicked(self):
        if not hasattr(self, 'AuxLineWidget'):
            self.qpainterWindow.AuxLine['show'] = True
            self.qpainterWindow.AuxLine['horizontal'] = True
            self.qpainterWindow.AuxLine['vertical'] = True
            table = self.Entiteis_Point
            self.AuxLineWidget = AuxLine_show(table, self.qpainterWindow.AuxLine['pt'], self.qpainterWindow.AuxLine['color'], self.qpainterWindow.AuxLine['limit_color'])
            self.AuxLineWidget.Point_change.connect(self.draw_Auxline)
            self.PointTab.addTab(self.AuxLineWidget, QIcon(QPixmap(":/icons/auxline.png")), 'Auxiliary Line')
            self.PointTab.setCurrentIndex(self.PointTab.count()-1)
        else:
            self.closePanel(self.AuxLineWidget, 'AuxLineWidget', self.AuxLine)
            self.qpainterWindow.reset_Auxline()
        self.Reload_Canvas()
    @pyqtSlot(int, int, int, bool, bool, bool, bool, bool)
    def draw_Auxline(self, pt, color, color_l, axe_H, axe_V, max_l, min_l, pt_change):
        self.qpainterWindow.AuxLine['pt'] = pt
        self.qpainterWindow.AuxLine['color'] = color
        self.qpainterWindow.AuxLine['limit_color'] = color_l
        if pt_change: self.qpainterWindow.Reset_Aux_limit()
        self.qpainterWindow.AuxLine['horizontal'] = axe_H
        self.qpainterWindow.AuxLine['vertical'] = axe_V
        self.qpainterWindow.AuxLine['isMax'] = max_l
        self.qpainterWindow.AuxLine['isMin'] = min_l
        self.Reload_Canvas()
    
    @pyqtSlot()
    def on_actionClose_all_panels_triggered(self): self.closePanels()
    def closePanels(self):
        if hasattr(self, 'PathSolvingDlg'): self.closePanel(self.PathSolvingDlg, 'PathSolvingDlg', self.PathSolving)
        if hasattr(self, 'DriveShaftWidget'): self.closePanel(self.DriveShaftWidget, 'DriveShaftWidget', self.Drive_shaft)
        if hasattr(self, 'DriveRodWidget'): self.closePanel(self.DriveRodWidget, 'DriveRodWidget', self.Drive_rod)
        if hasattr(self, 'MeasurementWidget'): self.closePanel(self.MeasurementWidget, 'MeasurementWidget', self.Measurement)
        if hasattr(self, 'AuxLineWidget'): self.closePanel(self.AuxLineWidget, 'AuxLineWidget', self.AuxLine)
        self.qpainterWindow.reset_Auxline()
        self.PointTab.setCurrentIndex(0)
    def closePanel(self, panel, name, button):
        panel.deleteLater()
        delattr(self, name)
        button.setChecked(False)
    
    def Mask_Change(self):
        row_Count = str(self.Parameter_list.rowCount()-1)
        param = '(('
        for i in range(len(row_Count)): param += '[1-'+row_Count[i]+']' if i==0 and not len(row_Count)<=1 else '[0-'+row_Count[i]+']'
        param += ')|'
        param_100 = '[0-9]{0,'+str(len(row_Count)-2)+'}' if len(row_Count)>2 else str()
        param_20 = '([1-'+str(int(row_Count[0])-1)+']'+param_100+')?' if self.Parameter_list.rowCount()>19 else str()
        if len(row_Count)>1: param += param_20+'[0-9]'
        param += ')'
        param_use = '^[n]'+param+'$|' if self.Parameter_list.rowCount()>=1 else str()
        mask = '('+param_use+'^[-]?([1-9][0-9]{0,6})?[0-9][.][0-9]{1,8}$)'
        self.Mask = QRegExpValidator(QRegExp(mask))
        self.X_coordinate.setValidator(self.Mask)
        self.Y_coordinate.setValidator(self.Mask)
    
    @pyqtSlot(int, int, int, int)
    def on_Parameter_list_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        try:
            self.Parameter_num.setPlainText("n"+str(currentRow))
            self.Parameter_digital.setPlaceholderText(str(self.Parameter_list.item(currentRow, 1).text()))
            self.Parameter_digital.clear()
        except:
            self.Parameter_num.setPlainText("N/A")
            self.Parameter_digital.setPlaceholderText("0.0")
            self.Parameter_digital.clear()
        self.Parameter_num.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_digital.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_lable.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
        self.Parameter_update.setEnabled(self.Parameter_list.rowCount()>0 and currentRow>-1)
    @pyqtSlot()
    def on_Parameter_update_clicked(self):
        try: self.Parameter_list.setItem(self.Parameter_list.currentRow(), 1, QTableWidgetItem(self.Parameter_digital.text() if self.Parameter_digital.text() else Parameter_digital.placeholderText()))
        except: pass
    @pyqtSlot(int, int, int, int)
    def on_Entiteis_Point_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        self.X_coordinate.setPlaceholderText(self.Entiteis_Point.item(currentRow, 1).text())
        self.Y_coordinate.setPlaceholderText(self.Entiteis_Point.item(currentRow, 2).text())
    @pyqtSlot(int, int)
    def on_Parameter_list_cellChanged(self, row, column):
        if column in [1, 2]: self.Parameter_list.item(row, column).setToolTip(self.Parameter_list.item(row, column).text())
    
    @pyqtSlot()
    def on_action_Prefenece_triggered(self):
        dlg = options_show()
        color_list = self.qpainterWindow.re_Color
        for i in range(len(color_list)): dlg.LinkingLinesColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.StayChainColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.AuxiliaryLineColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.AuxiliaryLimitLineColor.insertItem(i, color_list[i])
        for i in range(len(color_list)): dlg.TextColor.insertItem(i, color_list[i])
        dlg.show()
        if dlg.exec_(): pass
