# -*- coding: utf-8 -*-

"""'core' module will load necessaries when startup."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from sys import exit
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
    for info in INFO:
        print(info)
    print('-' * 7)
    QApp = QApplication([])
    if ARGUMENTS.fusion:
        QApp.setStyle('fusion')
    splash = PyslvsSplash()
    splash.show()
    run = MainWindow(ARGUMENTS)
    run.show()
    splash.finish(run)
    exit(QApp.exec())
