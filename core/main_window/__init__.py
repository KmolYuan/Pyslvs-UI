# -*- coding: utf-8 -*-

"""'main_window' module contains the methods of main window.

Abstract classes (ordered):
+ MainWindowBase (imported from core.widget.custom)
+ EntitiesMethodInterface (entities)
+ SolverMethodInterface (solver)
+ StorageMethodInterface (storage)
+ ActionMethodInterface (actions)
+ IOMethodInterface (io)
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence
from core.QtModules import (
    Slot,
    qt_image_format,
    QMessageBox,
    QInputDialog,
    QTextCursor,
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
        self.restore_settings()

        # Console widget.
        self.consoleerror_option.setChecked(ARGUMENTS.debug_mode)
        if not ARGUMENTS.debug_mode:
            self.__console_connect()

        # Start first solve function calling.
        self.solve()

        # Load workbook from argument.
        self.load_from_args()

    def closeEvent(self, event):
        """Close event to avoid user close the window accidentally."""
        if self.check_file_changed():
            event.ignore()
            return
        if self.InputsWidget.inputs_playShaft.isActive():
            self.InputsWidget.inputs_playShaft.stop()
        self.save_settings()
        XStream.back()
        print("Exit.")
        event.accept()

    @Slot(int, name='on_ZoomBar_valueChanged')
    def __set_zoom(self, value: int):
        """Reset the text when zoom bar changed."""
        self.zoom_button.setText(f'{value}%')

    @Slot()
    def customize_zoom(self):
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

    @Slot(bool, name='on_action_show_dimensions_toggled')
    def __set_show_dimensions(self, toggled: bool):
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_show_point_mark.setChecked(True)

    @Slot(bool, name='on_action_show_point_mark_toggled')
    def __set_show_point_mark(self, toggled: bool):
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_show_dimensions.setChecked(False)

    @Slot(name='on_action_path_style_triggered')
    def __set_curve_mode(self):
        """Set path style as curve (true) or dots (false)."""
        self.MainCanvas.set_curve_mode(self.action_path_style.isChecked())

    @Slot(int, name='on_Panel_currentChanged')
    @Slot(int, name='on_SynthesisTab_currentChanged')
    def __set_show_target_path(self, _: int):
        """Dimensional synthesis information will show on the canvas."""
        panel_index = self.Panel.currentIndex()
        synthesis_index = self.SynthesisTab.currentIndex()
        self.MainCanvas.set_show_target_path(panel_index == synthesis_index == 2)

    def add_target_point(self):
        """Use context menu to add a target path coordinate."""
        self.DimensionalSynthesis.add_point(self.mouse_pos_x, self.mouse_pos_y)

    @Slot(int, tuple)
    def merge_result(self, row: int, path: Sequence[Sequence[Tuple[float, float]]]):
        """Merge result function of dimensional synthesis."""
        result = self.DimensionalSynthesis.mechanism_data[row]
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
            tmp_dict[tag] = self.add_point(
                result[tag][0],
                result[tag][1],
                color=("Dark-Orange" if tag in result['Target'] else 'Green')
            )
        for i, exp in enumerate(result['Link_expr'].split(';')):
            self.add_normal_link(tuple(
                tmp_dict[name] for name in str_between(exp, '[', ']').split(',')
            ))
            if i == 0:
                self.constrain_link(self.EntitiesLink.rowCount() - 1)
        self.CommandStack.endMacro()
        # Add the path.
        i = 0
        while f"Algorithm_{i}" in self.InputsWidget.path_data():
            i += 1
        self.InputsWidget.add_path(f"Algorithm_{i}", path)
        self.MainCanvas.zoom_to_fit()

    @Slot(name='on_background_choose_dir_clicked')
    def __set_background(self):
        """Show up dialog to set the background file path."""
        file_name = self.input_from("Background", qt_image_format)
        if file_name:
            self.background_option.setText(file_name)

    @Slot(name='on_console_connect_button_clicked')
    def __console_connect(self):
        """Turn the OS command line (stdout) log to console."""
        print("Connect to GUI console.")
        XStream.stdout().messageWritten.connect(self.__append_to_console)
        XStream.stderr().messageWritten.connect(self.__append_to_console)
        self.console_connect_button.setEnabled(False)
        self.console_disconnect_button.setEnabled(True)
        print("Connect to GUI console.")

    @Slot(name='on_console_disconnect_button_clicked')
    def __console_disconnect(self):
        """Turn the console log to OS command line (stdout)."""
        print("Disconnect from GUI console.")
        XStream.back()
        self.console_connect_button.setEnabled(True)
        self.console_disconnect_button.setEnabled(False)
        print("Disconnect from GUI console.")

    @Slot(str)
    def __append_to_console(self, log: str):
        """After inserted the text, move cursor to end."""
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)
        self.consoleWidgetBrowser.insertPlainText(log)
        self.consoleWidgetBrowser.moveCursor(QTextCursor.End)

    @Slot(bool, name='on_action_full_screen_toggled')
    def __full_screen(self, full_screen: bool):
        """Show full screen or not."""
        if full_screen:
            self.showFullScreen()
        else:
            self.showMaximized()

    @Slot(name='on_action_about_qt_triggered')
    def __about_qt(self):
        """Open Qt about."""
        QMessageBox.aboutQt(self)

    @Slot(name='on_action_commit_branch_triggered')
    def commit_branch(self):
        """Save as new branch action."""
        self.commit(True)
