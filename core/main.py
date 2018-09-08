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

from typing import Tuple
from core.QtModules import (
    pyqtSlot,
    QMessageBox,
    QInputDialog,
    QTextCursor,
    QListWidgetItem,
)
from core.info import ARGUMENTS
from core.io import XStream, strbetween, QTIMAGES
from core.main_method import IOMethodInterface


class MainWindow(IOMethodInterface):
    
    """The main window of Pyslvs.
    
    Inherited from QMainWindow.
    Exit with QApplication.
    
    The main window is so much method that was been split it
    to wrapper function in 'main_method' module.
    """
    
    def __init__(self):
        """Notes:
        
        + Input command line arguments object from Python parser.
        + Command line arguments excluding any Qt startup option.
        + Start main window with no parent.
        """
        super(MainWindow, self).__init__()
        
        self.autopreview = []
        self.restoreSettings()
        
        # Console widget.
        self.consoleerror_option.setChecked(ARGUMENTS.debug_mode)
        if not ARGUMENTS.debug_mode:
            self.__consoleConnect()
        
        # Start first solve function calling.
        self.solve()
        
        # Load workbook from argument.
        self.readFromArgs()
    
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
    
    @pyqtSlot(int, name='on_ZoomBar_valueChanged')
    def setZoom(self, value: int):
        """Reset the text when zoom bar changed."""
        self.zoom_button.setText(f'{value}%')
    
    @pyqtSlot()
    def customizeZoom(self):
        """Customize zoom value."""
        value, ok = QInputDialog.getInt(
            self,
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
        # exp_symbol = ['A', 'B', 'C', 'D', 'E']
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
            self.addNormalLink(tuple(
                tmp_dict[name] for name in strbetween(exp, '[', ']').split(',')
            ))
            if i == 0:
                self.constrainLink(self.EntitiesLink.rowCount() - 1)
        self.CommandStack.endMacro()
        # Add the path.
        i = 0
        while f"Algorithm_{i}" in self.InputsWidget.pathData():
            i += 1
        self.InputsWidget.addPath(f"Algorithm_{i}", path)
        self.MainCanvas.zoomToFit()
    
    @pyqtSlot(int, name='on_EntitiesTab_currentChanged')
    def __setSelectionMode(self, index: int):
        """Connect selection signal for main canvas."""
        # Set selection from click table items.
        tables = (self.EntitiesPoint, self.EntitiesLink, self.EntitiesExpr)
        try:
            for table in tables:
                table.rowSelectionChanged.disconnect()
        except TypeError:
            pass
        tables[index].rowSelectionChanged.connect(self.MainCanvas.setSelection)
        # Double click signal.
        try:
            self.MainCanvas.doubleclick_edit.disconnect()
        except TypeError:
            pass
        if index == 0:
            self.MainCanvas.doubleclick_edit.connect(self.editPoint)
        elif index == 1:
            self.MainCanvas.doubleclick_edit.connect(self.editLink)
        # Clear all selections.
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
    
    @pyqtSlot(name='on_action_About_Qt_triggered')
    def aboutQt(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)
    
    @pyqtSlot(name='on_action_Save_branch_triggered')
    def saveBranch(self):
        """Save as new branch action."""
        self.save(True)
    
    @pyqtSlot(QListWidgetItem, name='on_mechanism_storage_itemDoubleClicked')
    def __doubleClickStorage(self, item):
        """Restore the storage data as below."""
        self.restoreStorage(item)
