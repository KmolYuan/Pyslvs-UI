from sys import exit, argv
from core.info.version import show_info, show_help, show_version
from core.io.transfer import Transfer

#Start Pyslvs
if __name__=="__main__":
    for i in argv:
        if ".csv" in i:
            tra = Transfer()
            tra.input_file(argv[argv.index(i)][2::])
            if "--check" in argv:
                tra.show_dxf()
                break
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
