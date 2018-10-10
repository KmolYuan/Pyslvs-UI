# -*- coding: utf-8 -*-

"""'main_window' module contains the methods of main window.

Abstract classes (ordered):
+ MainWindowUiInterface (imported from core.widget.custom)
+ EntitiesMethodInterface (entities)
+ SolverMethodInterface (solver)
+ StorageMethodInterface (storage)
+ ActionMethodInterface (actions)
+ IOMethodInterface (io)
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence
from core.QtModules import (
    pyqtSlot,
    qt_image_format,
    QMessageBox,
    QInputDialog,
    QTextCursor,
    QListWidgetItem,
)
from core.info import ARGUMENTS
from core.io import XStream, str_between
from .io import IOMethodInterface

__all__ = ['MainWindow']


class MainWindow(IOMethodInterface):

    """The main window of Pyslvs.

    Inherited from QMainWindow.
    Exit with QApplication.

    The main window is so much method that was been split it
    to wrapper function in 'main_window' module.
    """

    def __init__(self):
        """Notes:

        + Input command line arguments object from Python parser.
        + Command line arguments excluding any Qt startup option.
        + Start main window with no parent.
        """
        super(MainWindow, self).__init__()
        self.restoreSettings()

        # Console widget.
        self.consoleerror_option.setChecked(ARGUMENTS.debug_mode)
        if not ARGUMENTS.debug_mode:
            self.__console_connect()

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
        if index != self.DatabaseWidget.Stack:
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

    @pyqtSlot(bool, name='on_action_show_dimensions_toggled')
    def __set_show_dimensions(self, toggled: bool):
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_show_point_mark.setChecked(True)

    @pyqtSlot(bool, name='on_action_show_point_mark_toggled')
    def __set_show_point_mark(self, toggled: bool):
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_show_dimensions.setChecked(False)

    @pyqtSlot(name='on_action_path_style_triggered')
    def __set_curve_mode(self):
        """Set path style as curve (true) or dots (false)."""
        self.MainCanvas.setCurveMode(self.action_path_style.isChecked())

    @pyqtSlot(int, name='on_SynthesisTab_currentChanged')
    def __set_show_target_path(self, index: int):
        """Dimensional synthesis information will show on the canvas."""
        self.MainCanvas.setShowTargetPath(index == 2)

    def addTargetPoint(self):
        """Use context menu to add a target path coordinate."""
        self.DimensionalSynthesis.addPoint(self.mouse_pos_x, self.mouse_pos_y)

    @pyqtSlot(int, tuple)
    def mergeResult(self, row: int, path: Sequence[Sequence[Tuple[float, float]]]):
        """Merge result function of dimensional synthesis."""
        result = self.DimensionalSynthesis.mechanism_data(row)
        # exp_symbol = ['A', 'B', 'C', 'D', 'E']
        exp_symbol = []
        for exp in result['Link_expr'].split(';'):
            for name in str_between(exp, '[', ']').split(','):
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
                color=("Dark-Orange" if tag in result['Target'] else None)
            )
        for i, exp in enumerate(result['Link_expr'].split(';')):
            self.addNormalLink(tuple(
                tmp_dict[name] for name in str_between(exp, '[', ']').split(',')
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
    def __set_selection_mode(self, index: int):
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

    @pyqtSlot(name='on_background_choose_dir_clicked')
    def __set_background(self):
        """Show up dialog to set the background file path."""
        file_name = self.inputFrom("Background", qt_image_format)
        if file_name:
            self.background_option.setText(file_name)

    @pyqtSlot(name='on_console_connect_button_clicked')
    def __console_connect(self):
        """Turn the OS command line (stdout) log to console."""
        print("Connect to GUI console.")
        XStream.stdout().messageWritten.connect(self.__append_to_console)
        XStream.stderr().messageWritten.connect(self.__append_to_console)
        self.console_connect_button.setEnabled(False)
        self.console_disconnect_button.setEnabled(True)
        print("Connect to GUI console.")

    @pyqtSlot(name='on_console_disconnect_button_clicked')
    def __console_disconnect(self):
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

    @pyqtSlot(bool, name='on_action_full_screen_toggled')
    def __full_screen(self, full_screen: bool):
        """Show full screen or not."""
        if full_screen:
            self.showFullScreen()
        else:
            self.showMaximized()

    @pyqtSlot(name='on_action_about_qt_triggered')
    def __about_qt(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)

    @pyqtSlot(name='on_action_commit_branch_triggered')
    def commit_branch(self):
        """Save as new branch action."""
        self.commit(True)

    @pyqtSlot(QListWidgetItem, name='on_mechanism_storage_itemDoubleClicked')
    def __double_click_storage(self, item):
        """Restore the storage data as below."""
        self.restoreStorage(item)
