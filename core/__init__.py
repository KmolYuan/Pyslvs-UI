# -*- coding: utf-8 -*-

"""'core' module contains a main startup function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"
__all__ = ['main']

app = None


def main() -> None:
    """Startup function."""
    global app
    from time import perf_counter
    t0 = perf_counter()

    from sys import argv, exit
    from logging import shutdown
    from platform import system
    from .QtModules import Qt, QApplication, QPixmap, QSplashScreen
    from .info import ARGUMENTS, logger
    if ARGUMENTS.test:
        from .main_window import MainWindow
        logger.info("All module loaded successfully.")
        shutdown()
        exit(0)

    app = QApplication(argv)
    import preview_rc
    splash = QSplashScreen(QPixmap(":/icons/splash.png"))
    splash.showMessage(f"{__author__} {__copyright__}", Qt.AlignBottom | Qt.AlignRight)
    splash.show()

    # Force enable fusion style on macOS
    if system() == 'Darwin':
        ARGUMENTS.fusion = True
    if ARGUMENTS.fusion:
        app.setStyle('fusion')

    from .main_window import MainWindow
    w = MainWindow()
    w.show()
    splash.finish(w)
    splash.deleteLater()
    logger.info(f"Startup with: {perf_counter() - t0:.02f}s")
    if not ARGUMENTS.debug_mode:
        w.console_connect()
    del preview_rc, splash, t0

    qt_exit_code = app.exec_()
    shutdown()
    exit(qt_exit_code)
