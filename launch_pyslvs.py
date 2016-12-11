# -*- coding: utf-8 -*-
'''
Start Pyslvs
PySolvespace - PyQt 5 GUI with Solvespace Library
Including Python module: PyQt5, peewee, dxfwrite
Copyright (C) 2016 Yuan Chang
E-mail: daan0014119@gmail.com
'''
from sys import exit, argv
from core.info.version import show_info, show_help, show_version
if __name__=="__main__":
    show_version()
    if "--help" in argv or "-h" in argv: show_help()
    elif "--version" in argv or "-v" in argv: pass
    else:
        show_info()
        from PyQt5.QtWidgets import QApplication
        from core.main import MainWindow
        if "--fusion" in argv: QApplication.setStyle("fusion")
        app = QApplication(argv)
        run  = MainWindow()
        run.show()
        exit(app.exec())
