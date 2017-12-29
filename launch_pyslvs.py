# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]
from sys import exit
from core.info.info import INFO, args

if __name__=='__main__':
    if args.server:
        from core.server.zmq_rep import startRep
        startRep(args.server)
        exit(0)
    elif args.test:
        from core.main import MainWindow
        print("All modules are loaded.")
        exit(0)
    else:
        print('\n'.join(INFO+('-'*7,)))
        from PyQt5.QtWidgets import QApplication
        from core.main import MainWindow
        QApp = QApplication([])
        if args.fusion:
            QApp.setStyle('fusion')
        from core.info.about import Pyslvs_Splash
        splash = Pyslvs_Splash()
        splash.show()
        run = MainWindow(args)
        run.show()
        splash.finish(run)
        exit(QApp.exec())
