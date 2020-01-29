# -*- coding: utf-8 -*-

"""Compile source code files from UI files."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from os import walk
from os.path import join
import re
from qtpy import PYQT5
if PYQT5:
    from PyQt5.uic import compileUi
    from PyQt5.pyrcc_main import processResourceFile
else:
    raise ModuleNotFoundError("no compiler found")


def gen_ui():
    """Compile GUIs."""
    count = 0
    for root, _, files in walk("pyslvs_ui"):
        for file in files:
            if not file.endswith('.ui'):
                continue
            target_name = re.sub(r"([\w ]+)\.ui", r"\1_ui.py", file)
            with open(join(root, target_name), 'w+', encoding='utf-8') as f:
                compileUi(
                    join(root, file).replace('\\', '/'),
                    f,
                    from_imports='pyslvs_ui',
                    import_from='pyslvs_ui'
                )
                f.seek(0)
                script_new = (
                    f.read()
                    .replace("from PyQt5 import", "from qtpy import")
                    .replace("from PySide2 import", "from qtpy import")
                )
                f.seek(0)
                f.truncate()
                f.write(script_new)
            count += 1
    print(f"Compiled {count} UI file(s)")


def gen_qrc():
    """Compile icons."""
    count = 0
    for root, _, files in walk("pyslvs_ui"):
        for file in files:
            if not file.endswith('.qrc'):
                continue
            target_name = re.sub(r"([\w ]+)\.qrc", r"\1_rc.py", file)
            processResourceFile([join(root, file).replace('\\', '/')], join(root, target_name), False)
            with open(join(root, target_name), 'r+', encoding='utf-8') as f:
                script_new = (
                    f.read()
                    .replace("from PyQt5 import", "from qtpy import")
                    .replace("from PySide2 import", "from qtpy import")
                )
                f.seek(0)
                f.truncate()
                f.write(script_new)
            count += 1
    print(f"Compiled {count} resource file(s)")


if __name__ == '__main__':
    gen_ui()
    # gen_qrc()
