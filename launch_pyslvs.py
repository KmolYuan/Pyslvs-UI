# -*- coding: utf-8 -*-
##Pyslvs - Dimensional Synthesis of Planar Four-bar Linkages in PyQt5 GUI.
##Copyright (C) 2016 Yuan Chang [daan0014119@gmail.com]
from sys import exit
if __name__=='__main__':
    try:
        from core.info.info import show_info, Pyslvs_Splash
        args = show_info()
        from PyQt5.QtWidgets import QApplication
        from core.main import MainWindow
        if args.fusion: QApplication.setStyle('fusion')
        app = QApplication(list(vars(args).values()))
        splash = Pyslvs_Splash()
        splash.show()
        run = MainWindow(args)
        run.show()
        splash.finish(run)
        exit(app.exec())
    except Exception as e:
        if e!=SystemExit:
            import logging, traceback
            logging.basicConfig(filename='PyslvsLogFile.log', filemode='a', level=logging.WARNING)
            logging.exception("Exception Happened.")
            traceback.print_tb(e.__traceback__)
            print(e)
            exit(1)
