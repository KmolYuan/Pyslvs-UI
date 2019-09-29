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
    from os.path import join
    from logging import shutdown
    from platform import system
    from qtpy.QtCore import Qt, QDir, QLockFile
    from qtpy.QtWidgets import QApplication, QSplashScreen
    from qtpy.QtGui import QPixmap
    from .info import ARGUMENTS, logger
    if ARGUMENTS.test:
        from importlib import import_module
        import_module('pyslvs_ui.main_window')
        logger.info("All module loaded successfully.")
        logger.info(f"Loaded with: {perf_counter() - t0:.02f}s")
        shutdown()
        exit(0)

    _app = QApplication(argv)
    lf = QLockFile(join(QDir.tempPath(), "pyslvs.lock"))
    if not lf.tryLock(100):
        logger.info("Pyslvs can only start one instance.")
        shutdown()
        exit(0)
    sp = QSplashScreen(QPixmap(":/icons/splash.png"))
    sp.showMessage(f"{__author__} {__copyright__}", Qt.AlignBottom | Qt.AlignRight)
    sp.show()

    # Force enable fusion style on macOS
    if system() == 'Darwin':
        ARGUMENTS.fusion = True
    if ARGUMENTS.fusion:
        _app.setStyle('fusion')

    from .main_window import MainWindow
    sp.finish(MainWindow.new())
    sp.deleteLater()
    logger.info(f"Startup with: {perf_counter() - t0:.02f}s")
    del sp, t0

    qt_exit_code = _app.exec_()
    shutdown()
    exit(qt_exit_code)
