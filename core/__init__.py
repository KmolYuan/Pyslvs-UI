# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import argv, exit
from platform import system
from .QtModules import QApplication
from .info import ARGUMENTS, INFO, Splash, logger
from .main_window import MainWindow

__all__ = ['main']


def main():
    """Startup function."""
    for info_str in INFO:
        logger.info(info_str)

    logger.info('-' * 7)

    if ARGUMENTS.test:
        logger.info("All module loaded successfully.")
        exit(0)

    app = QApplication(argv)

    # Force enable fusion style on Mac OS.
    if system() == 'Darwin':
        ARGUMENTS.fusion = True

    # Fusion style.
    if ARGUMENTS.fusion:
        app.setStyle('fusion')

    splash = Splash()
    splash.show()

    run = MainWindow()
    run.show()
    splash.finish(run)
    splash.deleteLater()

    exit(app.exec())
