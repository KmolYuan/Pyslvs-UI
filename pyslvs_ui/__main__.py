# -*- coding: utf-8 -*-

"""Launch script from module level."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from time import process_time

_app = None


def main() -> None:
    """Startup function."""
    global _app
    t0 = process_time()
    exit_code = 0
    from sys import argv, exit
    from logging import shutdown
    from platform import system
    from pyslvs_ui.info import ARGUMENTS, parse_args, sign_in_logger, logger
    parse_args()
    sign_in_logger()
    if ARGUMENTS.cmd in {'gui', None}:
        from qtpy.QtCore import Qt, qInstallMessageHandler
        from qtpy.QtWidgets import QApplication, QSplashScreen
        from qtpy.QtGui import QPixmap
        _app = QApplication(argv)
        # Depress Qt warning
        qInstallMessageHandler(lambda _0, _1, _2: None)
        # Splash
        sp = QSplashScreen(QPixmap("icons:splash.png"))
        sp.showMessage(f"{__author__} {__copyright__}",
                       Qt.AlignBottom | Qt.AlignRight)
        sp.show()
        # Force enable fusion style on macOS
        if system() == 'Darwin':
            ARGUMENTS.fusion = True
        if ARGUMENTS.fusion:
            _app.setStyle('fusion')
        # Main window
        from pyslvs_ui.main_window import MainWindow
        w = MainWindow.new()
        sp.finish(w)
        sp.deleteLater()
        logger.info(f"Startup with: {process_time() - t0:.02f}s")
        if not ARGUMENTS.debug_mode:
            w.console_connect()
        del sp, w
        exit_code = _app.exec_()
    elif ARGUMENTS.cmd == 'test':
        from importlib import import_module
        import_module('pyslvs_ui.main_window')
        logger.info("All module loaded successfully.")
        logger.info(f"Loaded with: {process_time() - t0:.02f}s")
    else:
        raise ValueError(f"unknown command: {ARGUMENTS.cmd}")
    shutdown()
    exit(exit_code)


if __name__ == '__main__':
    main()
