# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]
from sys import exit
from core import *

if __name__=='__main__':
    if args.server:
        startRep(args.server)
        exit(0)
    elif args.test:
        print(ImportTest)
        exit(0)
    else:
        print('\n'.join(INFO+('-'*7,)))
        from PyQt5.QtWidgets import QApplication
        QApp = QApplication([])
        if args.fusion:
            QApp.setStyle('fusion')
        splash = Pyslvs_Splash()
        splash.show()
        run = MainWindow(args)
        run.show()
        splash.finish(run)
        exit(QApp.exec())
