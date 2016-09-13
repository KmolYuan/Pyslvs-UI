# -*- coding: utf-8 -*-
#CSV & SQLite
import csv, math
from peewee import *
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
_translate = QCoreApplication.translate
#UI Ports
from .Ui_main import Ui_MainWindow
import webbrowser
#Dialog Ports
from .info.version import version_show
from .info.color import color_show
from .info.info import Info_show
from .info.help import Help_info_show
from .info.script import Script_Dialog
from .info.path_point_data import path_point_data_show
#Warning Dialog Ports
from .warning.reset_workbook import reset_show
from .warning.zero_value import zero_show
from .warning.repeated_value import same_show
from .warning.restriction_conflict import restriction_conflict_show
from .warning.kill_origin import kill_origin_show
from .warning.resolution_fail import resolution_fail_show
#Drawing Dialog Ports
from .draw.draw_point import New_point
from .draw.draw_link import New_link
from .draw.draw_stay_chain import chain_show
from .draw.draw_edit_point import edit_point_show
from .draw.draw_edit_link import edit_link_show
from .draw.draw_edit_stay_chain import edit_stay_chain_show
#Delete Dialog Ports
from .draw.draw_delete_point import delete_point_show
from .draw.draw_delete_linkage import delete_linkage_show
from .draw.draw_delete_chain import delete_chain_show
from .simulate.delete_drive_shaft import delete_shaft_show
from .simulate.delete_slider import delete_slider_show
from .simulate.delete_rod import delete_rod_show
#Simulate Dialog Ports
from .simulate.set_drive_shaft import shaft_show
from .simulate.set_slider import slider_show
from .simulate.set_rod import rod_show
from .simulate.edit_drive_shaft import edit_shaft_show
from .simulate.edit_slider import edit_slider_show
from .simulate.edit_rod import edit_rod_show
from .simulate.run_Path_Track import Path_Track_show
from .simulate.run_Drive import Drive_show
from .simulate.run_Measurement import Measurement_show
#DynamicCanvas
from .canvas import DynamicCanvas
#Solve
from .calculation import Solvespace
from .list_process import *

Environment_variables = "../"

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #No Save
        self.Workbook_Change = False
        #mpl Window
        self.qpainterWindow = DynamicCanvas()
        self.qpainterWindow.setStatusTip(_translate("MainWindow",
            "Press Ctrl Key and use mouse to Change Origin or Zoom Size."))
        self.mplLayout.insertWidget(0, self.qpainterWindow)
        self.qpainterWindow.show()
        #Script & Path
        self.Script = ""
        self.Path_data = []
        self.Path_Run_list = []
        #Mask
        self.Mask = None
        self.Mask_Change()
        #qpainterWindow Right-click menu
        self.qpainterWindow.setContextMenuPolicy(Qt.CustomContextMenu)
        self.qpainterWindow.customContextMenuRequested.connect(self.on_painter_context_menu)
        self.popMenu_painter = QMenu(self)
        self.action_painter_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_painter.addAction(self.action_painter_right_click_menu_add)
        self.mouse_pos_x = 0.0
        self.mouse_pos_y = 0.0
        self.qpainterWindow.mouse_track.connect(self.context_menu_mouse_pos)
        #Entiteis_Point Right-click menu
        self.Entiteis_Point_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Point_Widget.customContextMenuRequested.connect(self.on_point_context_menu)
        self.popMenu_point = QMenu(self)
        self.action_point_right_click_menu_add = QAction("Add a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_add)
        self.action_point_right_click_menu_edit = QAction("Edit a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_edit)
        self.popMenu_point.addSeparator()
        self.action_point_right_click_menu_delete = QAction("Delete a Point", self)
        self.popMenu_point.addAction(self.action_point_right_click_menu_delete) 
        #Entiteis_Link Right-click menu
        self.Entiteis_Link_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Link_Widget.customContextMenuRequested.connect(self.on_link_context_menu)
        self.popMenu_link = QMenu(self)
        self.action_link_right_click_menu_add = QAction("Add a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_add)
        self.action_link_right_click_menu_edit = QAction("Edit a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_edit)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_up)
        self.action_link_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_move_down)
        self.popMenu_link.addSeparator()
        self.action_link_right_click_menu_delete = QAction("Delete a Link", self)
        self.popMenu_link.addAction(self.action_link_right_click_menu_delete) 
        #Entiteis_Chain Right-click menu
        self.Entiteis_Stay_Chain_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Entiteis_Stay_Chain_Widget.customContextMenuRequested.connect(self.on_chain_context_menu)
        self.popMenu_chain = QMenu(self)
        self.action_chain_right_click_menu_add = QAction("Add a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_add)
        self.action_chain_right_click_menu_edit = QAction("Edit a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_edit)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_up)
        self.action_chain_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_move_down)
        self.popMenu_chain.addSeparator()
        self.action_chain_right_click_menu_delete = QAction("Delete a Chain", self)
        self.popMenu_chain.addAction(self.action_chain_right_click_menu_delete) 
        #Drive_Shaft Right-click menu
        self.Drive_Shaft_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Drive_Shaft_Widget.customContextMenuRequested.connect(self.on_shaft_context_menu)
        self.popMenu_shaft = QMenu(self)
        self.action_shaft_right_click_menu_add = QAction("Add a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_add)
        self.action_shaft_right_click_menu_edit = QAction("Edit a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_edit)
        self.popMenu_shaft.addSeparator()
        self.action_shaft_right_click_menu_delete = QAction("Delete a Drive Shaft", self)
        self.popMenu_shaft.addAction(self.action_shaft_right_click_menu_delete) 
        #Slider Right-click menu
        self.Slider_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Slider_Widget.customContextMenuRequested.connect(self.on_slider_context_menu)
        self.popMenu_slider = QMenu(self)
        self.action_slider_right_click_menu_add = QAction("Add a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_add)
        self.action_slider_right_click_menu_edit = QAction("Edit a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_edit)
        self.popMenu_slider.addSeparator()
        self.action_slider_right_click_menu_delete = QAction("Delete a Slider", self)
        self.popMenu_slider.addAction(self.action_slider_right_click_menu_delete) 
        #Rod Right-click menu
        self.Rod_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Rod_Widget.customContextMenuRequested.connect(self.on_rod_context_menu)
        self.popMenu_rod = QMenu(self)
        self.action_rod_right_click_menu_add = QAction("Add a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_add)
        self.action_rod_right_click_menu_edit = QAction("Edit a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_edit)
        self.popMenu_rod.addSeparator()
        self.action_rod_right_click_menu_delete = QAction("Delete a Rod", self)
        self.popMenu_rod.addAction(self.action_rod_right_click_menu_delete)
        #Parameter Right-click menu
        self.Parameter_Widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Parameter_Widget.customContextMenuRequested.connect(self.on_parameter_context_menu)
        self.popMenu_parameter = QMenu(self)
        self.action_parameter_right_click_menu_add = QAction("Add a Parameter", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_add)
        self.popMenu_parameter.addSeparator()
        self.action_parameter_right_click_menu_move_up = QAction("Move up", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_move_up)
        self.action_parameter_right_click_menu_move_down = QAction("Move down", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_move_down)
        self.popMenu_parameter.addSeparator()
        self.action_parameter_right_click_menu_delete = QAction("Delete a Parameter", self)
        self.popMenu_parameter.addAction(self.action_parameter_right_click_menu_delete)
        #Resolve
        self.Resolve()
    
    #Right-click menu event
    def on_painter_context_menu(self, point):
        action = self.popMenu_painter.exec_(self.qpainterWindow.mapToGlobal(point))
        if action == self.action_painter_right_click_menu_add:
            table1 = self.Entiteis_Point
            table2 = self.Entiteis_Point_Style
            x = str(self.mouse_pos_x)
            y = str(self.mouse_pos_y)
            Points_list(table1, "Point"+str(table1.rowCount()), x, y, False, False)
            Points_style_add(table2, "Point"+str(table2.rowCount()), "G", "5", "G")
    @pyqtSlot(float, float)
    def context_menu_mouse_pos(self, x, y):
        self.mouse_pos_x = x
        self.mouse_pos_y = y
    def on_point_context_menu(self, point):
        self.action_point_right_click_menu_edit.setEnabled(self.Entiteis_Point.rowCount()>=2)
        self.action_point_right_click_menu_delete.setEnabled(self.Entiteis_Point.rowCount()>=2)
        action = self.popMenu_point.exec_(self.Entiteis_Point_Widget.mapToGlobal(point))
        table_pos = self.Entiteis_Point.currentRow() if self.Entiteis_Point.currentRow()>=1 else 1
        if action == self.action_point_right_click_menu_add: self.on_action_New_Point_triggered()
        elif action == self.action_point_right_click_menu_edit: self.on_actionEdit_Point_triggered(table_pos)
        elif action == self.action_point_right_click_menu_delete: self.on_actionDelete_Point_triggered()
    def on_link_context_menu(self, point):
        self.action_link_right_click_menu_edit.setEnabled(self.Entiteis_Link.rowCount()>=1)
        self.action_link_right_click_menu_delete.setEnabled(self.Entiteis_Link.rowCount()>=1)
        self.action_link_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()>=1))
        self.action_link_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Link.rowCount()<=1))and(self.Entiteis_Link.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_link.exec_(self.Entiteis_Link_Widget.mapToGlobal(point))
        if action == self.action_link_right_click_menu_add: self.on_action_New_Line_triggered()
        elif action == self.action_link_right_click_menu_edit: self.on_actionEdit_Linkage_triggered(self.Entiteis_Link.currentRow())
        elif action == self.action_link_right_click_menu_move_up: self.move_up(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
        elif action == self.action_link_right_click_menu_move_down: self.move_down(self.Entiteis_Link, self.Entiteis_Link.currentRow(), "Line")
        elif action == self.action_link_right_click_menu_delete: self.on_actionDelete_Linkage_triggered()
    def on_chain_context_menu(self, point):
        self.action_chain_right_click_menu_edit.setEnabled(self.Entiteis_Stay_Chain.rowCount()>=1)
        self.action_chain_right_click_menu_delete.setEnabled(self.Entiteis_Stay_Chain.rowCount()>=1)
        self.action_chain_right_click_menu_move_up.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()>=1))
        self.action_chain_right_click_menu_move_down.setEnabled((not bool(self.Entiteis_Stay_Chain.rowCount()<=1))and(self.Entiteis_Stay_Chain.currentRow()<=self.Entiteis_Link.rowCount()-2))
        action = self.popMenu_chain.exec_(self.Entiteis_Stay_Chain_Widget.mapToGlobal(point))
        if action == self.action_chain_right_click_menu_add: self.on_action_New_Stay_Chain_triggered()
        elif action == self.action_chain_right_click_menu_edit: self.on_actionEdit_Stay_Chain_triggered(self.Entiteis_Stay_Chain.currentRow())
        elif action == self.action_chain_right_click_menu_move_up: self.move_up(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_move_down: self.move_down(self.Entiteis_Stay_Chain, self.Entiteis_Stay_Chain.currentRow(), "Chain")
        elif action == self.action_chain_right_click_menu_delete: self.on_actionDelete_Stay_Chain_triggered()
    def on_shaft_context_menu(self, point):
        self.action_shaft_right_click_menu_edit.setEnabled(self.Drive_Shaft.rowCount()>=1)
        self.action_shaft_right_click_menu_delete.setEnabled(self.Drive_Shaft.rowCount()>=1)
        action = self.popMenu_shaft.exec_(self.Drive_Shaft_Widget.mapToGlobal(point))
        if action == self.action_shaft_right_click_menu_add: self.on_action_Set_Drive_Shaft_triggered()
        elif action == self.action_shaft_right_click_menu_edit: self.on_action_Edit_Drive_Shaft_triggered(self.Drive_Shaft.currentRow())
        elif action == self.action_shaft_right_click_menu_delete: self.on_actionDelete_Drive_Shaft_triggered()
    def on_slider_context_menu(self, point):
        self.action_slider_right_click_menu_edit.setEnabled(self.Slider.rowCount()>=1)
        self.action_slider_right_click_menu_delete.setEnabled(self.Slider.rowCount()>=1)
        action = self.popMenu_slider.exec_(self.Slider_Widget.mapToGlobal(point))
        if action == self.action_slider_right_click_menu_add: self.on_action_Set_Slider_triggered()
        elif action == self.action_slider_right_click_menu_edit: self.on_action_Edit_Slider_triggered()
        elif action == self.action_slider_right_click_menu_delete: self.on_actionDelete_Slider_triggered()
    def on_rod_context_menu(self, point):
        self.action_rod_right_click_menu_edit.setEnabled(self.Rod.rowCount()>=1)
        self.action_rod_right_click_menu_delete.setEnabled(self.Rod.rowCount()>=1)
        action = self.popMenu_rod.exec_(self.Rod_Widget.mapToGlobal(point))
        if action == self.action_rod_right_click_menu_add: self.on_action_Set_Rod_triggered()
        elif action == self.action_rod_right_click_menu_edit: self.on_action_Edit_Piston_Spring_triggered()
        elif action == self.action_rod_right_click_menu_delete: self.on_actionDelete_Piston_Spring_triggered()
    def on_parameter_context_menu(self, point):
        self.action_parameter_right_click_menu_move_up.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(self.Parameter_list.currentRow()>=1))
        self.action_parameter_right_click_menu_move_down.setEnabled((not bool(self.Parameter_list.rowCount()<=1))and(self.Parameter_list.currentRow()<=self.Parameter_list.rowCount()-2))
        self.action_parameter_right_click_menu_delete.setEnabled(self.Parameter_list.rowCount()>=1)
        action = self.popMenu_parameter.exec_(self.Parameter_Widget.mapToGlobal(point))
        if action == self.action_parameter_right_click_menu_add:
            rowPosition = self.Parameter_list.rowCount()
            self.Parameter_list.insertRow(rowPosition)
            name_set = QTableWidgetItem("n0")
            for i in range(rowPosition-1):
                if not 'n'+str(i) == self.Parameter_list.item(i, 0).text():
                    name_set = QTableWidgetItem("n"+str(i))
                    break
            name_set.setFlags(Qt.ItemIsEnabled)
            digit_set = QTableWidgetItem("0.0")
            digit_set.setFlags(Qt.ItemIsEnabled)
            commit_set = QTableWidgetItem("No commit yet.")
            commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.Parameter_list.setItem(rowPosition, 0, name_set)
            self.Parameter_list.setItem(rowPosition, 1, digit_set)
            self.Parameter_list.setItem(rowPosition, 2, commit_set)
            self.Workbook_noSave()
            self.Mask_Change()
            self.Resolve()
        elif action == self.action_parameter_right_click_menu_move_up:
            table = self.Parameter_list
            row = self.Parameter_list.currentRow()
            try:
                print(row)
                table.insertRow(row-1)
                for i in range(2):
                    name_set = QTableWidgetItem(table.item(row+1, i).text())
                    name_set.setFlags(Qt.ItemIsEnabled)
                    table.setItem(row-1, i, name_set)
                commit_set = QTableWidgetItem(table.item(row+1, 2).text())
                commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                table.setItem(row-1, 2, commit_set)
                table.removeRow(row+1)
                self.Workbook_noSave()
                self.Mask_Change()
                self.Resolve()
            except: pass
        elif action == self.action_parameter_right_click_menu_move_down:
            try:
                table.insertRow(row+2)
                for i in range(2):
                    name_set = QTableWidgetItem(table.item(row+2, i).text())
                    name_set.setFlags(Qt.ItemIsEnabled)
                    table.setItem(row+2, i, name_set)
                commit_set = QTableWidgetItem(table.item(row+2, 2).text())
                commit_set.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                table.removeRow(row)
                self.Workbook_noSave()
            except: pass
        elif action == self.action_parameter_right_click_menu_delete:
            self.Parameter_list.removeRow(self.Parameter_list.currentRow())
            self.Workbook_noSave()
            self.Mask_Change()
    
    #Table move up & down
    def move_up(self, table, row, name):
        try:
            table.insertRow(row-1)
            for i in range(table.columnCount()): table.setItem(row-1, i, QTableWidgetItem(table.item(row+1, i).text()))
            table.removeRow(row+1)
            for j in range(table.rowCount()):
                name_set = QTableWidgetItem(name+str(j))
                name_set.setFlags(Qt.ItemIsEnabled)
                table.setItem(j, 0, name_set)
            self.Workbook_noSave()
        except: pass
    def move_down(self, table, row, name):
        try:
            table.insertRow(row+2)
            for i in range(table.columnCount()): table.setItem(row+2, i, QTableWidgetItem(table.item(row, i).text()))
            table.removeRow(row)
            for j in range(table.rowCount()):
                name_set = QTableWidgetItem(name+str(j))
                name_set.setFlags(Qt.ItemIsEnabled)
                table.setItem(j, 0, QTableWidgetItem(name+str(j)))
            self.Workbook_noSave()
        except: pass
    
    #Close Event
    def closeEvent(self, event):
        if self.Workbook_Change:
            reply = QMessageBox.question(self, 'Saving Message',
                "Are you sure to quit?\nAny Changes won't be saved.",
                (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel), QMessageBox.Save)
            if reply == QMessageBox.Discard or reply == QMessageBox.Ok:
                print("Exit.")
                event.accept()
            elif reply == QMessageBox.Save:
                self.on_action_Output_Coordinate_to_Text_File_triggered()
                if not self.Workbook_Change:
                    print("Exit.")
                    event.accept()
                else: event.ignore()
            else: event.ignore()
        else: event.accept()
    
    #Scripts
    @pyqtSlot()
    def on_action_See_Python_Scripts_triggered(self):
        dlg = Script_Dialog()
        dlg.script.setPlainText(self.Script)
        dlg.show()
        dlg.exec()
    
    #Resolve
    def Resolve(self):
        table_point = self.Entiteis_Point
        table_line = self.Entiteis_Link
        table_chain = self.Entiteis_Stay_Chain
        table_shaft = self.Drive_Shaft
        table_slider = self.Slider
        table_rod = self.Rod
        for i in range(table_line.rowCount()):
            a = int(table_line.item(i, 1).text().replace("Point", ""))
            b = int(table_line.item(i, 2).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            if case1 and case2:
                if b == 0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
        for i in range(table_chain.rowCount()):
            a = int(table_chain.item(i, 1).text().replace("Point", ""))
            b = int(table_chain.item(i, 2).text().replace("Point", ""))
            c = int(table_chain.item(i, 3).text().replace("Point", ""))
            case1 = float(table_point.item(a, 1).text())==float(table_point.item(b, 1).text())
            case2 = float(table_point.item(a, 2).text())==float(table_point.item(b, 2).text())
            case3 = float(table_point.item(b, 1).text())==float(table_point.item(c, 1).text())
            case4 = float(table_point.item(b, 2).text())==float(table_point.item(c, 2).text())
            case5 = float(table_point.item(a, 1).text())==float(table_point.item(c, 1).text())
            case6 = float(table_point.item(a, 2).text())==float(table_point.item(c, 2).text())
            if case1 and case2:
                if b==0: table_point.setItem(a, 1, QTableWidgetItem(str(float(table_point.item(a, 1).text())+0.01)))
                else: table_point.setItem(b, 1, QTableWidgetItem(str(float(table_point.item(b, 1).text())+0.01)))
            if case3 and case4:
                if c==0: table_point.setItem(b, 2, QTableWidgetItem(str(float(table_point.item(b, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
            if case5 and case6:
                if c==0: table_point.setItem(a, 2, QTableWidgetItem(str(float(table_point.item(a, 2).text())+0.01)))
                else: table_point.setItem(c, 2, QTableWidgetItem(str(float(table_point.item(c, 2).text())+0.01)))
        #Solve
        result = []
        solvespace = Solvespace()
        fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "").split("/")[-1].split(".")[0]
        result = solvespace.static_process(table_point, table_line, table_chain,
            table_shaft, table_slider, table_rod, fileName, self.Parameter_list)
        self.Script = solvespace.Script
        if result==[]:
            print("Rebuild the cavanc falled.")
            dlg = resolution_fail_show()
            dlg.show()
            dlg.exec()
        else:
            for i in range(table_point.rowCount()):
                Point_setup(table_point, i, result[i*2], result[i*2+1])
            self.Reload_Canvas()
    
    #Reload Canvas
    def Reload_Canvas(self):
        self.qpainterWindow.update_figure(float(self.LineWidth.text()), float(self.PathWidth.text()),
            self.Entiteis_Point, self.Entiteis_Link,
            self.Entiteis_Stay_Chain, self.Drive_Shaft,
            self.Slider, self.Rod, self.Parameter_list,
            self.Entiteis_Point_Style, self.ZoomText.toPlainText(),
            self.Font_size.value(),
            self.actionDisplay_Dimensions.isChecked(), self.actionDisplay_Point_Mark.isChecked(),
            self.action_Black_Blackground.isChecked())
    
    #Workbook Change
    def Workbook_noSave(self):
        self.Workbook_Change = True
        self.setWindowTitle(_translate("MainWindow", self.windowTitle().replace("*", "")+"*"))
    
    @pyqtSlot()
    def on_action_Full_Screen_triggered(self): print("Full Screen.")
    @pyqtSlot()
    def on_actionNormalmized_triggered(self): print("Normal Screen.")
    
    @pyqtSlot()
    def on_actionHow_to_use_triggered(self):
        dlg = Help_info_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_actionColor_Settings_triggered(self):
        dlg = color_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_action_Get_Help_triggered(self):
        print("Open http://project.mde.tw/blog/slvs-library-functions.html")
        webbrowser.open("http://project.mde.tw/blog/slvs-library-functions.html")
    @pyqtSlot()
    def on_actionGit_hub_Site_triggered(self):
        print("Open https://github.com/40323230/python-solvespace")
        webbrowser.open("https://github.com/40323230/python-solvespace")
    @pyqtSlot()
    def on_actionGithub_Wiki_triggered(self):
        print("Open https://github.com/40323230/python-solvespace/wiki")
        webbrowser.open("https://github.com/40323230/python-solvespace/wiki")
    @pyqtSlot()
    def on_action_About_Pyslvs_triggered(self):
        dlg = version_show()
        dlg.show()
        dlg.exec()
    @pyqtSlot()
    def on_action_About_Python_Solvspace_triggered(self):
        dlg = Info_show()
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_action_New_Workbook_triggered(self):
        if self.Workbook_Change:
            dlg  = reset_show()
            dlg.show()
            if dlg.exec_(): self.new_Workbook()
        else: self.new_Workbook()
    
    @pyqtSlot()
    def on_action_Load_Workbook_triggered(self):
        if self.Workbook_Change:
            warning_reset  = reset_show()
            warning_reset.show()
            if warning_reset.exec_(): self.load_Workbook()
        else: self.load_Workbook()
    
    def new_Workbook(self):
        try:
            self.MeasurementWidget.deleteLater()
            del self.MeasurementWidget
            self.Measurement.setChecked(False)
        except: pass
        try:
            self.DriveWidget.deleteLater()
            del self.DriveWidget
            self.Drive.setChecked(False)
        except: pass
        Reset_notebook(self.Entiteis_Point, 1)
        Reset_notebook(self.Entiteis_Link, 0)
        Reset_notebook(self.Entiteis_Stay_Chain, 0)
        Reset_notebook(self.Entiteis_Point_Style, 1)
        Reset_notebook(self.Drive_Shaft, 0)
        Reset_notebook(self.Slider, 0)
        Reset_notebook(self.Rod, 0)
        Reset_notebook(self.Parameter_list, 0)
        self.qpainterWindow.removePath()
        self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
        self.Resolve()
        print("Reset the workbook.")
        self.setWindowTitle(_translate("MainWindow", "Pyslvs - New Workbook"))
    def load_Workbook(self):
        try:
            self.MeasurementWidget.deleteLater()
            del self.MeasurementWidget
            self.Measurement.setChecked(False)
        except: pass
        try:
            self.DriveWidget.deleteLater()
            del self.DriveWidget
            self.Drive.setChecked(False)
        except: pass
        Reset_notebook(self.Entiteis_Point, 1)
        Reset_notebook(self.Entiteis_Link, 0)
        Reset_notebook(self.Entiteis_Stay_Chain, 0)
        Reset_notebook(self.Entiteis_Point_Style, 1)
        Reset_notebook(self.Drive_Shaft, 0)
        Reset_notebook(self.Slider, 0)
        Reset_notebook(self.Rod, 0)
        Reset_notebook(self.Parameter_list, 0)
        self.qpainterWindow.removePath()
        self.Resolve()
        print("Reset workbook.")
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open file...', Environment_variables, 'CSV File(*.csv);;Text File(*.txt)')
        if fileName:
            print("Get:"+fileName)
            data = []
            with open(fileName, newline="") as stream:
                reader = csv.reader(stream, delimiter=' ', quotechar='|')
                for row in reader: data += ', '.join(row).split('\t,')
            bookmark = 0
            for i in range(4, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                fixed = data[i+3]=="Fixed"
                Points_list(self.Entiteis_Point, data[i], data[i+1], data[i+2], fixed, False)
            self.Entiteis_Point_Style.removeRow(0)
            for i in range(bookmark+1, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Points_style_add(self.Entiteis_Point_Style, data[i], data[i+1], data[i+2], data[i+3])
            for i in range(bookmark+1, len(data), 4):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Links_list(self.Entiteis_Link, data[i], data[i+1], data[i+2], data[i+3], False)
            for i in range(bookmark+1, len(data), 7):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Chain_list(self.Entiteis_Stay_Chain, data[i], data[i+1], data[i+2], data[i+3], data[i+4], data[i+5], data[i+6], False)
            for i in range(bookmark+1, len(data), 6):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Shaft_list(self.Drive_Shaft, data[i], data[i+1], data[i+2], data[i+3], data[i+4], data[i+5], False)
            for i in range(bookmark+1, len(data), 3):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Slider_list(self.Slider, data[i], data[i+1], data[i+2], False)
            for i in range(bookmark+1, len(data), 5):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Rod_list(self.Parameter_list, data[i], data[i+1], data[i+2], data[i+3], data[i+4], False)
            for i in range(bookmark+1, len(data), 3):
                bookmark = i
                if data[i] == 'Next_table\t': break
                Parameter_management(self.Parameter_list, data[i], data[i+1], data[i+2], False)
            self.Workbook_Change = False
            self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
            self.Resolve()
            self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
            self.Path_Clear.setEnabled(False)
            self.Path_coordinate.setEnabled(False)
            print("Successful Load the workbook...")
    
    @pyqtSlot()
    def on_action_Output_Coordinate_to_Text_File_triggered(self):
        print("Saving to CSV or text File...")
        if self.windowTitle()=="Pyslvs - New Workbook" or self.windowTitle()=="Pyslvs - New Workbook*":
            fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Spreadsheet(*.csv)')
        else:
            fileName = self.windowTitle().replace("Pyslvs - ", "").replace("*", "")
        if fileName:
            fileName = fileName.replace(".csv", "")+".csv"
            with open(fileName, 'w', newline="") as stream:
                table = self.Entiteis_Point
                writer = csv.writer(stream)
                for row in range(table.rowCount()):
                    rowdata = []
                    for column in range(table.columnCount()-1):
                        item = table.item(row, column)
                        if item is not None:
                            if (item.checkState()==False) and (item.text()==''): rowdata += ["noFixedFixed"]
                            else:
                                if item.text()=='': rowdata += ["Fixed"]
                                else: rowdata += [item.text()+'\t']
                    writer.writerow(rowdata)
                CSV_notebook(writer, self.Entiteis_Point_Style, 4)
                CSV_notebook(writer, self.Entiteis_Link, 4)
                CSV_notebook(writer, self.Entiteis_Stay_Chain, 7)
                CSV_notebook(writer, self.Drive_Shaft, 6)
                CSV_notebook(writer, self.Slider, 3)
                CSV_notebook(writer, self.Rod, 5)
                CSV_notebook(writer, self.Parameter_list, 3)
            print("Successful Save: "+fileName)
            self.Workbook_Change = False
            self.setWindowTitle(_translate("MainWindow", "Pyslvs - "+fileName))
    
    @pyqtSlot()
    def on_action_Output_to_S_QLite_Data_Base_triggered(self):
        print("Saving to Data Base...")
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Data Base(*.db)')
        if fileName:
            fileName = fileName.replace(".db", "")
            fileName += ".db"
            #TODO: SQLite
    
    @pyqtSlot()
    def on_action_Output_to_Script_triggered(self):
        print("Saving to script...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'Python Script(*.py)')
        if fileName:
            fileName = fileName.replace(".py", "")
            if sub == "Python Script(*.py)": fileName += ".py"
            with open(fileName, 'w', newline="") as f:
                f.write(self.Script)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_action_Output_to_Picture_triggered(self):
        print("Saving to picture...")
        fileName, sub = QFileDialog.getSaveFileName(self, 'Save file...', Environment_variables, 'PNG file(*.png)')
        if fileName:
            fileName = fileName.replace(".png", "")
            fileName += ".png"
            pixmap = self.qpainterWindow.grab()
            pixmap.save(fileName)
            print("Saved to:"+str(fileName))
    
    @pyqtSlot()
    def on_action_New_Point_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        dlg  = New_point()
        dlg.Point_num.insertPlainText("Point"+str(table1.rowCount()))
        dlg.show()
        if dlg.exec_():
            x = self.X_coordinate.text() if not self.X_coordinate.text()in["", "n", "-"] else self.X_coordinate.placeholderText()
            y = self.Y_coordinate.text() if not self.Y_coordinate.text()in["", "n", "-"] else self.Y_coordinate.placeholderText()
            Points_list(table1, dlg.Point_num.toPlainText(),
                x, y, dlg.Fix_Point.checkState(), False)
            fix = "10" if dlg.Fix_Point.checkState() else "5"
            Points_style_add(table2, dlg.Point_num.toPlainText(), "G", fix, "G")
            self.Resolve()
            self.Workbook_noSave()
    
    @pyqtSlot()
    def on_Point_add_button_clicked(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Point_Style
        x = self.X_coordinate.text() if not self.X_coordinate.text()in["", "n", "-"] else self.X_coordinate.placeholderText()
        y = self.Y_coordinate.text() if not self.Y_coordinate.text()in["", "n", "-"] else self.Y_coordinate.placeholderText()
        Points_list(table1, "Point"+str(table1.rowCount()), x, y, False, False)
        Points_style_add(table2, "Point"+str(table2.rowCount()), "G", "5", "G")
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Point_triggered(self, pos = 1):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg  = edit_point_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(1, table1.rowCount()): dlg.Point.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Another_point.connect(self.Change_Edit_Point)
            self.point_feedback.connect(dlg.change_feedback)
            dlg.Point.setCurrentIndex(pos-1)
            self.Change_Edit_Point(pos)
            dlg.show()
            if dlg.exec_():
                table2 = self.Entiteis_Point_Style
                Points_list(table1, dlg.Point.currentText(),
                    dlg.X_coordinate.text() if not dlg.X_coordinate.text()in["", "n", "-"] else dlg.X_coordinate.placeholderText(),
                    dlg.Y_coordinate.text() if not dlg.Y_coordinate.text()in["", "n", "-"] else dlg.Y_coordinate.placeholderText(),
                    dlg.Fix_Point.checkState(), True)
                Points_style_fix(table2, dlg.Point.currentText(), dlg.Fix_Point.checkState())
                self.Resolve()
                self.Workbook_noSave()
    point_feedback = pyqtSignal(float, float, bool)
    @pyqtSlot(int)
    def Change_Edit_Point(self, pos):
        table = self.Entiteis_Point
        x = float(table.item(pos, 1).text())
        y = float(table.item(pos, 2).text())
        fix = table.item(pos, 3).checkState()
        self.point_feedback.emit(x, y, fix)
    
    @pyqtSlot()
    def on_action_New_Line_triggered(self):
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            dlg  = New_link()
            for i in range(table1.rowCount()):
                dlg.Start_Point.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End_Point.insertItem(i, icon, table1.item(i, 0).text())
            table2 = self.Entiteis_Link
            dlg.Link_num.insertPlainText("Line"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Start_Point.currentText()
                b = dlg.End_Point.currentText()
                if Repeated_check_line(table2, a, b): self.on_action_New_Line_triggered()
                elif a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Line_triggered()
                else:
                    Links_list(table2, dlg.Link_num.toPlainText(),
                        dlg.Start_Point.currentText(), dlg.End_Point.currentText(),
                        dlg.Length.text()if not dlg.Length.text()in["", "n"] else dlg.Length.placeholderText(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Linkage_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            dlg  = edit_link_show()
            for i in range(table1.rowCount()):
                dlg.Start_Point.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.End_Point.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Link.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_line.connect(self.Change_Edit_Line)
            self.link_feedback.connect(dlg.change_feedback)
            dlg.Link.setCurrentIndex(pos)
            self.Change_Edit_Line(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Start_Point.currentText()
                b = dlg.End_Point.currentText()
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Linkage_triggered()
                else:
                    Links_list(table2, dlg.Link.currentText(),
                        dlg.Start_Point.currentText(),  dlg.End_Point.currentText(),
                        dlg.Length.text() if not dlg.Length.text()in["", "n"] else dlg.Length.placeholderText(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    link_feedback = pyqtSignal(int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Line(self, pos):
        table = self.Entiteis_Link
        start = int(table.item(pos, 1).text().replace("Point", ""))
        end = int(table.item(pos, 2).text().replace("Point", ""))
        len = float(table.item(pos, 3).text())
        self.link_feedback.emit(start, end, len)
    
    @pyqtSlot()
    def on_action_New_Stay_Chain_triggered(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        if (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = chain_show()
            table2 = self.Entiteis_Stay_Chain
            for i in range(table1.rowCount()):
                dlg.Point1.insertItem(i, icon, table1.item(i, 0).text())
                dlg.Point2.insertItem(i, icon, table1.item(i, 0).text())
                dlg.Point3.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Chain_num.insertPlainText("Chain"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                p1 = dlg.Point1.currentText()
                p2 = dlg.Point2.currentText()
                p3 = dlg.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_New_Stay_Chain_triggered()
                else:
                    Chain_list(table2, dlg.Chain_num.toPlainText(),
                        p1, p2, p3,
                        dlg.p1_p2.text() if not dlg.p1_p2.text()in["", "n"] else dlg.p1_p2.placeholderText(),
                        dlg.p2_p3.text() if not dlg.p2_p3.text()in["", "n"] else dlg.p2_p3.placeholderText(),
                        dlg.p1_p3.text() if not dlg.p1_p3.text()in["", "n"] else dlg.p1_p3.placeholderText(), False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionEdit_Stay_Chain_triggered(self, pos = 0):
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Stay_Chain
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_stay_chain_show()
            for i in range(table1.rowCount()):
                dlg.Point1.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.Point2.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.Point3.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Chain.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_chain.connect(self.Change_Edit_Chain)
            self.chain_feedback.connect(dlg.change_feedback)
            dlg.Chain.setCurrentIndex(pos)
            self.Change_Edit_Chain(pos)
            dlg.show()
            if dlg.exec_():
                p1 = dlg.Point1.currentText()
                p2 = dlg.Point2.currentText()
                p3 = dlg.Point3.currentText()
                if (p1 == p2) | (p2 == p3) | (p1 == p3):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_actionEdit_Stay_Chain_triggered()
                else:
                    Chain_list(table2, dlg.Chain.currentText(), p1, p2, p3,
                        dlg.p1_p2.text() if not dlg.p1_p2.text()in["", "n"] else dlg.p1_p2.placeholderText(),
                        dlg.p2_p3.text() if not dlg.p2_p3.text()in["", "n"] else dlg.p2_p3.placeholderText(),
                        dlg.p1_p3.text() if not dlg.p1_p3.text()in["", "n"] else dlg.p1_p3.placeholderText(), True)
                    self.Resolve()
                    self.Workbook_noSave()
    chain_feedback = pyqtSignal(int, int, int, float, float, float)
    @pyqtSlot(int)
    def Change_Edit_Chain(self, pos):
        table = self.Entiteis_Stay_Chain
        Point1 = int(table.item(pos, 1).text().replace("Point", ""))
        Point2 = int(table.item(pos, 2).text().replace("Point", ""))
        Point3 = int(table.item(pos, 3).text().replace("Point", ""))
        p1_p2 = float(table.item(pos, 4).text())
        p2_p3 = float(table.item(pos, 5).text())
        p1_p3 = float(table.item(pos, 6).text())
        self.chain_feedback.emit(Point1, Point2, Point3, p1_p2, p2_p3, p1_p3)
    
    @pyqtSlot()
    def on_action_Set_Drive_Shaft_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = shaft_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Shaft_num.insertPlainText("Shaft"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if dlg.Demo_angle_enable.checkState(): e = dlg.Demo_angle.text()
                else: e = None
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Shaft_list(table2, dlg.Shaft_num.toPlainText(), a, b, c, d, e, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Drive_Shaft_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Drive_Shaft
        if (table2.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_shaft_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Shaft_Center.insertItem(i, icon1, table1.item(i, 0).text())
                dlg.References.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Shaft.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Another_shaft.connect(self.Change_Edit_Shaft)
            self.shaft_feedback.connect(dlg.change_feedback)
            dlg.Shaft.setCurrentIndex(pos)
            self.Change_Edit_Shaft(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Shaft_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.Start_Angle.text()
                d = dlg.End_Angle.text()
                if (a == b) or (c == d):
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Shaft_list(table2, dlg.Shaft.currentText(), a, b, c, d, table2.item(dlg.Shaft.currentIndex(), 5), True)
                    self.Resolve()
                    self.Workbook_noSave()
    shaft_feedback = pyqtSignal(int, int, float, float)
    @pyqtSlot(int)
    def Change_Edit_Shaft(self, pos):
        table = self.Drive_Shaft
        center = int(table.item(pos, 1).text().replace("Point", ""))
        references = int(table.item(pos, 2).text().replace("Point", ""))
        start = float(table.item(pos, 3).text().replace("°", ""))
        end = float(table.item(pos, 4).text().replace("°", ""))
        self.shaft_feedback.emit(center, references, start, end)
    
    @pyqtSlot()
    def on_action_Set_Slider_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table2.rowCount() <= 0) and (table1.rowCount() <= 2):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            dlg.Slider_num.insertPlainText("Slider"+str(table3.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Slider_triggered()
                else:
                    Slider_list(table3, dlg.Slider_num.toPlainText(), a, b, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Slider_triggered(self, pos):
        table1 = self.Entiteis_Point
        table2 = self.Entiteis_Link
        table3 = self.Slider
        if (table3.rowCount() <= 0):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_slider_show()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
            icon3 = QIcon()
            icon3.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()): dlg.Slider_Center.insertItem(i, icon1, table1.item(i, 0).text())
            for i in range(table2.rowCount()): dlg.References.insertItem(i, icon2, table2.item(i, 0).text())
            for i in range(table3.rowCount()): dlg.Slider.insertItem(i, icon3, table3.item(i, 0).text())
            dlg.Another_slider.connect(self.Change_Edit_Slider)
            self.slider_feedback.connect(dlg.change_feedback)
            dlg.Slider.setCurrentIndex(pos)
            self.Change_Edit_Slider(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Slider_Center.currentText()
                b = dlg.References.currentText()
                c = dlg.References.currentIndex()
                if (table2.item(c, 1).text()==a) or (table2.item(c, 2).text()==a):
                    dlg = restriction_conflict_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Edit_Slider_triggered()
                else:
                    Slider_list(table3, dlg.Slider.currentText(), a, b, True)
                    self.Resolve()
                    self.Workbook_noSave()
    slider_feedback = pyqtSignal(int, int)
    @pyqtSlot(int)
    def Change_Edit_Slider(self, pos):
        table = self.Slider
        point = int(table.item(pos, 1).text().replace("Ponit", ""))
        line = int(table.item(pos, 2).text().replace("Line", ""))
        self.slider_feedback.emit(point, line)
    
    @pyqtSlot()
    def on_action_Set_Rod_triggered(self):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Rod_num.insertPlainText("Rod"+str(table2.rowCount()))
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Rod_list(table2, dlg.Rod_num.toPlainText(), a, b, c, d, False)
                    self.Resolve()
                    self.Workbook_noSave()
    
    @pyqtSlot()
    def on_action_Edit_Piston_Spring_triggered(self, pos = 0):
        table1 = self.Entiteis_Point
        table2 = self.Rod
        if (table1.rowCount() <= 1):
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = edit_rod_show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            for i in range(table1.rowCount()):
                dlg.Start.insertItem(i, icon, table1.item(i, 0).text())
                dlg.End.insertItem(i, icon, table1.item(i, 0).text())
            for i in range(table2.rowCount()):
                dlg.Rod.insertItem(i, icon, table2.item(i, 0).text())
            dlg.Another_rod.connect(self.Change_Edit_Rod)
            self.rod_feedback.connect(dlg.change_feedback)
            dlg.Rod.setCurrentIndex(pos)
            self.Change_Edit_Rod(pos)
            dlg.show()
            if dlg.exec_():
                a = dlg.Start.currentText()
                b = dlg.End.currentText()
                c = str(min(float(dlg.len1.text()), float(dlg.len2.text())))
                d = str(max(float(dlg.len1.text()), float(dlg.len2.text())))
                if a == b:
                    dlg = same_show()
                    dlg.show()
                    if dlg.exec_(): self.on_action_Set_Drive_Shaft_triggered()
                else:
                    Rod_list(table2, dlg.Rod.currentText(), a, b, c, d, True)
                    self.Resolve()
                    self.Workbook_noSave()
    rod_feedback = pyqtSignal(int, int, int, float)
    @pyqtSlot(int)
    def Change_Edit_Rod(self, pos):
        table = self.Rod
        center = int(table.item(pos, 1).text().replace("Point", ""))
        start = int(table.item(pos, 2).text().replace("Point", ""))
        end = int(table.item(pos, 3).text().replace("Point", ""))
        position = float(table.item(pos, 4).text())
        self.rod_feedback.emit(center, start, end, position)
    
    @pyqtSlot()
    def on_actionDelete_Point_triggered(self, pos = 1):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
        table = self.Entiteis_Point
        if table.rowCount() <= 1:
            dlg = kill_origin_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_point_show()
            for i in range(1, table.rowCount()):
                dlg.Entity.insertItem(i, icon, table.item(i, 0).text())
            dlg.Entity.setCurrentIndex(pos)
            dlg.show()
            if dlg.exec_():
                Point_list_delete(table,
                    self.Entiteis_Point_Style, self.Entiteis_Link,
                    self.Entiteis_Stay_Chain, self.Drive_Shaft,
                    self.Slider, self.Rod, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Linkage_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/line.png"), QIcon.Normal, QIcon.Off)
        table1 = self.Entiteis_Link
        table2 = self.Slider
        if table1.rowCount() <= 0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg = delete_linkage_show()
            for i in range(table1.rowCount()):
                dlg.Entity.insertItem(i, icon, table1.item(i, 0).text())
            dlg.Entity.setCurrentIndex(pos)
            dlg.show()
            if dlg.exec_():
                Link_list_delete(table1, table2, dlg)
                self.Resolve()
                self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Stay_Chain_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/equal.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Entiteis_Stay_Chain, icon, delete_chain_show(), "Chain", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Drive_Shaft_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Drive_Shaft, icon, delete_shaft_show(), "Shaft", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Slider_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/pointonx.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Slider, icon, delete_slider_show(), "Slider", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot()
    def on_actionDelete_Piston_Spring_triggered(self, pos = 0):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/spring.png"), QIcon.Normal, QIcon.Off)
        Delete_dlg_set(self.Rod, icon, delete_rod_show(), "Rod", pos)
        self.Resolve()
        self.Workbook_noSave()
    
    @pyqtSlot(int)
    def on_ZoomBar_valueChanged(self, value):
        self.ZoomText.setPlainText(str(value)+"%")
        self.Reload_Canvas()
    
    def wheelEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            if event.angleDelta().y()>0: self.ZoomBar.setValue(self.ZoomBar.value()+10)
            if event.angleDelta().y()<0: self.ZoomBar.setValue(self.ZoomBar.value()-10)
    
    @pyqtSlot()
    def on_actionReload_Drawing_triggered(self): self.Resolve()
    
    @pyqtSlot(QTableWidgetItem)
    def on_Entiteis_Point_Style_itemChanged(self, item):
        self.Reload_Canvas()
        self.Workbook_noSave()
    @pyqtSlot(int)
    def on_LineWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(int)
    def on_PathWidth_valueChanged(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Dimensions_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_actionDisplay_Point_Mark_toggled(self, p0): self.Reload_Canvas()
    @pyqtSlot(bool)
    def on_action_Black_Blackground_toggled(self, p0): self.Reload_Canvas()
    
    @pyqtSlot()
    def on_PathTrack_clicked(self):
        table1 = self.Entiteis_Point
        dlg = Path_Track_show()
        self.actionDisplay_Point_Mark.setChecked(True)
        for i in range(table1.rowCount()):
            if not table1.item(i, 3).checkState(): dlg.Point_list.addItem(table1.item(i, 0).text())
        if dlg.Point_list.count()==0:
            dlg = zero_show()
            dlg.show()
            dlg.exec()
        else:
            dlg.Entiteis_Point = self.Entiteis_Point
            dlg.Entiteis_Link = self.Entiteis_Link
            dlg.Entiteis_Stay_Chain = self.Entiteis_Stay_Chain
            dlg.Drive_Shaft = self.Drive_Shaft
            dlg.Slider = self.Slider
            dlg.Rod = self.Rod
            dlg.Parameter_list = self.Parameter_list
            dlg.show()
            if dlg.exec_():
                self.Path_Run_list = []
                for i in range(dlg.Run_list.count()): self.Path_Run_list += [dlg.Run_list.item(i).text()]
                self.Path_data = dlg.Path_data
                self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">Path Data Exist</span></p></body></html>"))
                self.Path_Clear.setEnabled(True)
                self.Path_coordinate.setEnabled(True)
                self.qpainterWindow.path_track(dlg.Path_data)
    @pyqtSlot()
    def on_Path_Clear_clicked(self):
        self.qpainterWindow.removePath()
        self.Reload_Canvas()
        self.Path_data_exist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ff0000;\">No Path Data</span></p></body></html>"))
        self.Path_Clear.setEnabled(False)
        self.Path_coordinate.setEnabled(False)
    @pyqtSlot()
    def on_Path_coordinate_clicked(self):
        dlg = path_point_data_show()
        Path_point_setup(dlg.path_data, self.Path_data, self.Path_Run_list)
        dlg.show()
        dlg.exec()
    
    @pyqtSlot()
    def on_Drive_clicked(self):
        if self.mplLayout.count()<=3 and not hasattr(self, 'DriveWidget'):
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/circle.png"), QIcon.Normal, QIcon.Off)
            self.DriveWidget = Drive_show()
            for i in range(self.Drive_Shaft.rowCount()): self.DriveWidget.Shaft.insertItem(i, icon, self.Drive_Shaft.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.DriveWidget)
            self.DriveWidget.Degree_change.connect(self.Change_demo_angle)
            self.DriveWidget.Shaft_change.connect(self.Shaft_limit)
            self.Shaft_limit(0)
        else:
            try:
                self.DriveWidget.deleteLater()
                del self.DriveWidget
            except: pass
    @pyqtSlot(int)
    def Shaft_limit(self, pos):
        try:
            self.DriveWidget.Degree.setMinimum(int(float(self.Drive_Shaft.item(pos, 3).text().replace("°", "")))*100)
            self.DriveWidget.Degree.setMaximum(int(float(self.Drive_Shaft.item(pos, 4).text().replace("°", "")))*100)
            self.DriveWidget.Degree.setValue(int(float(self.Drive_Shaft.item(pos, 5).text().replace("°", "")))*100)
        except: self.DriveWidget.Degree.setValue(int((self.DriveWidget.Degree.maximum()+self.DriveWidget.Degree.minimum())/2))
        self.DriveWidget.Degree_text.setPlainText(str(float(self.DriveWidget.Degree.value()/100))+"°")
    @pyqtSlot(int, float)
    def Change_demo_angle(self, shaft_int, angle):
        self.Drive_Shaft.setItem(shaft_int, 5, QTableWidgetItem(str(angle)+"°"))
        self.Resolve()
    
    @pyqtSlot()
    def on_Measurement_clicked(self):
        if self.mplLayout.count()<=3 and not hasattr(self, 'MeasurementWidget'):
            table = self.Entiteis_Point
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/point.png"), QIcon.Normal, QIcon.Off)
            self.MeasurementWidget = Measurement_show()
            for i in range(table.rowCount()):
                self.MeasurementWidget.Start.insertItem(i, icon, table.item(i, 0).text())
                self.MeasurementWidget.End.insertItem(i, icon, table.item(i, 0).text())
            self.mplLayout.insertWidget(1, self.MeasurementWidget)
            self.qpainterWindow.change_event.connect(self.MeasurementWidget.Detection_do)
            self.actionDisplay_Dimensions.setChecked(True)
            self.actionDisplay_Point_Mark.setChecked(True)
            self.qpainterWindow.mouse_track.connect(self.MeasurementWidget.show_mouse_track)
            self.MeasurementWidget.point_change.connect(self.distance_solving)
            self.distance_changed.connect(self.MeasurementWidget.change_distance)
            self.MeasurementWidget.Mouse.setPlainText("Detecting")
        else:
            try:
                self.MeasurementWidget.deleteLater()
                del self.MeasurementWidget
            except: pass
    distance_changed = pyqtSignal(float)
    @pyqtSlot(int, int)
    def distance_solving(self, start, end):
        start = self.Entiteis_Point.item(start, 4).text().replace("(", "").replace(")", "")
        end = self.Entiteis_Point.item(end, 4).text().replace("(", "").replace(")", "")
        x = float(start.split(", ")[0])-float(end.split(", ")[0])
        y = float(start.split(", ")[1])-float(end.split(", ")[1])
        self.distance_changed.emit(round(math.sqrt(x**2+y**2), 9))
    
    def Mask_Change(self):
        param_10 = '[1-'+str(int(self.Parameter_list.rowCount()/10))+']?' if self.Parameter_list.rowCount()>=10 else ''
        param_use = '(^[n]'+param_10+'[0-'+str(int(self.Parameter_list.rowCount())-1)+']$|' if self.Parameter_list.rowCount()>=1 else ''
        mask = param_use+'^[-]?([1-9][0-9]{1,2})?[0-9][.][0-9]{1,4}$'
        if param_use: mask += ')'
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
    
    @pyqtSlot()
    def on_Parameter_update_clicked(self):
        try: self.Parameter_list.setItem(self.Parameter_list.currentRow(), 1, QTableWidgetItem(self.Parameter_digital.text() if self.Parameter_digital.text() else Parameter_digital.placeholderText()))
        except: pass

def CSV_notebook(writer, table, k):
    writer.writerow(["Next_table\t"])
    for row in range(table.rowCount()):
        rowdata = []
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is not None:
                if column==k-1: rowdata += [item.text()]
                else: rowdata += [item.text()+'\t']
        writer.writerow(rowdata)
