# -*- coding: utf-8 -*-

"""'core' module contains a main startup function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"
__all__ = ['main']


def main():
    """Startup function."""
    global app
    from time import time
    t0 = time()

    from sys import argv, exit
    from logging import shutdown
    from platform import system
    from .QtModules import (
        Qt,
        QApplication,
        QPixmap,
        QSplashScreen,
    )
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

    # Force enable fusion style on Mac OS
    if system() == 'Darwin':
        ARGUMENTS.fusion = True

    # Fusion style
    if ARGUMENTS.fusion:
        app.setStyle('fusion')

    from .main_window import MainWindow
    run = MainWindow()
    run.show()
    splash.finish(run)
    splash.deleteLater()
    logger.debug(f"Startup with: {time() - t0:.02f}s")
    del preview_rc, splash, t0

    qt_exit_code = app.exec()
    shutdown()
    exit(qt_exit_code)
