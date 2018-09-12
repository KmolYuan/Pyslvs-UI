# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import exit
import platform
from .QtModules import QApplication
from .main import MainWindow
from .info import (
    ARGUMENTS,
    INFO,
    PyslvsSplash
)

__all__ = ['main']


def main():
    """Startup function."""
    for info_str in INFO:
        print(info_str)
    print('-' * 7)
    if ARGUMENTS.test:
        print("All module loaded successfully.")
        exit(0)
    app = QApplication([])
    if platform.system() == 'Darwin':
        ARGUMENTS.fusion = True
    if ARGUMENTS.fusion:
        app.setStyle('fusion')
    splash = PyslvsSplash()
    splash.show()
    run = MainWindow()
    run.show()
    splash.finish(run)
    exit(app.exec())
