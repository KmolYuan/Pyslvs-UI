# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]
from sys import exit
if __name__=='__main__':
    try:
        from core.info.info import show_info, Pyslvs_Splash
        args = show_info()
        if args.server:
            from core.server.zmq_rep import startRep
            startRep(args.server)
            exit()
        else:
            from PyQt5.QtWidgets import QApplication
            from core.main import MainWindow
            QApp = QApplication(list(vars(args).values()))
            if args.fusion:
                QApp.setStyle('fusion')
            splash = Pyslvs_Splash()
            splash.show()
            run = MainWindow(args)
            run.show()
            splash.finish(run)
            exit(QApp.exec())
    except Exception as e:
        if e!=SystemExit:
            import logging, traceback
            logging.basicConfig(filename='pyslvs_error.log', filemode='a', level=logging.WARNING)
            logging.exception("Exception Happened.")
            traceback.print_tb(e.__traceback__)
            print(e)
            exit(1)
