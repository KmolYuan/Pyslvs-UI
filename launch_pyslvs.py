# -*- coding: utf-8 -*-
##Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.
##Copyright (C) 2016 Yuan Chang [daan0014119@gmail.com]
from sys import exit, argv
from core.info.info import show_version, Pyslvs_Splash
from core.main import MainWindow
if __name__=="__main__":
    args = show_version()
    from PyQt5.QtWidgets import QApplication
    if args.fusion: QApplication.setStyle('fusion')
    app = QApplication(argv)
    splash = Pyslvs_Splash()
    splash.show()
    run = MainWindow(args)
    run.show()
    splash.finish(run)
    exit(app.exec())
