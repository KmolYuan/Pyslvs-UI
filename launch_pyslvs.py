# -*- coding: utf-8 -*-
##Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.
##Copyright (C) 2016 Yuan Chang [daan0014119@gmail.com]
from sys import exit
from core.info.info import show_info, Pyslvs_Splash
if __name__=='__main__':
    args = show_info()
    from PyQt5.QtWidgets import QApplication
    if args.fusion: QApplication.setStyle('fusion')
    app = QApplication(list(vars(args).values()))
    splash = Pyslvs_Splash()
    splash.show()
    from core.main import MainWindow
    run = MainWindow(args)
    run.show()
    splash.finish(run)
    exit(app.exec())
