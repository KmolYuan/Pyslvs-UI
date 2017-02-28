# -*- coding: utf-8 -*-
##PySolvespace - PyQt 5 GUI with Solvespace Library
##Copyright (C) 2016 Yuan Chang [daan0014119@gmail.com]
from sys import exit, argv
from core.info.info import show_version, Pyslvs_Splash
from core.main import MainWindow
if __name__=="__main__":
    start = show_version()
    if start:
        from PyQt5.QtWidgets import QApplication
        if "--fusion" in argv or "-f" in argv: QApplication.setStyle("fusion")
        app = QApplication(argv)
        splash = Pyslvs_Splash()
        splash.show()
        run = MainWindow()
        run.show()
        splash.finish(run)
        exit(app.exec())
