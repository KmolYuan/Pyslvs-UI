# -*- coding: utf-8 -*-

'''
PySolvespace - PyQt 5 GUI with Solvespace Library
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com
'''

from sys import exit, argv
from core.info.version import show_info, show_help, show_version

#Start Pyslvs
if __name__=="__main__":
    if "--help" in argv or "-h" in argv: show_help()
    elif "--version" in argv or "-v" in argv: show_version()
    else:
        show_info()
        from PyQt5.QtWidgets import QApplication
        from core.main import MainWindow
        QApplication.setStyle("fusion")
        app = QApplication(argv)
        run  = MainWindow()
        run.show()
        exit(app.exec())
