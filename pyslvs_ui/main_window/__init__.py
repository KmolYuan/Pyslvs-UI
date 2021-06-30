# -*- coding: utf-8 -*-

"""'main_window' module contains the methods of main window.

Abstract classes (ordered):
+ MainWindowBase (imported from pyslvs_ui.widget.custom)
+ EntitiesMethodInterface (entities)
+ SolverMethodInterface (solver)
+ StorageMethodInterface (storage)
+ ActionMethodInterface (actions)
+ IOMethodInterface (io)
"""

from __future__ import annotations

__all__ = ['MainWindow']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QMessageBox, QInputDialog
from qtpy.QtGui import QTextCursor, QCloseEvent
from pyslvs_ui.info import XStream, logger
from .io import IOMethodInterface


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

        # Start first solve function calling
        self.solve()
        # Load project from argument
        self.load_from_args()

    @staticmethod
    @Slot()
    def new() -> MainWindow:
        """Create a new main window."""
        m = MainWindow()
        m.show()
        m.main_canvas.zoom_to_fit()
        return m

    def closeEvent(self, event: QCloseEvent) -> None:
        """Close event to avoid user close the window accidentally."""
        if self.check_file_changed():
            event.ignore()
            return
        if self.inputs_widget.inputs_play_shaft.isActive():
            self.inputs_widget.inputs_play_shaft.stop()
        self.save_settings()
        XStream.back()
        logger.info("Exit")
        event.accept()

    @Slot(int, name='on_zoom_bar_valueChanged')
    def __set_zoom(self, value: int) -> None:
        """Reset the text when zoom bar changed."""
        self.zoom_btn.setText(f'{value}px')

    @Slot(name='on_zoom_cus_btn_clicked')
    def __customize_zoom(self) -> None:
        """Customize zoom value."""
        value, ok = QInputDialog.getInt(
            self,
            "Zooming",
            "Enter a zoom value: (px)",
            self.zoom_bar.value(),
            self.zoom_bar.minimum(),
            self.zoom_bar.maximum(),
            10
        )
        if ok:
            self.zoom_bar.setValue(value)

    @Slot(name='on_reset_canvas_btn_clicked')
    def __reset_zoom(self) -> None:
        """Reset to default zoom."""
        self.main_canvas.zoom_to_fit()

    @Slot(bool, name='on_action_show_dimensions_toggled')
    def __set_show_dimensions(self, toggled: bool) -> None:
        """If turn on dimension labels, turn on the point marks."""
        if toggled:
            self.action_show_point_mark.setChecked(True)

    @Slot(bool, name='on_action_show_point_mark_toggled')
    def __set_show_point_mark(self, toggled: bool) -> None:
        """If no point marks, turn off the dimension labels."""
        if not toggled:
            self.action_show_dimensions.setChecked(False)

    @Slot(name='on_action_path_style_triggered')
    def __set_curve_mode(self) -> None:
        """Set path style as curve (true) or dots (false)."""
        self.main_canvas.set_curve_mode(self.action_path_style.isChecked())

    @Slot(int, name='on_main_panel_currentChanged')
    @Slot(int, name='on_synthesis_tab_widget_currentChanged')
    def __set_show_target_path(self, _=None) -> None:
        """Dimensional synthesis information will show on the canvas."""
        self.main_canvas.set_show_target_path(
            self.main_panel.currentWidget() is self.synthesis_tab
            and self.synthesis_tab_widget.currentWidget() is self.optimizer
        )

    def add_target_point(self) -> None:
        """Use context menu to add a target path coordinate."""
        self.optimizer.add_point(self.mouse_pos_x, self.mouse_pos_y)

    def merge_result(
        self,
        expr: str,
        path: Sequence[Sequence[Tuple[float, float]]]
    ) -> None:
        """Merge result function of dimensional synthesis."""
        if not self.ask_add_storage(expr):
            return
        # Add the path
        i = 0
        while f"Mechanism {i}" in self.inputs_widget.paths():
            i += 1
        if path:
            self.inputs_widget.add_path(f"Mechanism {i}", path, {})

    @Slot(name='on_console_connect_btn_clicked')
    def console_connect(self) -> None:
        """Turn the OS command line (stdout) log to console."""
        logger.info("Connect to GUI console.")
        XStream.stdout().message_written.connect(self.__append_to_console)
        self.console_connect_btn.setEnabled(False)
        self.console_disconnect_btn.setEnabled(True)
        logger.info("Connect to GUI console.")

    @Slot(name='on_console_disconnect_btn_clicked')
    def console_disconnect(self) -> None:
        """Turn the console log to OS command line (stdout)."""
        logger.info("Disconnect from GUI console.")
        XStream.back()
        self.console_connect_btn.setEnabled(True)
        self.console_disconnect_btn.setEnabled(False)
        logger.info("Disconnect from GUI console.")

    @Slot(str)
    def __append_to_console(self, log: str) -> None:
        """After inserted the text, move cursor to end."""
        self.console_widget_browser.moveCursor(QTextCursor.End)
        self.console_widget_browser.insertPlainText(log)
        self.console_widget_browser.moveCursor(QTextCursor.End)

    @Slot(bool, name='on_action_full_screen_toggled')
    def __full_screen(self, full_screen: bool) -> None:
        """Show full screen or not."""
        if full_screen:
            self.showFullScreen()
        else:
            self.showMaximized()

    @Slot(name='on_action_about_qt_triggered')
    def __about_qt(self) -> None:
        """Open Qt about."""
        QMessageBox.aboutQt(self)
