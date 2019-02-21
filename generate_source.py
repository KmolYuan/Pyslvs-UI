# -*- coding: utf-8 -*-

"""Generate source code files from UI files."""

from os import listdir, walk
from os.path import join
import re
from PyQt5.uic import compileUi
from PyQt5.pyrcc_main import processResourceFile


def gen_ui():
    for root, _, files in walk("core"):
        for file in files:
            if not file.endswith('.ui'):
                continue
            target_name = re.sub(r"([\w ]+)\.ui", r"Ui_\1.py", file)
            with open(join(root, target_name), 'w+', encoding='utf-8') as f:
                compileUi(join(root, file).replace('\\', '/'), f)
                f.seek(0)
                script_new = f.read().replace(
                    "from PyQt5 import QtCore, QtGui, QtWidgets",
                    "from core.QtModules import QtCore, QtGui, QtWidgets"
                )
                f.seek(0)
                f.truncate()
                f.write(script_new)


def gen_qrc():
    for file in listdir('.'):
        if not file.endswith('.qrc'):
            continue
        target_name = re.sub(r"([\w ]+)\.qrc", r"\1_rc.py", file)
        processResourceFile([file], target_name, False)
        with open(target_name, 'r+', encoding='utf-8') as f:
            script_new = f.read().replace(
                "from PyQt5 import QtCore",
                "from core.QtModules import QtCore",
            )
            f.seek(0)
            f.truncate()
            f.write(script_new)


if __name__ == '__main__':
    gen_ui()
    # gen_qrc()
