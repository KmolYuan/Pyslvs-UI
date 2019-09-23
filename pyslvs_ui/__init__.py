# -*- coding: utf-8 -*-

"""Pyslvs-UI module."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from pyslvs import __version__

__all__ = ['main', '__version__']

_app = None


def main() -> None:
    """Startup function."""
    global _app
    from time import perf_counter
    t0 = perf_counter()

    from sys import argv, exit
    from logging import shutdown
    from platform import system
    from qtpy.QtCore import Qt
    from qtpy.QtWidgets import QApplication, QSplashScreen
    from qtpy.QtGui import QPixmap
    from .core.info import ARGUMENTS, logger
    if ARGUMENTS.test:
        from importlib import import_module
        import_module('pyslvs_ui.core.main_window')
        logger.info("All module loaded successfully.")
        logger.info(f"Loaded with: {perf_counter() - t0:.02f}s")
        shutdown()
        exit(0)

    _app = QApplication(argv)
    splash = QSplashScreen(QPixmap(":/icons/splash.png"))
    splash.showMessage(f"{__author__} {__copyright__}", Qt.AlignBottom | Qt.AlignRight)
    splash.show()

    # Force enable fusion style on macOS
    if system() == 'Darwin':
        ARGUMENTS.fusion = True
    if ARGUMENTS.fusion:
        _app.setStyle('fusion')

    from .core.main_window import MainWindow
    w = MainWindow()
    w.show()
    splash.finish(w)
    splash.deleteLater()
    logger.info(f"Startup with: {perf_counter() - t0:.02f}s")
    if not ARGUMENTS.debug_mode:
        w.console_connect()
    del splash, t0

    qt_exit_code = _app.exec_()
    shutdown()
    exit(qt_exit_code)
