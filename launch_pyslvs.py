# -*- coding: utf-8 -*-
##PySolvespace - PyQt 5 GUI with Solvespace Library
##Copyright (C) 2016 Yuan Chang [daan0014119@gmail.com]
from sys import exit, argv
from core.info.version import show_info, show_help, show_version
from core.main import MainWindow
if __name__=="__main__":
    show_version()
    if "--help" in argv or "-h" in argv: show_help()
    elif "--version" in argv or "-v" in argv: pass
    else:
        show_info()
        from PyQt5.QtWidgets import QApplication, QSplashScreen
        from PyQt5.QtGui import QPixmap
        if "--fusion" in argv or "-f" in argv: QApplication.setStyle("fusion")
        app = QApplication(argv)
        splash = QSplashScreen(QPixmap(":/icons/title.png"))
        splash.show()
        run = MainWindow()
        run.show()
        splash.finish(run)
        exit(app.exec())
