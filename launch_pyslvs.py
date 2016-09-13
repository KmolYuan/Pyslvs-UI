from sys import exit, argv
from core.info.version import show_version

#Start Pyslvs
if __name__=="__main__":
    show_version()
    from PyQt5.QtWidgets import QApplication
    from core.main import MainWindow
    QApplication.setStyle("fusion")
    app = QApplication(argv)
    run  = MainWindow()
    run.show()
    exit(app.exec())
