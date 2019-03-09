# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"
__all__ = ['main']


def main():
    """Startup function."""
    from sys import argv, exit
    from logging import shutdown
    from platform import system

    from .info import ARGUMENTS, logger
    if ARGUMENTS.test:
        logger.info("All module loaded successfully.")
        shutdown()
        exit(0)

    from .QtModules import (
        Qt,
        QApplication,
        QPixmap,
        QSplashScreen,
    )
    import preview_rc
    app = QApplication(argv)
    splash = QSplashScreen(QPixmap(":/icons/splash.png"))
    splash.showMessage(f"{__author__} {__copyright__}", Qt.AlignBottom | Qt.AlignRight)
    splash.show()

    # Force enable fusion style on Mac OS.
    if system() == 'Darwin':
        ARGUMENTS.fusion = True

    # Fusion style.
    if ARGUMENTS.fusion:
        app.setStyle('fusion')

    from .main_window import MainWindow
    del preview_rc
    run = MainWindow()
    run.show()
    splash.finish(run)
    splash.deleteLater()

    qt_exit_code = app.exec()
    shutdown()
    exit(qt_exit_code)
