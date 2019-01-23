# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import argv, exit
from platform import system
from .QtModules import QApplication
from core.main_window import MainWindow
from .info import ARGUMENTS, INFO, Splash

__all__ = ['main']


def main():
    """Startup function."""
    for info_str in INFO:
        print(info_str)

    print('-' * 7)

    if ARGUMENTS.test:
        print("All module loaded successfully.")
        exit(0)

    app = QApplication(argv)

    # Force fusion style on Mac OS.
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

    exit(app.exec())
