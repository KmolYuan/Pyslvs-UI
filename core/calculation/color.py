# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
def colorlist():
    return {
        "Red":Qt.red,
        "Green":Qt.green,
        "Blue":Qt.blue,
        "Cyan":Qt.cyan,
        "Magenta":Qt.magenta,
        "Yellow":Qt.yellow,
        "Gray":Qt.gray,
        "Orange":QColor(225, 165, 0),
        "Pink":QColor(225, 192, 230),
        "Black":Qt.black,
        "White":Qt.white,
        "Dark-Red":Qt.darkRed,
        "Dark-Green":Qt.darkGreen,
        "Dark-Blue":Qt.darkBlue,
        "Dark-Cyan":Qt.darkCyan,
        "Dark-Magenta":Qt.darkMagenta,
        "Dark-Yellow":Qt.darkYellow,
        "Dark-Gray":Qt.darkGray,
        "Dark-Orange":QColor(225, 140, 0),
        "Dark-Pink":QColor(225, 20, 147),
        }
def colorName():
    return [e for e in colorlist()]
